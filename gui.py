from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtSvg import * 

from constants import *
from game import *

class GuiSquare(QWidget):
    def __init__(self, x_cords, y_cords,window, game, gui_squares):
        super().__init__()
        self.window = window

        self.x_cords = x_cords
        self.y_cords = y_cords

        self.game = game
        self.square = self.game.board.squares[self.x_cords-1][self.y_cords-1]
        self.gui_squares = gui_squares

        if self.x_cords==1 or self.y_cords ==1:
            self.square_renderer = QSvgRenderer(f"{NUMBERED_SQUARE}{chr(ord('a')+self.x_cords-1)}{self.y_cords}.svg")
        else:
            self.square_renderer = QSvgRenderer(WHITE_SQUARE if (self.x_cords+self.y_cords)%2!=0 else BLACK_SQUARE)

        self.piece_renderer = None
        self.overlay_renderer = None # for possible moves - reset after clicking on something else for all squares

    def paintEvent(self, event):
        if self.square.has_piece and not self.square.piece.is_captured:
            self.piece_renderer = QSvgRenderer(self.square.piece.piece_path)
        else:
            self.piece_renderer = None

        self.square_rectangle = QRectF(0,0,79,78)
        self.overlay_rectangle = QRectF(self.width()*(1-OVERLAY_SCALE)/2, self.height()*(1-OVERLAY_SCALE)/2, self.width()*OVERLAY_SCALE, self.height()*OVERLAY_SCALE)
        self.piece_rectangle = QRectF(self.width()*(1-PIECE_SCALE)/2, self.height()*(1-PIECE_SCALE)/2, self.width()*PIECE_SCALE, self.height()*PIECE_SCALE)

        painter = QPainter(self)

        self.square_renderer.render(painter, self.square_rectangle)
        if self.piece_renderer:
            self.piece_renderer.render(painter, self.piece_rectangle)
        if self.overlay_renderer:
            self.overlay_renderer.render(painter, self.overlay_rectangle)


    def mousePressEvent(self, event):

        #debugging                        
        if event.button() == Qt.MouseButton.RightButton: 
            pass

        if event.button() == Qt.MouseButton.LeftButton:

            self.game.square_clicked(self.square)
            if self.square.has_piece:
                if isinstance(self.square.piece, Pawn):
                    if self.square.piece.to_promote:
                        dialog = PromotionDialog(self.window)
                        dialog.exec()
                        self.square.piece.promote_pawn(dialog.choice, self.square)
            
            self.window.captured_score_label.update_score()
            self.update_gui_display()
            self.window.check_end_game()


        return super().mousePressEvent(event)
    
    def update_gui_display(self):
        #board clear
        for s in self.gui_squares: 
            s.overlay_renderer = None
            s.update()

        #overlay
        if self.square.has_piece and self.game.get_player_turn() == self.square.piece.color: 
            for s in self.gui_squares:
                if s.square in self.square.piece.available_squares:
                    s.overlay_renderer = QSvgRenderer(OVERLAY)
                    s.update()

        if self.game.board.get_piece("w_k").checked:
            self.window.get_gui_square(self.game.board.get_piece("w_k").square).overlay_renderer = QSvgRenderer(CHECK_OVERLAY)
            self.window.get_gui_square(self.game.board.get_piece("w_k").square).update()

        if self.game.board.get_piece("b_k").checked:
            self.window.get_gui_square(self.game.board.get_piece("b_k").square).overlay_renderer = QSvgRenderer(CHECK_OVERLAY)
            self.window.get_gui_square(self.game.board.get_piece("b_k").square).update()

