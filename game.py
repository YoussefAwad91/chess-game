import time #clock
from datetime import datetime #saving file with unique name
from grid import Board
from pieces import *

class Player:
    def __init__(self, game, color):
        self.pieces = []

        self.game = game
        self.color = color
        
        self.all_current_moves = []
        self.is_mate = False

        self.clock = PlayerClock() #user input

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
                self.game.game_ended = True
                self.game.end_reason = "checkmate"
                self.game.winner = "white" if self.color == "black" else "black"
            else:
                self.game.is_stale_mate = True
                self.game.game_ended = True
                self.game.end_reason = "stalemate"
                self.game.winner = "draw"

    def set_time_settings(self, time, increment):
        if time<0:
            self.game.timed = False
        else:
            self.game.timed = True
        self.clock.time_limit =time
        self.clock.increment = increment

    def get_captured_or_not(self, state): #to get captured pieces or available pieces - True gets captured
        captured_pieces = []
        for piece in self.pieces:
            if piece.is_captured == state:
                captured_pieces.append(piece)
        return captured_pieces
        
class PlayerClock:
    def __init__(self):
        self.time_elapsed = 0
        self.is_running = False
        self.time_limit = 0
        self.last_start_time = 0
        self.increment = 0
    
    def start_time(self):
        if not self.is_running:
            self.last_start_time = time.perf_counter()
            self.is_running = True

    def stop_time(self):
        if self.is_running:
            self.time_elapsed = self.time_elapsed + time.perf_counter() - self.last_start_time
            self.time_limit += self.increment
            self.is_running = False
    
    def get_remaining_time(self):
        if self.is_running:
            local_elapsed = time.perf_counter() - self.last_start_time
            return self.time_limit - self.time_elapsed - local_elapsed
        return self.time_limit - self.time_elapsed

class Game:
    def __init__(self):
    #def __init__(self, MainWindow):
        self.board = Board(self)
        self.white_score = 0
        self.black_score = 0 
        self.move_number = 0
        self.timed = None

        self.board_states = [] #saves previous FENs
        self.last_pawn_or_capture = 0
        
        self.is_stale_mate = False
        self.game_ended = False
        self.end_reason = None
        self.winner = None

        self.white_player = Player(self, "white")
        self.black_player = Player(self, "black")

        self.current_moves = []
        self.current_piece = None
        self.promotion_piece = None


    def square_clicked(self,square):

        self.get_player(self.get_player_turn()).clock.start_time()

        #to perform move after selecting piece and showing move overlays
        if square in self.current_moves: 
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

        self.get_score()

        #game state checks 
        self.threefold_draw()
        self.fiftymove_draw()
        self.material_draw()
        self.get_player(self.get_player_turn()).mate_or_stale()

        if self.game_ended:
            self.black_player.clock.stop_time()
            self.white_player.clock.stop_time()

                  
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

    def set_time_settings(self,time_limit,time_increment):
        self.white_player.set_time_settings(time_limit, time_increment)
        self.black_player.set_time_settings(time_limit, time_increment)

    def threefold_draw(self):
        draw_counter = 0
        current_state = self.board.generate_FEN()
        for state in self.board_states:
            if current_state == state:
                draw_counter+=1
        if draw_counter>=3:
            self.game_ended = True
            self.end_reason = "3repetitions"
            self.winner = "draw"
            return True
        if not self.board_states:
            self.board_states.append(current_state)
        else:
            if current_state != self.board_states[-1]:
                self.board_states.append(current_state)

        return False
    
    def fiftymove_draw(self):
        if self.move_number-self.last_pawn_or_capture>=100:
            self.game_ended = True
            self.end_reason = "50moves"
            self.winner = "draw"
            return True
        return False
    
    def material_draw(self):
        black_pieces = self.black_player.get_captured_or_not(False)
        white_pieces = self.white_player.get_captured_or_not(False)

        if len(black_pieces)>2 or len(white_pieces)>2: # more than two pieces each is not draw
            return False
        for color_list in [white_pieces, black_pieces]: # if either has rook, queen, or pawns not draw
            for piece in color_list:
                for piece_type in [Queen, Rook, Pawn]:
                    if isinstance(piece, piece_type):
                        return False
                    
        black_pieces.sort(key=lambda p:p.__class__.VALUE)
        white_pieces.sort(key=lambda p:p.__class__.VALUE)

        if black_pieces[0].__class__ != white_pieces[0].__class__: # if one has bishop and one knight then not draw -
            return False

        if isinstance(black_pieces[0], Bishop):  # ignores two knights
            if (black_pieces[0].square.x_cords +black_pieces[0].square.y_cords)%2!=(white_pieces[0].square.x_cords +(white_pieces[0].square.y_cords)%2): # two different square bishops not draw
                return False
        
        self.game_ended = True
        self.end_reason = "material"
        self.winner = "draw"
        return True

    def win_by_time(self, loser):
        self.game_ended = True
        self.end_reason = "timeout"
        self.winner = "white" if loser=="black" else "black"
        return True

    def generate_save_uci(self, save_flag):
        game_uci = ""
        board = [[0 for _ in range(0,8)] for _ in range(0,8)]
        state_number = 0
        for state in self.board_states:
            from_cords = ""
            to_cords = ""
            counter = 0
            i = 0
            for row in state.split("/"):
                j = 0
                for letter in row:
                    if counter==0:
                        try:
                            counter += int(letter)
                        except ValueError:
                            if board[i][j]!=1:
                                to_cords = f"{chr(ord('a')+j)}{8-i}"
                                board[i][j] = 1
                            j+=1                       
                    while(counter>0):
                        if board[i][j] != 0:
                            from_cords = f"{chr(ord('a')+j)}{8-i}"
                            board[i][j] = 0
                        counter-=1 
                        j+=1
                i+=1
            if state_number>0:
                game_uci += f"{from_cords}{to_cords} "
            state_number+=1

        game_uci = game_uci[:-1] #remove ending space
        if save_flag:
            timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            filename = f"game_{timestamp}.uci"

            try:
                with open(filename, "w") as file:
                    file.write(game_uci)
            except Exception as e:
                print(f"Error saving game: {e}")

        return game_uci
    
    def save_fen(self):
        full_game_fen = ""
        move_counter = 0
        for state in self.board_states:
            full_game_fen+=state + f"{" w" if move_counter%2==0 else " b" }"+ "\n" 
            move_counter+=1

        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        filename = f"game_{timestamp}.fen"

        try:
            with open(filename, "w") as file:
                file.write(full_game_fen)
        except Exception as e:
            print(f"Error saving game: {e}")

