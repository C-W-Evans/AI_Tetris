# Game constants and configuration

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 25

# Colors
BLACK = "#000000"
WHITE = "#FFFFFF"
GRAY = "#808080"
RED = "#FF0000"
YELLOW = "#FFFF00"

# Tetromino colors
COLORS = {
    "I": "#00FFFF",  # Cyan
    "J": "#0000FF",  # Blue
    "L": "#FF8000",  # Orange
    "O": "#FFFF00",  # Yellow
    "S": "#00FF00",  # Green
    "T": "#8000FF",  # Purple
    "Z": "#FF0000",  # Red
    "HEART": "#FF0000",  # Red
    "STAR": "#FFFF00",  # Yellow
}

# Alternate colors for visual change
ALT_COLORS = {
    "I": "#FF00FF",  # Magenta
    "J": "#00FFFF",  # Cyan
    "L": "#0000FF",  # Blue
    "O": "#00FF00",  # Green
    "S": "#FF8000",  # Orange
    "T": "#FF0000",  # Red
    "Z": "#8000FF",  # Purple
    "HEART": "#FF00FF",  # Magenta
    "STAR": "#00FF00",  # Green
}

# Game timing (milliseconds)
INITIAL_FALL_SPEED = 500  # Medium speed
GAME_DURATION = 5 * 60 * 1000  # 5 minutes in milliseconds
COLOR_CHANGE_INTERVAL = 2 * 60 * 1000  # 2 minutes in milliseconds
COLOR_CHANGE_DURATION = 20 * 1000  # 20 seconds in milliseconds
SPEED_BOOST_DURATION = 10 * 1000  # 10 seconds in milliseconds

# Scoring
SCORE_SINGLE = 50
SCORE_DOUBLE = 100
SCORE_TRIPLE = 200
SCORE_TETRIS = 300
SCORE_SPECIAL = 100

# Points threshold for game mechanics
SLOW_DOWN_THRESHOLD = 1000
SPECIAL_PIECE_THRESHOLD = 3000