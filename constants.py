#gui.py

###### image asset paths #######
WHITE_SQUARE = "assets/squares/white_square.svg"
BLACK_SQUARE = "assets/squares/black_square.svg"
OVERLAY = "assets/squares/overlay.svg"
CHECK_OVERLAY = "assets/squares/check_overlay.svg"
NUMBERED_SQUARE = "assets/numbered squares/"


WHITE_PAWN   = "assets/pieces/white_pawn.svg"
WHITE_ROOK   = "assets/pieces/white_rook.svg"
WHITE_KNIGHT = "assets/pieces/white_knight.svg"
WHITE_BISHOP = "assets/pieces/white_bishop.svg"
WHITE_QUEEN  = "assets/pieces/white_queen.svg"
WHITE_KING   = "assets/pieces/white_king.svg"

BLACK_PAWN   = "assets/pieces/black_pawn.svg"
BLACK_ROOK   = "assets/pieces/black_rook.svg"
BLACK_KNIGHT = "assets/pieces/black_knight.svg"
BLACK_BISHOP = "assets/pieces/black_bishop.svg"
BLACK_QUEEN  = "assets/pieces/black_queen.svg"
BLACK_KING   = "assets/pieces/black_king.svg"

BLACK_STYLESHEET = """
            QLabel {
                font-family: 'Roboto Mono', 'Consolas', monospace;
                font-size: 28px;
                font-weight: bold;
                color: #E8EDF9;
                background-color: #B7C0D8;
                border-radius: 8px;
                padding: 4px 12px;
            }
        """

WHITE_STYLESHEET = """
            QLabel {
                font-family: 'Roboto Mono', 'Consolas', monospace;
                font-size: 28px;
                font-weight: bold;
                color: #B7C0D8;
                background-color: #E8EDF9;
                border-radius: 8px;
                padding: 4px 12px;
            }
        """

WHITE_DIALOG_STYLESHEET = """
            QDialog {
                background-color: #E8EDF9;
                border-radius: 20px;   /* <--- rounded edges */
            }
            QPushButton {
                font-size: 16px;
                padding: 8px 16px;
                border-radius: 10px;
                background-color: #E8EDF9;
            }
            QPushButton:hover {
                background-color: #B7C0D8;
            }
        """

BLACK_DIALOG_STYLESHEET = """
            QDialog {
                background-color: #B7C0D8;
                border-radius: 20px;   /* <--- rounded edges */
            }
            QPushButton {
                font-size: 16px;
                padding: 8px 16px;
                border-radius: 10px;
                background-color: #B7C0D8;
            }
            QPushButton:hover {
                background-color: #E8EDF9;
            }
        """

TIME_DIALOG_STYLESHEET = """
            QDialog {
                background-color: #1e1e2f;
                border-radius: 12px;
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                background-color: #3a3a5c;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #505080;
            }
            QPushButton:pressed {
                background-color: #2a2a40;
            }
            QLineEdit, QComboBox {
                background-color: #2a2a40;
                color: white;
                font-size: 14px;
                border: 1px solid #505080;
                border-radius: 6px;
                padding: 4px;
            }
        """

##### time formats ######

TIME_FORMATS = {"1 min": (60,0), "1|1": (60,1),"2|1": (120,1),"3 min": (180,0),"3|2": (180,2),"5 min": (300,0),"10 min": (600,0),"15|10": (900,10),"30 min": (1800,0), "∞":(-1,0) }

##### scaling ########
OVERLAY_SCALE = 0.4
PIECE_SCALE = 0.95

##### window positioning ########
X_POS = 370
Y_POS = 150


#grid.py
CODES = ['r','n','b','q','k','b','n','r'] # for giving pieces codes


#pieces.py
BISHOP_FACTORS = [ (-1,1), (-1,-1), (1,-1), (1,1)] 
ROOK_FACTORS = [(0,1), (-1,0), (0,-1), (1,0)]
KNIGHT_OFFSETS = [(1,2), (2,1), (-2,1), (2,-1), (-2,-1), (-1,-2), (1,-2), (-1,2)]
KING_OFFSETS = [(0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (1,1)]
PAWN_OFFSET = [(0,1),(0,2)]