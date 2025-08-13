from grid import Square
from grid import Board

class Piece:
    VALUE = None
    x_cords = None
    y_cords = None
    is_Captured = False
    available_squares =[]
    color = None
    board = None

    def __init__(self, initial_x, initial_y, color, board):
        self.x_cords = initial_x
        self.y_cords = initial_y
        self.color = color
        self.board = board

    def verify_square(self, x, y): #ensure moves are within board boundaries
        if(1<=x<=8) and (1<=y<=8):
            return True
        else:
            return False
    #def find_square(self, x, y):
     #   for 

class Knight(Piece):
    VALUE = 3
    offsets = [(1,2), (2,1), (-2,1), (2,-1), (-2,-1), (-1,-2), (-2,1), (2,-1)] #top right, top left, bottom left, bottom right

    def moves(self):
        for dx, dy in self.offsets:
          if super().verify_square(self.x_cords + dx, self.y_cords + dy):
              self.available_squares.append((self.x_cords + dx, self.y_cords + dy))

    def remove_friendly(self):
        filtered_squares = []
        for chosen_s in self.available_squares[:]:
            for all_s in self.board.squares:
                if (chosen_s[0] == all_s.x_cords) and (chosen_s[1] == all_s.y_cords):
                    if (all_s.has_Piece) and (all_s.piece_color == self.color):
                        break
            else:
                filtered_squares.append(chosen_s)
        self.available_squares = filtered_squares

class Bishop(Piece):
    VALUE = 3
    blocked = [False, False, False, False] #top right, top left, bottom left, bottom right paths

    def moves(self):
        for i in range (0,8):
            if super().verify_square(self.x_cords + i, self.y_cords + i):
                self.available_squares.append((self.x_cords + i, self.y_cords + i))

            if super().verify_square(self.x_cords - i, self.y_cords + i):
                self.available_squares.append((self.x_cords - i, self.y_cords + i))

            if super().verify_square(self.x_cords - i, self.y_cords - i):
                self.available_squares.append((self.x_cords - i, self.y_cords - i))

            if super().verify_square(self.x_cords + i, self.y_cords - i):
                self.available_squares.append((self.x_cords + i, self.y_cords - i))

    def remove_blocked(self):
        pass 
        # *remove moves with friendly pieces and moves behind enemy pieces

class Rook(Piece):
    VALUE = 5
    blocked = [False, False, False, False] #top , left, bottom, right paths

    def moves(self):
        for i in range(0,8):
            if super().verify_square(self.x_cords, self.y_cords + i):
                self.available_squares.append((self.x_cords, self.y_cords + i))

            if super().verify_square(self.x_cords - i, self.y_cords):
                self.available_squares.append((self.x_cords - i, self.y_cords))

            if super().verify_square(self.x_cords, self.y_cords - i):
                self.available_squares.append((self.x_cords, self.y_cords - i))

            if super().verify_square(self.x_cords + i, self.y_cords):
                self.available_squares.append((self.x_cords + i, self.y_cords))

    def remove_blocked(self):
        pass 
        # *remove moves with friendly pieces and moves behind enemy pieces

class Pawn(Piece):
    VALUE = 1
    has_Moved = False

    # *first move has 2 squares, en passant

class Queen(Piece):
    VALUE = 9
    blocked = [False, False, False, False, False, False, False, False] 
    #top, top left, left, bottom left, bottom, bottom right, right, top right

    def moves(self):
        for i in range(0,8):
            #linear moves
            if super().verify_square(self.x_cords, self.y_cords + i):
                self.available_squares.append((self.x_cords, self.y_cords + i))

            if super().verify_square(self.x_cords - i, self.y_cords):
                self.available_squares.append((self.x_cords - i, self.y_cords))

            if super().verify_square(self.x_cords, self.y_cords - i):
                self.available_squares.append((self.x_cords, self.y_cords - i))

            if super().verify_square(self.x_cords + i, self.y_cords):
                self.available_squares.append((self.x_cords + i, self.y_cords))

            #diagonal moves
            if super().verify_square(self.x_cords + i, self.y_cords + i):
                self.available_squares.append((self.x_cords + i, self.y_cords + i))

            if super().verify_square(self.x_cords - i, self.y_cords + i):
                self.available_squares.append((self.x_cords - i, self.y_cords + i))

            if super().verify_square(self.x_cords - i, self.y_cords - i):
                self.available_squares.append((self.x_cords - i, self.y_cords - i))

            if super().verify_square(self.x_cords + i, self.y_cords - i):
                self.available_squares.append((self.x_cords + i, self.y_cords - i))

    def remove_blocked(self):
        pass 
        # *remove moves with friendly pieces and moves behind enemy pieces


class King(Piece):
    VALUE = 1000000
    offsets = [(0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (1,1)] 
    blocked = [False, False, False, False, False, False, False, False] 
    #top, top left, left, bottom left, bottom, bottom right, right, top right

    def moves(self):
        for dx, dy in self.offsets:
          if super().verify_square(self.x_cords + dx, self.y_cords + dy):
              self.available_squares.append((self.x_cords + dx, self.y_cords + dy))

    def remove_blocked(self):
        pass 
        # *remove moves with friendly pieces

