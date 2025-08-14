class Square:
    x_cords = None
    y_cords = None
    has_piece = False
    piece_color = None

    def __init__(self, x, y, has_piece, piece_color):
        self.x_cords = x
        self.y_cords = y
        self.has_piece = has_piece
        self.piece_color = piece_color



class Board:
    squares = []

    def __init__(self):
        self.squares = [[Square(column, row, False, None) for row in range(1,8+1)] for column in range(1,8+1)]

    def place_piece(self, x, y, piece_color):
        self.squares[x-1][y-1].has_piece = True
        self.squares[x-1][y-1].piece_color = piece_color
    
    def remove_piece(self,x,y):
        self.squares[x-1][y-1].has_piece = False
        self.squares[x-1][y-1].piece_color = None

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
