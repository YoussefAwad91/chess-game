from constants import *
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn

learning_rate = 1e-3

#generating move vocabulary
squares = [file+rank for file in FILES for rank in RANKS]
vocab_list = [initial + to for initial in squares for to in squares if initial != to ]
vocab_list.extend([file+"7"+chr((ord(file)+dx))+"8"+prom for file in FILES for prom in PROMOTIONS for dx in [-1,0,1]])
vocab_list.extend([file+"2"+chr(ord(file)+dx)+"1"+prom for file in FILES for prom in PROMOTIONS for dx in [-1,0,1]])

vocab_list = [PAD, SOS, EOS] + vocab_list

move2inx = {move:i for i, move in enumerate(vocab_list)}
inx2move = {i:move for move, i in move2inx.items()}

#encoding training batch
batch = []
with open("pgns/all_games_uci.txt") as file:
    for line in file:
        batch.append([move2inx[move] for move in line.strip().split()])
batch = [[move2inx[SOS]] + game + [move2inx[EOS]] for game in batch]

#padding sequence for consistent lengths
max_seq = max([len(game) for game in batch])

for game in batch:
    game.extend([move2inx[PAD]]*(max_seq-len(game)))

#creating and loading dataset
batch_tensor = torch.tensor(batch, dtype = torch.long)
inputs_tensor = batch_tensor[:, :-1]
targets_tensor = batch_tensor[:,1:]

class ChessDataset(Dataset):
    def __init__(self, inputs, targets):
        self.inputs = inputs
        self.targets = targets
    
    def __len__(self):
        return self.inputs.size(0)
    
    def __getitem__(self, index):
        return self.inputs[index], self.targets[index]
    
dataset = ChessDataset(inputs_tensor, targets_tensor)
dataloader = DataLoader(dataset=dataset, batch_size=32, shuffle=True)


class ChessLLM(nn.Module):
    def __init__(self, vocab_size, embed_size=128, n_heads = 4, n_layers=4, seq_length=400):
        super().__init__()
        self.embedding =  nn.Embedding(vocab_size, embed_size)
        encoder_layer = nn.TransformerEncoderLayer(d_model = embed_size,nhead=n_heads, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.fc_out = nn.Linear(embed_size, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        x= self.transformer(x)
        logits = self.fc_out(x)
        return logits
    
model = ChessLLM(vocab_size=len(vocab_list))
criterion = nn.CrossEntropyLoss(ignore_index=move2inx[PAD])
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate) #learning rate


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

num_epochs = 5

for epoch in range(num_epochs):
    model.train()  
    total_loss = 0

    for x_batch, y_batch in dataloader:
        print(total_loss)
        x_batch, y_batch = x_batch.to(device), y_batch.to(device)

        optimizer.zero_grad()
        logits = model(x_batch)
        loss = criterion(logits.view(-1, logits.size(-1)), y_batch.view(-1))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    avg_loss = total_loss / len(dataloader)
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {avg_loss:.4f}")


torch.save({
    "model_state": model.state_dict(),
    "move2inx": move2inx,
    "inx2move": inx2move,
    "vocab_size": model.vocab_size,
    "embed_dim": 128,
    "n_heads": 4,
    "n_layers": 4
}, "chess_llm_checkpoint.pth")
