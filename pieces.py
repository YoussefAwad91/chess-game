from constants import *
import copy

__all__ = ["Pawn", "Knight","Rook", "Bishop", "Queen", "King"]

class Piece:  

    def __init__(self, x, y, color, board, game, code):
        self.square = board.squares[x-1][y-1] #Square object
        self.color = color
        self.board = board
        self.board.place_piece(x,y,self)
        self.game = game
        self.code = code #to be able to reference indivdual pieces without position
        self.is_captured = False
        self.available_squares =[]


    def move_piece(self,to_x, to_y): #with capturing funcitonality
        for s in self.available_squares:
            if (s.x_cords==to_x and s.y_cords==to_y):
                self.board.remove_piece(self.square.x_cords, self.square.y_cords) #removing piece to be moved from intial sqaure
                self.square = self.board.squares[to_x-1][to_y-1] #moving piece to new square
                if self.board.squares[to_x-1][to_y-1].has_piece:
                    self.square.piece.is_captured = True
                    self.square.piece.square = None
                    # todo: add score **score += self.square.piece.VALUE
                self.board.place_piece(to_x,to_y,self)
                return True
        return False #if piece didnt move
                
############## Generating moves #############

    def final_moves(self):
        self.initial_moves()
        if not self.board.virtual:
            self.remove_checked_moves()
        return self.available_squares

    def remove_checked_moves(self):
        new_available_squares = []
        for square in self.available_squares:
            virtual_board = copy.deepcopy(self.board)
            virtual_board.virtual = True
            virtual_board.get_piece(self.code).final_moves()
            virtual_board.get_piece(self.code).move_piece(square.x_cords, square.y_cords)
            #virtual_board.display_board()
            if self.color == "white":
                if virtual_board.get_piece("w_k").square not in virtual_board.game.black_player.get_all_moves():
                    new_available_squares.append(square)
            else:
                if virtual_board.get_piece("b_k").square not in virtual_board.game.white_player.get_all_moves():
                    new_available_squares.append(square)

            del virtual_board
        #print("1", self.available_squares)
        #print("2", new_available_squares)
        #print("\n")
        self.available_squares = new_available_squares 
        return self.available_squares


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
        self.final_moves()
        for s in self.available_squares:
            print(f"{chr(ord('A')-1+s.x_cords)}{s.y_cords} ")

    def display_moves_matrix(self):
        self.final_moves()
        for s in self.available_squares:
            print(f"{s.x_cords}{s.y_cords} ")

    def display_moves_graphical(self):
        self.final_moves()
        counter = 0
        for j in range(8):
            for i in range(8):
                print(" ", end="")
                if self.board.squares[i][7-j] in self.available_squares:
                    print("● ", end="")
                elif self.board.squares[i][7-j].has_piece:
                    print(self.board.squares[i][7-j].piece.icon, end="")
                else:    
                    print(f"{chr(ord('a')-1+self.board.squares[i][7-j].x_cords)}{self.board.squares[i][7-j].y_cords}", end="")
                counter+=1
                if counter ==8:
                    print("\n", end="")
                    counter =0
        print("\n")
###############################
        

class Knight(Piece):
    VALUE = 3

    def __init__(self, x, y, color, board, game,code):
        super().__init__(x, y, color, board, game,code)
        self.icon = "♘ " if color == "white" else "♞ "
        self.piece_path = WHITE_KNIGHT if color == "white" else BLACK_KNIGHT

    def initial_moves(self):
        super().get_unblockable_moves(KNIGHT_OFFSETS)
        return self.available_squares

class Bishop(Piece):
    VALUE = 3

    def __init__(self, x, y, color, board, game,code):
        super().__init__(x, y, color, board, game,code)
        self.icon = "♗ " if color == "white" else "♝ "
        self.piece_path = WHITE_BISHOP if color == "white" else BLACK_BISHOP

    def initial_moves(self):
        super().get_blockable_moves(BISHOP_FACTORS)
        return self.available_squares

class Rook(Piece):
    VALUE = 5

    def __init__(self, x, y, color, board, game,code):
        super().__init__(x, y, color, board, game,code)
        self.icon = "♖ " if color == "white" else "♜ "
        self.piece_path = WHITE_ROOK if color == "white" else BLACK_ROOK
        self.has_moved = False

    def initial_moves(self):
        super().get_blockable_moves(ROOK_FACTORS)
        return self.available_squares

class Queen(Piece):
    VALUE = 9

    def __init__(self, x, y, color, board, game,code):
        super().__init__(x, y, color, board, game,code)
        self.icon = "♕ " if color == "white" else "♛ "
        self.piece_path = WHITE_QUEEN if color == "white" else BLACK_QUEEN

    def initial_moves(self):
        super().get_blockable_moves(BISHOP_FACTORS+ROOK_FACTORS)
        return self.available_squares

