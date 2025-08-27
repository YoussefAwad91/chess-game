import chess
import chess.pgn
import glob

def pgn_to_uci(pgn_file):
    games_uci = []
    with open(pgn_file, "r", encoding="utf-8") as f:
        # Read PGN file, one game at a time
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            board = game.board()
            uci_moves = []
            for move in game.mainline_moves():
                board.push(move)
                uci_moves.append(move.uci())
            games_uci.append(" ".join(uci_moves))
    return games_uci

def merge_txt_to_uci(input_pattern, output_file):
    all_games = []
    for filename in glob.glob(input_pattern):
        print(filename)
        all_games.extend(pgn_to_uci(filename))
    
    with open(output_file, "w", encoding="utf-8") as out:
        for game in all_games:
            out.write(game + "\n")

# Example usage:
# Will look for all .txt files in current folder and merge them into "all_games.uci"
merge_txt_to_uci("pgns/clean data/*.txt", "pgns/all_games_uci.txt")
print("done")
