from grid import Square
from grid import Board

BISHOP_FACTORS = [ (-1,1), (-1,-1), (1,-1), (1,1)] 
ROOK_FACTORS = [(0,1), (-1,0), (0,-1), (1,0)]
KNIGHT_OFFSETS = [(1,2), (2,1), (-2,1), (2,-1), (-2,-1), (-1,-2), (1,-2), (-1,2)]
KING_OFFSETS = [(0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (1,1)]
PAWN_OFFSET = [(0,1),(0,2)]
REVERSED_PAWN_OFFSET = [(0,-1),(0,-2)] #for black pawns - only piece where movement has certain direction


class Piece:
    VALUE = None
    square = None # Square object
    is_Captured = False
    available_squares =[]
    color = None
    board = None
    captured = False

    def __init__(self, x, y, color, board):
        self.square = board.squares[x-1][y-1] #Square object
        self.color = color
        self.board = board
        self.board.place_piece(x,y,color)

    def move_piece(self,to_x, to_y):
        for s in self.available_squares:
            if (s.x_cords==to_x and s.y_cords==to_y):
                if self.board.squares[to_x-1][to_y-1].has_piece:
                    self.board.remove_piece(self.square.x_cords, self.square.y_cords)
                    self.square = self.board.squares[to_x-1][to_y-1]
                
############## Generating moves #############
    def square_inbounds(self, x, y): #ensure moves are within board boundaries
        if(1<=x<=8) and (1<=y<=8):
            return True
        else:
            return False
        
    def get_blockable_moves(self, factors):
        self.available_squares.clear()
        for x_factor,y_factor in factors:
            for i in range (1,8):
                x_offset = i * x_factor
                y_offset = i * y_factor
                if self.square_inbounds(self.square.x_cords + x_offset, self.square.y_cords + y_offset):
                    if (self.board.squares[self.square.x_cords + x_offset - 1][self.square.y_cords + y_offset - 1]).has_piece:
                        if (self.board.squares[self.square.x_cords + x_offset - 1][self.square.y_cords + y_offset - 1]).piece_color != self.color:
                            self.available_squares.append(self.board.squares[self.square.x_cords + x_offset -1][self.square.y_cords + y_offset - 1])
                        break
                    else:
                        self.available_squares.append(self.board.squares[self.square.x_cords + x_offset -1][self.square.y_cords + y_offset - 1])
    
    def get_unblockable_moves(self, offsets):
        self.available_squares.clear()
        for dx, dy in offsets:
          if self.square_inbounds(self.square.x_cords + dx, self.square.y_cords + dy):
            if ((self.board.squares[self.square.x_cords + dx-1][self.square.y_cords + dy-1]).has_piece and (self.board.squares[self.square.x_cords + dx-1][self.square.y_cords + dy-1]).piece_color != self.color) or not(self.board.squares[self.square.x_cords + dx-1][self.square.y_cords + dy-1]).has_piece: #remove friendly squares
              self.available_squares.append(self.board.squares[self.square.x_cords + dx-1][self.square.y_cords + dy-1])
######################################

########### Display modes ###########
    def display_moves_letters(self):
        self.moves()
        for s in self.available_squares:
            print(f"{chr(ord('A')-1+s.x_cords)}{s.y_cords} ")

    def display_moves_matrix(self):
        self.moves()
        for s in self.available_squares:
            print(f"{s.x_cords}{s.y_cords} ")

    def display_moves_graphical(self):
        self.moves()
        counter = 0
        for j in range(8):
            for i in range(8):
                print(" ", end="")
                if self.board.squares[i][7-j] in self.available_squares:
                    print("O ", end="")
                elif self.board.squares[i][7-j] == self.square:
                    print(self.name, end="")
                else:
                    print(f"{chr(ord('A')-1+self.board.squares[i][7-j].x_cords)}{self.board.squares[i][7-j].y_cords}", end="")
                counter+=1
                if counter ==8:
                    print("\n", end="")
                    counter =0
###############################
        

class Knight(Piece):
    VALUE = 3
    name = "Kn"

    def moves(self):
        super().get_unblockable_moves(KNIGHT_OFFSETS)

class Bishop(Piece):
    VALUE = 3
    name = "B "

    def moves(self):
        super().get_blockable_moves(BISHOP_FACTORS)

class Rook(Piece):
    VALUE = 5
    name = "R "

    def moves(self):
        super().get_blockable_moves(ROOK_FACTORS)

class Queen(Piece):
    VALUE = 9
    name = "Q "

    def moves(self):
        super().get_blockable_moves(BISHOP_FACTORS+ROOK_FACTORS)

class King(Piece):
    VALUE = 1000000
    name = "K "

    def moves(self):
        super().get_unblockable_moves(KING_OFFSETS)

class Pawn(Piece):
    VALUE = 1
    name = "P "
    has_moved = False
    
    def moves(self):
        offset = PAWN_OFFSET if self.color == "white" else REVERSED_PAWN_OFFSET
        if self.has_moved:
            super().get_unblockable_moves(offset[:-1]) #removes second offset
        else:
            super().get_unblockable_moves(offset)

    # *self.has_moved = True after first move
    # *en passant
    # *promotion

board = Board()
#knight = Knight(5,3, "white", board)
#knight1 = Knight(5,2, "white", board)
#bishop = Bishop(3,1,"white", board)
queen = Queen(4,4,"white",board)
#rook = Rook(8,8,"black",board)
#king = King(5,1,"white",board)
#pawn = Pawn(8,7,"black",board)

#knight.display_moves_matrix()
#pawn.display_moves_matrix()
queen.display_moves_graphical()
queen.move_piece(8,8)
print("\n")
queen.display_moves_graphical()
