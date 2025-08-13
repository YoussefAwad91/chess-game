class Square:
    x_cords = None
    y_cords = None
    has_Piece = False
    piece_color = None

    def __init__(self, x, y, has_piece, piece_color):
        self.x_cords = x
        self.y_cords = y
        self.has_Piece = has_piece
        self.piece_color = piece_color



class Board:
    square = []

    def __init__(self):
        self.squares = [[Square(column, row,False, None) for column in range(1,8+1)] for row in range(1,8+1)]

    def display(self):
        for r in range(8):
            for c in range(8):
                print(f"{self.squares[c][r].x_cords}{self.squares[c][r].y_cords} ")
            print("\n")


board = Board()
board.display()