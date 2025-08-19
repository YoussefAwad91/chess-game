from pieces import *
from constants import *

BACK_ROW = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook] # for creating pieces

# todo: can include different back_row for 960 format

class Square:
    def __init__(self, x, y, has_piece, piece=None):
        self.x_cords = x
        self.y_cords = y
        self.has_piece = has_piece
        self.piece = piece

class Board:
    def __init__(self,game):
        self.pieces = []
        self.game = game
        self.virtual = False
        self.squares = [[Square(column, row, False, None) for row in range(1,8+1)] for column in range(1,8+1)]

        for color, back_row, pawn_row in [("white",0,1),("black",7,6)]: #list indices
            for column, piece_class in enumerate(BACK_ROW):
                self.squares[column][back_row].piece = piece_class(column+1, back_row+1, color, self, game, f"{color[0]}_{CODES[column]}{"_1" if column<3 else "_2" if column>4 else ""}")
                self.pieces.append(self.squares[column][back_row].piece)
            
            for column in range(0,8):
                 self.squares[column][pawn_row].piece = Pawn(column+1, pawn_row+1, color, self, game, f"{color[0]}_p_{column+1}")
                 self.pieces.append(self.squares[column][pawn_row].piece)

    def place_piece(self, x, y, piece):
        self.squares[x-1][y-1].has_piece = True
        self.squares[x-1][y-1].piece = piece
        piece.square = self.squares[x-1][y-1]

    def get_square(self, x, y):
        for square in self.squares:
            if square.x_cords == x and square.y_cords == y:
                return square
    
    def remove_piece(self,x,y):
        self.squares[x-1][y-1].has_piece = False
        self.squares[x-1][y-1].piece = None

    def get_piece(self,code):
        for p in self.pieces:
            if code == p.code:
                return p

    def display_board(self):
        counter = 0
        for j in range(8):
            for i in range(8):
                print(" ", end="")
                if self.squares[i][7-j].has_piece:
                    print(self.squares[i][7-j].piece.icon, end="")
                else:    
                    print(f"{chr(ord('a')-1+self.squares[i][7-j].x_cords)}{self.squares[i][7-j].y_cords}", end="")
                counter+=1
                if counter ==8:
                    print("\n", end="")
                    counter =0
        print("\n")

