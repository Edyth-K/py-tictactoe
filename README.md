# py-tictactoe

A simple multiplayer Tic Tac Toe game built with Python and Pygame, using sockets for two-player local network play.

## 🎮 How It Works

- One player runs `server.py` to host the game.
- Two players each run their own instance of `tictactoe.py` to join the game as clients.
- Players take turns making moves by clicking on the board.
- The game automatically handles turn order and win/draw detection.

## 📦 Requirements

- Python 3
- Pygame

To install Pygame:
```bash
pip install pygame
