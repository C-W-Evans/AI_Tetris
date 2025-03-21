# AI Tetris Battle

A two-player Tetris game where you compete against an AI opponent. The game features special mechanics like penalty pieces, color changes, and special pieces when reaching high scores.

## Prerequisites

- Python 3.6 or higher
- tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-tetris-battle.git
cd ai-tetris-battle
```

2. No additional package installation is required as the game uses only Python's built-in libraries.

## How to Play

1. Start the game by running:
```bash
python main.py
```

2. Game Controls:
   - Left Arrow: Move piece left
   - Right Arrow: Move piece right
   - Down Arrow: Move piece down faster
   - Up Arrow: Rotate piece
   - Space: Hard drop (instantly drop piece) Only possible for human player.
   - Escape: Quit game

3. Game Features:
   - Compete against an AI opponent
   - Clear two lines at once to send a penalty piece to your opponent
   - Every 2 minutes, the game enters "RAINBOW MODE!!!" for 20 seconds
   - First player to reach 5000 points wins
   - Game ends if either player's grid becomes full

4. Scoring:
   - 100 points per line cleared
   - 300 points for clearing two lines at once
   - 500 points for clearing three lines at once
   - 800 points for clearing four lines at once (Tetris)

## Project Structure

```
ai-tetris-battle/
├── main.py          # Entry point of the game
├── game.py          # Main game logic
├── player.py        # Player class and controls
├── ai.py           # AI opponent logic
├── grid.py         # Game grid implementation
├── tetromino.py    # Tetromino piece definitions
└── constants.py    # Game constants and settings
```

## Game Rules

1. Each player has their own grid
2. Pieces fall automatically
3. Clearing two lines at once sends a penalty piece to your opponent
4. The game alternates between normal and rainbow colors every 2 minutes
5. First to 5000 points or last player standing wins

## Troubleshooting

If you encounter any issues:

1. Make sure you're using Python 3.6 or higher
2. Verify that tkinter is installed (it comes with standard Python installations)
3. Check that all files are in the same directory
4. Ensure you're running the game from the project directory

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 