class King(Piece):
    VALUE = 1000000

    def __init__(self, x, y, color, board, game,code):
        super().__init__(x, y, color, board, game,code)
        self.icon = "♔ " if color == "white" else "♚ "
        self.piece_path = WHITE_KING if color == "white" else BLACK_KING
        self.checked = False
        self.has_moved = False

    def initial_moves(self):
        super().get_unblockable_moves(KING_OFFSETS)
        return self.available_squares
        # todo: castling

class Pawn(Piece):
    VALUE = 1
    PROMOTION_PIECES = {"queen": Queen, "knight": Knight, "bishop": Bishop, "rook": Rook}

    
    def __init__(self, x, y, color, board, game,code):
        super().__init__(x, y, color, board, game,code)
        self.icon = "♙ " if self.color == "white" else "♟ "
        self.piece_path = WHITE_PAWN if color == "white" else BLACK_PAWN

        self.orientation = 1 if color == "white" else -1  #board orientation for black vs white movement
        self.has_moved = False
        self.promoted_piece = None
        self.first_move = 0
        self.enpassant_move = (0,0)
        self.to_promote = False

    def pawn_capturing_moves(self, direction): #1 for right and -1 for left
        if self.square_inbounds(self.square.x_cords+direction,self.square.y_cords+self.orientation):
            if (self.board.squares[self.square.x_cords+direction-1][self.square.y_cords+self.orientation-1].has_piece) and (self.board.squares[self.square.x_cords+direction-1][self.square.y_cords+self.orientation-1].piece.color != self.color):
                self.available_squares.append(self.board.squares[self.square.x_cords+direction-1][self.square.y_cords+self.orientation-1]) #normal capture
                return
        
        if self.square.y_cords == (5 if self.color == "white" else 4): #enpassant capture
            if self.square_inbounds(self.square.x_cords+direction, self.square.y_cords + self.orientation):
                if (self.board.squares[self.square.x_cords+direction-1][self.square.y_cords-1].has_piece) and (self.board.squares[self.square.x_cords+direction-1][self.square.y_cords-1].piece.color != self.color):
                    if isinstance(self.board.squares[self.square.x_cords+direction-1][self.square.y_cords-1].piece, Pawn):
                        if (self.board.squares[self.square.x_cords+direction-1][self.square.y_cords-1]).piece.first_move==self.game.move_number-1:
                            self.available_squares.append(self.board.squares[self.square.x_cords+direction-1][self.square.y_cords+self.orientation-1])
                            self.enpassant_move = (self.square.x_cords+direction,self.square.y_cords+self.orientation)
            # if y==5 or y==4 for black and pawn that just moved to right or left can capture enpassant

    def initial_moves(self):
        #self.orientation
        self.available_squares.clear()
        for x_offset,y_offset in (PAWN_OFFSET if not self.has_moved else PAWN_OFFSET[:-1]):
            if self.square_inbounds(self.square.x_cords + x_offset, self.square.y_cords + y_offset*self.orientation):
                if not (self.board.squares[self.square.x_cords + x_offset - 1][self.square.y_cords + y_offset*self.orientation - 1]).has_piece:
                    self.available_squares.append(self.board.squares[self.square.x_cords + x_offset -1][self.square.y_cords + y_offset*self.orientation - 1])
                else:
                    break
        self.enpassant_move = (0,0)
        self.pawn_capturing_moves(1)
        self.pawn_capturing_moves(-1)
        return self.available_squares


        

    def move_piece(self, to_x, to_y):
        if super().move_piece(to_x, to_y):
            if not self.has_moved:
                self.first_move = self.game.move_number
                self.has_moved = True
            elif self.square.y_cords == (8 if self.color == "white" else 1):
                self.to_promote = True
                """ self.board.remove_piece(self.square.x_cords, 8)
                # todo: create new promoted piece object - set as queen for now
                # todo: update pieces list to remove pawn and add queen
                self.promoted_piece = Queen(self.square.x_cords, 8, self.color, self.board,self.game, f"{self.color[0]}_q_2")
                self.board.place_piece(self.square.x_cords, 8, self.promoted_piece) """
            elif self.enpassant_move == (to_x, to_y):
                self.board.squares[to_x-1][to_y-self.orientation-1].piece.is_captured = True
                self.board.squares[to_x-1][to_y-self.orientation-1].piece.square = None
                self.board.remove_piece(to_x, to_y - self.orientation)
    
    def promote_pawn(self, piece, square):
        self.board.remove_piece(self.square.x_cords, (8 if self.color == "white" else 1))
        self.promoted_piece = self.PROMOTION_PIECES[piece](self.square.x_cords, (8 if self.color == "white" else 1), self.color, self.board,self.game, f"{self.color[0]}_{piece[0] if piece!="knight" else piece[1]}_promote")
        self.board.place_piece(self.square.x_cords, (8 if self.color == "white" else 1), self.promoted_piece)
        self.board.pieces.append(self.promoted_piece)
        self.board.game.get_player(self.color).pieces.append(self.promoted_piece)
        self.to_promote = False
        self.game.square_clicked(square) #rerun click to calculate king condition (check, checkmate, etc)
