from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtSvg import *

from constants import *

class GuiSquare(QWidget):
    def __init__(self, path, x_cords, y_cords):
        super().__init__()

        self.renderer = QSvgRenderer(path)

        self.x_cords = x_cords
        self.y_cords = y_cords
    
    def paintEvent(self, event):
        painter = QPainter(self)
        self.renderer.render(painter)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.show()
        self.setWindowTitle("Chess")
        self.setFixedSize(QSize(660,650))

        layout = QGridLayout()
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(0)

        self.create_gui_squares()

        for s in self.gui_squares:
            layout.addWidget(s, 8-s.y_cords, s.x_cords-1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def create_gui_squares(self):
        self.gui_squares = []

        for i in range(0,8):
            for j in range(0,8):
                self.gui_squares.append(GuiSquare(WHITE_SQUARE if (i+j)%2!=0 else BLACK_SQUARE, j+1,i+1))

app = QApplication([])

window = MainWindow()


app.exec()

"""
graphic object and add square self.variable to connect with code. 
click on object calls square.piece.moves() which is then displayed on board
graphic object will have piece image passed depending on piece on it
numbered squares on edge

"""