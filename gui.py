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
            print(self.game.board.get_piece(f'{self.game.get_player_turn()[0]}_k').king_castling_moves())
           
        if event.button() == Qt.MouseButton.LeftButton:

            self.game.square_clicked(self.square)
        
            if self.square.has_piece:
                if isinstance(self.square.piece, Pawn):
                    if self.square.piece.to_promote:
                        dialog = PromotionDialog(self.window)
                        dialog.exec()
                        self.square.piece.promote_pawn(dialog.choice, self.square)
            

        self.update_gui_display()

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
    
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.setStyleSheet(WHITE_STYLESHEET if self.player.color == "white" else BLACK_STYLESHEET)
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
        self.setStyleSheet(WHITE_DIALOG_STYLESHEET if window.game.get_player_turn()=="white" else BLACK_DIALOG_STYLESHEET)
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


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.show()
        self.setWindowTitle("Chess")
        self.setFixedSize(QSize(740,650))  #for squares: width min 632, height min 624
        self.move(QPoint(X_POS,Y_POS))

        self.game = Game()
        self.create_gui_squares()

        board_layout = QGridLayout()
        board_layout.setContentsMargins(20,20,20,20)
        board_layout.setSpacing(0)
        for s in self.gui_squares:
           board_layout.addWidget(s, 8-s.y_cords, s.x_cords-1)

        clock_layout = QVBoxLayout()
        self.white_time = TimeLabel(self.game.white_player)
        self.black_time = TimeLabel(self.game.black_player)
        clock_layout.addStretch()
        clock_layout.addWidget(self.black_time)
        clock_layout.addStretch()
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


app = QApplication([])
window = MainWindow()
app.exec()
