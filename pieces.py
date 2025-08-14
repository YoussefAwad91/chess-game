#from grid import Square
#from grid import Board
#from game import Game

__all__ = ["Pawn", "Knight","Rook", "Bishop", "Queen", "King"]

# !only change turn if move goes through
# !count moves


BISHOP_FACTORS = [ (-1,1), (-1,-1), (1,-1), (1,1)] 
ROOK_FACTORS = [(0,1), (-1,0), (0,-1), (1,0)]
KNIGHT_OFFSETS = [(1,2), (2,1), (-2,1), (2,-1), (-2,-1), (-1,-2), (1,-2), (-1,2)]
KING_OFFSETS = [(0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (1,1)]
PAWN_OFFSET = [(0,1),(0,2)]
REVERSED_PAWN_OFFSET = [(0,-1),(0,-2)] #for black pawns - only piece where movement has certain direction


class Piece:
    VALUE = None
    square = None # Square object
    available_squares =[]
    color = None
    board = None
    is_captured = False
    code = None #to be able to reference indivdual pieces without position

    def __init__(self, x, y, color, board, game, code):
        self.square = board.squares[x-1][y-1] #Square object
        self.color = color
        self.board = board
        self.board.place_piece(x,y,self)
        self.game = game
        self.code = code

    def move_piece(self,to_x, to_y): #with capturing funcitonality
        for s in self.available_squares:
            if (s.x_cords==to_x and s.y_cords==to_y):
                self.board.remove_piece(self.square.x_cords, self.square.y_cords) #removing piece to be moved from intial sqaure
                self.square = self.board.squares[to_x-1][to_y-1] #moving piece to new square
                if self.board.squares[to_x-1][to_y-1].has_piece:
                    self.square.piece.is_captured = True
                    self.square.piece.square = None
                    # *add score **score += self.square.piece.VALUE
                self.board.place_piece(to_x,to_y,self)
                return True
        return False #if piece didnt move
                
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
                        if (self.board.squares[self.square.x_cords + x_offset - 1][self.square.y_cords + y_offset - 1]).piece.color != self.color:
                            self.available_squares.append(self.board.squares[self.square.x_cords + x_offset -1][self.square.y_cords + y_offset - 1])
                        break
                    else:
                        self.available_squares.append(self.board.squares[self.square.x_cords + x_offset -1][self.square.y_cords + y_offset - 1])
    
    def get_unblockable_moves(self, offsets):
        self.available_squares.clear()
        for dx, dy in offsets:
          if self.square_inbounds(self.square.x_cords + dx, self.square.y_cords + dy):
            if ((self.board.squares[self.square.x_cords + dx-1][self.square.y_cords + dy-1]).has_piece and (self.board.squares[self.square.x_cords + dx-1][self.square.y_cords + dy-1]).piece.color != self.color) or not(self.board.squares[self.square.x_cords + dx-1][self.square.y_cords + dy-1]).has_piece: #remove friendly squares
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
                elif self.board.squares[i][7-j].has_piece:
                    print(self.board.squares[i][7-j].piece.name, end="")
                else:    
                    print(f"{chr(ord('A')-1+self.board.squares[i][7-j].x_cords)}{self.board.squares[i][7-j].y_cords}", end="")
                counter+=1
                if counter ==8:
                    print("\n", end="")
                    counter =0
        print("\n")
###############################
        

class Knight(Piece):
    VALUE = 3
    name = "Kn" #only for display purposes

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
    promoted_piece = None
    first_move = 0
    orientation = None
    enpassant_move = (0,0)

    def __init__(self, x, y, color, board, game,code):
        super().__init__(x, y, color, board, game,code)
        self.orientation = 1 if color == "white" else -1  #board orientation for black vs white movement

    def pawn_capturing_moves(self, direction): #1 for right and -1 for left
        if (self.board.squares[self.square.x_cords+direction-1][self.square.y_cords+1*self.orientation-1].has_piece) and (self.board.squares[self.square.x_cords+direction-1][self.square.y_cords+1*self.orientation-1].piece.color != self.color):
            self.available_squares.append(self.board.squares[self.square.x_cords+direction-1][self.square.y_cords+1*self.orientation-1]) #normal capture
        elif (self.board.squares[self.square.x_cords+direction-1][self.square.y_cords-1].has_piece) and (self.board.squares[self.square.x_cords+direction-1][self.square.y_cords-1].piece.color != self.color):
            if self.square.y_cords == (5 if self.orientation else 4): #enpassant capture
                if isinstance(self.board.squares[self.square.x_cords+direction-1][self.square.y_cords-1].piece, Pawn):
                    if (self.board.squares[self.square.x_cords+direction-1][self.square.y_cords-1]).piece.first_move==self.game.move_number:
                        self.available_squares.append(self.board.squares[self.square.x_cords+direction-1][self.square.y_cords+1*self.orientation-1])
                        self.enpassant_move = (self.square.x_cords+direction,self.square.y_cords+1*self.orientation)
        # if y==5 or y==4 for black and pawn that just moved to right or left can capture enpassant



    def moves(self):
        self.orientation
        self.available_squares.clear()
        for x_offset,y_offset in (PAWN_OFFSET if not self.has_moved else PAWN_OFFSET[:-1]):
            if self.square_inbounds(self.square.x_cords + x_offset, self.square.y_cords + y_offset*self.orientation):
                if (self.board.squares[self.square.x_cords + x_offset - 1][self.square.y_cords + y_offset*self.orientation - 1]).has_piece:
                    if (self.board.squares[self.square.x_cords + x_offset - 1][self.square.y_cords + y_offset - 1]).piece.color != self.color:
                        self.available_squares.append(self.board.squares[self.square.x_cords + x_offset -1][self.square.y_cords + y_offset - 1])
                    break
                else:
                    self.available_squares.append(self.board.squares[self.square.x_cords + x_offset -1][self.square.y_cords + y_offset - 1])
        self.enpassant_move = (0,0)
        self.pawn_capturing_moves(1)
        self.pawn_capturing_moves(-1)


        

    def move_piece(self, to_x, to_y):
        if super().move_piece(to_x, to_y):
            if not self.has_moved:
                self.first_move = self.game.move_number
                self.has_moved = True
            elif self.square.y_cords == 8:
                self.board.remove_piece(self.square.x_cords, 8)
                # *create new promoted piece object - set as queen for now
                self.promoted_piece = Queen(self.square.x_cords, 8, self.color, board)
                self.board.place_piece(self.square.x_cords, 8, self.promoted_piece)
            elif self.enpassant_move == (to_x, to_y):
                self.board.squares[to_x-1][to_y-self.orientation-1].piece.is_captured = True
                self.board.squares[to_x-1][to_y-self.orientation-1].piece.square = None
                self.board.remove_piece(to_x, to_y - self.orientation)
    # *promotion
