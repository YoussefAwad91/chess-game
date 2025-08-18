#gui.py

###### image asset paths #######
WHITE_SQUARE = "assets/squares/white_square.svg"
BLACK_SQUARE = "assets/squares/black_square.svg"
OVERLAY = "assets/squares/overlay.svg"
CHECK_OVERLAY = "assets/squares/check_overlay.svg"

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

##### overlay scaling ########
OVERLAY_SCALE = 0.4


#grid.py
CODES = ['r','n','b','q','k','b','n','r'] # for giving pieces codes


#pieces.py
BISHOP_FACTORS = [ (-1,1), (-1,-1), (1,-1), (1,1)] 
ROOK_FACTORS = [(0,1), (-1,0), (0,-1), (1,0)]
KNIGHT_OFFSETS = [(1,2), (2,1), (-2,1), (2,-1), (-2,-1), (-1,-2), (1,-2), (-1,2)]
KING_OFFSETS = [(0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (1,1)]
PAWN_OFFSET = [(0,1),(0,2)]