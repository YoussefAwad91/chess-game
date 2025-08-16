from grid import Board

class Player:

    def __init__(self, game, color):
        self.pieces = []
        self.game = game
        self.color = color
        for piece in self.game.board.pieces:
            if piece.color == self.color:
                self.pieces.append(piece)
        self.all_current_moves = []


class Game:

    def __init__(self):
        self.board = Board(self)
        self.white_score = 0
        self.black_score = 0 
        self.move_number = 0
        self.white_player = Player(self, "white")
        self.black_player = Player(self, "black")

        self.current_moves = []
        self.current_piece = None

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
    
    def get_score(self):
        self.black_score = 0
        self.white_score = 0 

        for piece in self.board.pieces:
            if piece.is_captured:
                if piece.color == "white":
                    self.black_score += piece.VALUE
                else:
                    self.white_score += piece.VALUE


""" game = Game()


game.board.get_piece("w_p_5").display_moves_graphical()
game.board.get_piece("w_p_5").move_piece(5,4)
game.board.get_piece("b_p_5").display_moves_graphical()
game.board.get_piece("b_p_5").move_piece(5,5)
game.board.get_piece("b_q").display_moves_graphical()
game.board.get_piece("b_q").move_piece(6,6)
game.board.get_piece("w_n_1").display_moves_graphical()
game.board.get_piece("w_n_1").move_piece(3,3)
game.board.get_piece("b_q").display_moves_graphical()
game.board.get_piece("b_q").move_piece(6,3)
game.board.get_piece("w_q").display_moves_graphical() """


