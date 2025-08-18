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