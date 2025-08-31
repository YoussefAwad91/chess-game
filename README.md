# Chess GUI

An interactive chess game built with PyQt6 featuring a fully functional board, piece movement according to standard chess rules, timers, and game saving in FEN and UCI formats. This project is designed for both casual play and studying chess games.

---

## Features

- **Interactive Chess Board**
  - Clickable squares to select and move pieces.
  - Move highlighting and overlays for legal moves.
  - Correct handling of all piece movements, including castling, en passant, and pawn promotion.

- **Game Rules Enforcement**
  - Detects check, checkmate, and stalemate.
  - Draw detection including 50-move rule, threefold repetition, and insufficient material.
  - Automatic turn switching and move validation.

- **Timers**
  - Configurable player clocks with multiple formats.
  - Supports increments and infinite time modes.
  - Automatic time tracking and game ending on timeout.

- **Captured Pieces & Scoring**
  - Display of captured pieces for both sides.
  - Real-time score tracking based on captured pieces.

- **Pawn Promotion**
  - Choice of promotion to queen, rook, knight, or bishop via a dialog.
  
- **Saving & Exporting**
  - Save the game in FEN format.
  - Export move sequences in UCI format for later analysis.

- **User Interface**
  - Customizable SVG assets for pieces and board squares.
  - Check highlighting and visual feedback for moves.
  - Clean, responsive PyQt6 interface with consistent scaling.

- **Extensible Architecture**
  - Modular codebase separating GUI, game logic, and piece movement.
  - Easily extendable for future features like AI opponents or networked play.

---
## Project Structure

High-level overview of important files/folders:

- `assets/`          Graphics for pieces and board
- `game.py`          Core chess logic
- `grid.py`          Board and square management
- `pieces.py`        Individual piece classes and movements
- `gui.py`           PyQt6 GUI
- `constants.py`     Asset paths, stylesheets, scaling, time formats

---

## Installation

Dependencies: Python 3.x, PyQt6.

Steps to install dependencies and run the program:

```bash
pip install PyQt6
python gui.py
 ```
 
**Or run the standalone executable**

A pre-built .exe file is available, so you can play the game without installing Python or dependencies. Just double-click Chess.exe to launch the game. All features, including timers, move highlighting, and saving, work out of the box.

 ---
## How to Play

User interaction instructions:

- Select a piece by left-clicking on it to highlight legal moves.
- Move a piece by clicking on the target square.
- Pawn promotion is handled via a pop-up dialog when a pawn reaches the last rank.
- Game ends automatically on checkmate, stalemate, or draw conditions according to offical FIDE rules.
- Timers display remaining time and enforce time-based wins.
- Captured pieces and scores update dynamically.
- Save the game in FEN or UCI formats from the GUI after game ends.

---

## License

- **Project Code:** MIT License – see the [LICENSE](LICENSE/LICENSE) file for details.

- **Assets:** Creative Commons Attribution 4.0 International License – see the [LICENSE_ASSETS](LICENSE/LICENSE_ASSETS) file for details.





