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

        self.square_renderer = QSvgRenderer(WHITE_SQUARE if (self.x_cords+self.y_cords)%2!=0 else BLACK_SQUARE)
        self.piece_renderer = None
        self.overlay_renderer = None # for possible moves - reset after clicking on something else for all squares

    def paintEvent(self, event):
        if self.square.has_piece and not self.square.piece.is_captured:
            self.piece_renderer = QSvgRenderer(self.square.piece.piece_path)
        else:
            self.piece_renderer = None
        self.overlay_rectangle = QRectF(self.width()*(1-OVERLAY_SCALE)/2, self.height()*(1-OVERLAY_SCALE)/2, self.width()*OVERLAY_SCALE, self.height()*OVERLAY_SCALE)
        painter = QPainter(self)
        self.square_renderer.render(painter)
        if self.piece_renderer:
            self.piece_renderer.render(painter)
        if self.overlay_renderer:
            self.overlay_renderer.render(painter, self.overlay_rectangle)


    def mousePressEvent(self, event):

        self.game.square_clicked(self.square)
        #debugging                        
        if event.button() == Qt.MouseButton.RightButton: 
            print(self.game.white_score)
            print(self.game.black_score)

        if event.button() == Qt.MouseButton.LeftButton:
            
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


        return super().mousePressEvent(event)

    def update_square_graphics(self):
        for s in self.gui_squares:
            pass

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.show()
        self.setWindowTitle("Chess")
        self.setFixedSize(QSize(660,650))

        self.game = Game()
        self.create_gui_squares()

        layout = QGridLayout()
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(0)
        for s in self.gui_squares:
            layout.addWidget(s, 8-s.y_cords, s.x_cords-1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def create_gui_squares(self):
        self.gui_squares = []
        for i in range(0,8):
            for j in range(0,8):
                self.gui_squares.append(GuiSquare(j+1,i+1,self, self.game,self.gui_squares))

    def get_gui_square(self, square):
        for g_square in self.gui_squares:
            if g_square.square == square:
                return g_square


app = QApplication([])
window = MainWindow()
app.exec()

