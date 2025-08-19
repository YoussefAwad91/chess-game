import time
from grid import Board
from pieces import Pawn

class Player:

    def __init__(self, game, color):
        self.pieces = []

        self.game = game
        self.color = color
        
        self.all_current_moves = []
        self.is_mate = False

        self.clock = PlayerClock(180,2) #user input

        for piece in self.game.board.pieces:
            if piece.color == self.color:
                self.pieces.append(piece)

    def get_all_moves(self):
        self.all_current_moves = []
        for piece in self.pieces:
            if not piece.is_captured:
                self.all_current_moves.extend(piece.final_moves())
        return self.all_current_moves
    
    def mate_or_stale(self):
        if not self.get_all_moves():
            if self.game.board.get_piece(f"{self.color[0]}_k").checked:
                self.is_mate = True
            else:
                self.game.is_stale_mate = True
        


class PlayerClock:
    def __init__(self, time_limit, increment=0):

        self.time_elapsed = 0
        self.is_running = False
        self.time_limit = time_limit
        self.last_start_time = 0
        self.remaining_time = self.time_limit
        self.increment = increment
    
    def start_time(self):
        if not self.is_running:
            self.last_start_time = time.perf_counter()
            self.is_running = True

    def stop_time(self):
        if self.is_running:
            self.time_elapsed = self.time_elapsed + time.perf_counter() - self.last_start_time
            self.remaining_time = self.time_limit - self.time_elapsed
            self.time_limit += self.increment
            self.is_running = False
    
    def get_remaining_time(self):
        if self.is_running:
            local_elapsed = time.perf_counter() - self.last_start_time
            return self.remaining_time - local_elapsed
        return self.remaining_time


class Game:

    def __init__(self):
    #def __init__(self, MainWindow):
        self.board = Board(self)
        self.white_score = 0
        self.black_score = 0 
        self.move_number = 0
        self.white_player = Player(self, "white")
        self.black_player = Player(self, "black")

        self.current_moves = []
        self.current_piece = None
        self.is_stale_mate = False
        self.promotion_piece = None

        #self.window = MainWindow #for connection between logic and top level window

    def square_clicked(self,square):

        self.get_score()

        self.get_player(self.get_player_turn()).clock.start_time()

        if square in self.current_moves: #to perform move after selecting piece and showing move overlays
            self.current_piece.square.has_piece = False
            self.current_piece.square.piece = None
            self.current_piece.move_piece(square.x_cords, square.y_cords)
            self.promotion_piece = self.current_piece
            if not isinstance(self.current_piece,Pawn):
                self.next_turn()
            else:
                if not self.current_piece.to_promote:
                    self.next_turn()

        self.current_moves = []
        self.current_piece = None
    
        #move generation
        if square.has_piece and self.get_player_turn() == square.piece.color: 
            self.current_piece = square.piece
            square.piece.final_moves()
            #self.square.piece.display_moves_matrix()
            self.current_moves = square.piece.available_squares.copy()
        
        self.board.get_piece("b_k").checked = False
        self.board.get_piece("w_k").checked = False

        if self.board.get_piece("w_k").square in self.black_player.get_all_moves():
            self.board.get_piece("w_k").checked = True

        if self.board.get_piece("b_k").square in self.white_player.get_all_moves():
            self.board.get_piece("b_k").checked = True

        self.get_player(self.get_player_turn()).mate_or_stale()
        if self.get_player(self.get_player_turn()).is_mate:
            print(self.get_player_turn() + " mated")
                  
    def next_turn(self):
        self.get_player(self.get_player_turn()).clock.stop_time()
        self.move_number+=1
        self.get_player(self.get_player_turn()).clock.start_time()

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
        return self.board.get_piece(code).final_moves()
    
    def get_player(self, color):
        if color =="white":
            return self.white_player
        else:
            return self.black_player
    
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


