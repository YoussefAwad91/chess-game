from pieces import *

WHITE_BACK_ROW = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

class Square:
    x_cords = None
    y_cords = None
    has_piece = False
    piece_color = None
    piece = None

    def __init__(self, x, y, has_piece, piece=None):
        self.x_cords = x
        self.y_cords = y
        self.has_piece = has_piece
        self.piece = piece


class Board:
    squares = []

    def __init__(self,game):
        self.squares = [[Square(column, row, False, None) for row in range(1,8+1)] for column in range(1,8+1)]
        

        white_pawn_1 = Pawn(1,2,"White",self,game)
        white_pawn_1 = Pawn(1,2,"White",self,game)
        white_pawn_1 = Pawn(1,2,"White",self,game)
        white_pawn_1 = Pawn(1,2,"White",self,game)
        white_pawn_1 = Pawn(1,2,"White",self,game)
        white_pawn_1 = Pawn(1,2,"White",self,game)
        white_pawn_1 = Pawn(1,2,"White",self,game)

    def place_piece(self, x, y, piece):
        self.squares[x-1][y-1].has_piece = True
        self.squares[x-1][y-1].piece = piece
    
    def remove_piece(self,x,y):
        self.squares[x-1][y-1].has_piece = False
        self.squares[x-1][y-1].piece = None

    def display(self):
        for r in range(8):
            for c in range(8):
                print(f"{self.squares[c][7-r].x_cords}{self.squares[c][7-r].y_cords} ", end="")
            print("\n")
        print ("\n")

        for r in range(8):
                for c in range(8):
                    print(f"{c}{7-r} ", end="")
                print("\n")