class TimeLabel(QLabel):
    
    def __init__(self, player,window):
        super().__init__()
        self.player = player
        self.window = window
        self.setStyleSheet(WHITE_TIME_STYLESHEET if self.player.color == "white" else BLACK_TIME_STYLESHEET)
        self.setTextFormat(Qt.TextFormat.RichText)
        self.setContentsMargins(0,0,0,0)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAutoFillBackground(True)

        self.timer = QTimer() # timer acts as a poller
        self.timer.timeout.connect(self.set_current_time)
        self.timer.start(500) #refresh rate = 500ms

    def set_current_time(self):
        if self.player.game.timed == False:
            self.setText("∞")
        else:
            current_time_seconds = self.player.clock.get_remaining_time()
            if current_time_seconds<0:
                self.player.game.win_by_time(self.player.game.get_player_turn())
                self.window.check_end_game()

            hours, remainder = divmod(current_time_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            seconds = int(seconds)
            minutes = int(minutes)
            hours = int(hours)
            if hours>0:
                self.setText(f"{hours}:{minutes if minutes>9 else f"0{minutes}"}:{seconds if seconds>9 else f"0{seconds}"}")
            else:
                self.setText(f"{minutes if minutes>9 else f"0{minutes}"}:{seconds if seconds>9 else f"0{seconds}"}")
            return (hours,minutes,seconds)

class PromotionDialog(QDialog):
    pieces = ["rook", "queen", "knight", "bishop"]
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.choice = None
        self.setStyleSheet(WHITE_PROMOTION_STYLESHEET if window.game.get_player_turn()=="white" else BLACK_PROMOTION_STYLESHEET)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setFixedSize((QSize(300,90)))
        self.setModal(True)
        
        button_layout = QHBoxLayout()
        self.move(QPoint((X_POS-140)+self.window.game.promotion_piece.square.x_cords*70,Y_POS+(132 if window.game.get_player_turn()=="white" else 486)))
        
        for piece in self.pieces:
            button = QPushButton()
            button.setIcon(QIcon(f"assets/pieces/{window.game.get_player_turn()}_{piece}.svg"))
            button.setIconSize(QSize(60,60))
            button.setFixedSize(QSize(70,70))         
            button.clicked.connect(lambda checked, p=piece: self.select_promotion(p))

            button_layout.addWidget(button)
        self.setLayout(button_layout)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()
            return
        return super().keyPressEvent(event)

    def select_promotion(self,piece):
        self.choice = piece
        self.window.game.next_turn()
        self.accept()
                
class TimeFormatDialog(QDialog):
    def __init__(self, window):
        super().__init__()

        self.window = window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setFixedSize((QSize(400,320)))
        self.setModal(True)
        self.move(530,335)

        button_layout = QGridLayout()

        x_counter = 0
        y_counter = 0
        
        for time_f in TIME_FORMATS:
            time_limit = TIME_FORMATS[time_f][0]
            increment = TIME_FORMATS[time_f][1]
            button = QPushButton()
            button.setStyleSheet(TIME_DIALOG_STYLESHEET)
            button.setText(time_f)
            button.clicked.connect(lambda checked, t=time_limit, i=increment: self.set_time_settings(t,i))

            button_layout.addWidget(button,y_counter,x_counter)
            x_counter+=1
            if x_counter>2:
                x_counter = 0
                y_counter+=1
            if y_counter>2:
                x_counter =1

        self.setLayout(button_layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()
            return
        return super().keyPressEvent(event)
    

    def set_time_settings(self,t,i):
        self.window.game.set_time_settings(t,i)
        self.accept()
        self.window.white_time.set_current_time()
        self.window.black_time.set_current_time()

class CapturedPiecesLabel(QLabel):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.update_score()
        self.setStyleSheet(CAPTURED_SCORE_STYLESHEET)
    
    def get_captured_string(self, player):
        captured_pieces_str = ""
        for piece in player.get_captured_or_not(True):
            captured_pieces_str+=piece.icon
        return captured_pieces_str
    
    def update_score(self):
        score = self.window.game.white_score - self.window.game.black_score
        black_captured_text = self.get_captured_string(self.window.game.white_player) + ("+"+str(abs(score)) if score<0 else "" )
        white_captured_text = self.get_captured_string(self.window.game.black_player) + ("+"+str(score) if score>0 else "" )
        self.setText(f"""
                    <span style="color:#B7C0D8;">{black_captured_text}</span>
                    <br>
                    <span style="color:#E8EDF9;">{white_captured_text}</span>
                    """)

class EndDialog(QDialog):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setFixedSize((QSize(400,180)))
        self.setModal(True)
        self.setStyleSheet(END_DIALOG_STYLESHEET)

        master_layout = QVBoxLayout()
        self.end_message_label = QLabel()
        button_layout = QHBoxLayout()

        save_pgn_button = QPushButton()
        leave_button = QPushButton()

        save_pgn_button.setText("Save Game")
        leave_button.setText("Leave")

        button_layout.addWidget(save_pgn_button)
        button_layout.addWidget(leave_button)

        save_pgn_button.clicked.connect(lambda: self.end_with_setting(True))
        leave_button.clicked.connect(lambda: self.end_with_setting(False))
        
        master_layout.addWidget(self.end_message_label)
        master_layout.addStretch()
        master_layout.addLayout(button_layout)
        master_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        master_layout.setContentsMargins(20,40,20,40)

        self.setLayout(master_layout)

    def set_text(self, reason, winner):
        text = ""
        if reason=="checkmate":
            text = f"{winner.capitalize()} won by checkmate!"
        elif reason=="timeout":
            text = f"{winner.capitalize()} won by timeout!"
        elif winner == "draw":
            if reason == "stalemate":
                text = "Draw by stalemate"
            elif reason == "50moves":
                text = "Draw by 50 move rule"
            elif reason == "3repetitions":
                text = "Draw by 3-fold repetiton"
            elif reason == "material":
                text = "Draw by insufficient material"
        self.end_message_label.setText(text)
    
    def end_with_setting(self, save_flag):
        if save_flag:
            self.window.game.generate_save_uci(True)
            self.window.game.save_fen()
        self.accept()
        self.window.close()
        return True

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.show()
        self.setWindowTitle("Chess")
        self.setFixedSize(QSize(810,650))  #for squares: width min 632, height min 624
        self.move(QPoint(X_POS,Y_POS))

        self.game = Game()
        self.create_gui_squares()

        board_layout = QGridLayout()
        board_layout.setContentsMargins(20,20,20,20)
        board_layout.setSpacing(0)
        for s in self.gui_squares:
           board_layout.addWidget(s, 8-s.y_cords, s.x_cords-1)

        clock_layout = QVBoxLayout()
        self.white_time = TimeLabel(self.game.white_player, self)
        self.black_time = TimeLabel(self.game.black_player, self)
        self.captured_score_label = CapturedPiecesLabel(self)
        clock_layout.addStretch()
        clock_layout.addWidget(self.black_time)
        clock_layout.addWidget(self.captured_score_label)
        #clock_layout.addStretch()
        clock_layout.addWidget(self.white_time)
        clock_layout.addStretch()

        main_layout = QHBoxLayout()
        main_layout.addLayout(board_layout, stretch=32)
        main_layout.addLayout(clock_layout, stretch=5)
        main_layout.setSpacing(0)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        time_dialog = TimeFormatDialog(self)
        time_dialog.exec()

        self.end_dialog = EndDialog(self)

    def create_gui_squares(self):
        self.gui_squares = []
        for i in range(0,8):
            for j in range(0,8):
                self.gui_squares.append(GuiSquare(j+1,i+1,self, self.game,self.gui_squares))

    def get_gui_square(self, square):
        for g_square in self.gui_squares:
            if g_square.square == square:
                return g_square
            
    def get_gui_square_cords(self, x, y):
        for g_square in self.gui_squares:
            if g_square.x_cords == x and g_square.y_cords:
                return g_square
            
    def check_end_game(self):
        if self.game.game_ended:
            self.end_dialog.set_text(self.game.end_reason, self.game.winner)
            self.end_dialog.exec()
            
if __name__=="__main__":

    app = QApplication([])
    window = MainWindow()
    app.exec()
