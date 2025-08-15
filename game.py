from grid import Board

class Player:

    def __init__(self, game, color):
        self.pieces = []
        self.game = game
        self.color = color
        for piece in self.game.board.pieces:
            if piece.color == self.color:
                self.pieces.append(piece)


class Game:

    def __init__(self):
        self.board = Board(self)
        self.white_score = 0
        self.black_score = 0 
        self.move_number = 0
        self.white_player = Player(self, "white")
        self.black_player = Player(self, "black")

    def get_player_turn(self):
        if self.move_number%2 == 0:
            return "white"
        else:
            return "black"

    def get_piece_list(self,color):
        if color == "white":
            return self.white_player.pieces
        else: 
            return self.black_player.pieces
    
    def select_piece(self, code):
        return self.board.get_piece(code).moves()


game = Game()

game.board.display_board()
game.board.get_piece("w_p_5").moves()
game.board.get_piece("w_p_5").move_piece(5,4)
game.board.display_board()

