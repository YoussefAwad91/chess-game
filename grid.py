from pieces import *
from game import Game

BACK_ROW = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
CODES = ['r','n','b','q','k','b','n','r']


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
    pieces = []

    def __init__(self,game):
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
    
    def remove_piece(self,x,y):
        self.squares[x-1][y-1].has_piece = False
        self.squares[x-1][y-1].piece = None

    def display_board(self):
        counter = 0
        for j in range(8):
            for i in range(8):
                print(" ", end="")
                if self.squares[i][7-j].has_piece:
                    print(self.squares[i][7-j].piece.name, end="")
                else:    
                    print(f"{chr(ord('A')-1+self.squares[i][7-j].x_cords)}{self.squares[i][7-j].y_cords}", end="")
                counter+=1
                if counter ==8:
                    print("\n", end="")
                    counter =0
        print("\n")


game=Game()
board = Board(game)

#print(board.squares[0][0].piece)
#board.squares[1][0].piece.display_moves_graphical()
board.display_board()

for p in board.pieces:
    print(p.code +" ",end="")
