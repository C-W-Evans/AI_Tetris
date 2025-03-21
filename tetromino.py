import random
from constants import COLORS, ALT_COLORS, GRID_WIDTH

# Tetromino shapes represented as matrices
SHAPES = {
    "I": [
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        
        [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0]],
        
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0]],
        
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]]
    ],
    "J": [
        [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],
        
        [[0, 1, 1],
         [0, 1, 0],
         [0, 1, 0]],
        
        [[0, 0, 0],
         [1, 1, 1],
         [0, 0, 1]],
        
        [[0, 1, 0],
         [0, 1, 0],
         [1, 1, 0]]
    ],
    "L": [
        [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],
        
        [[0, 1, 0],
         [0, 1, 0],
         [0, 1, 1]],
        
        [[0, 0, 0],
         [1, 1, 1],
         [1, 0, 0]],
        
        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 0]]
    ],
    "O": [
        [[0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]]
    ],
    "S": [
        [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],
        
        [[0, 1, 0],
         [0, 1, 1],
         [0, 0, 1]],
        
        [[0, 0, 0],
         [0, 1, 1],
         [1, 1, 0]],
        
        [[1, 0, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ],
    "T": [
        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],
        
        [[0, 1, 0],
         [0, 1, 1],
         [0, 1, 0]],
        
        [[0, 0, 0],
         [1, 1, 1],
         [0, 1, 0]],
        
        [[0, 1, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ],
    "Z": [
        [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],
        
        [[0, 0, 1],
         [0, 1, 1],
         [0, 1, 0]],
        
        [[0, 0, 0],
         [1, 1, 0],
         [0, 1, 1]],
        
        [[0, 1, 0],
         [1, 1, 0],
         [1, 0, 0]]
    ],
    "HEART": [
        [[0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]]
    ],
    "STAR": [
        [[0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]]
    ]
}

class Tetromino:
    def __init__(self, shape_name=None):
        if shape_name:
            self.shape_name = shape_name
        else:
            # Standard pieces with higher probability
            regular_shapes = ["I", "J", "L", "O", "S", "T", "Z"]
            self.shape_name = random.choice(regular_shapes)
        
        self.shape = SHAPES[self.shape_name]
        self.rotation = 0
        self.x = GRID_WIDTH // 2 - len(self.shape[0][0]) // 2
        self.y = 0
        self.color = COLORS[self.shape_name]
        self.alt_color = ALT_COLORS[self.shape_name]
        self.using_alt_color = False
        
    def get_current_shape(self):
        return self.shape[self.rotation]
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)
        
    def get_color(self):
        """Get the current color based on whether using alternate colors"""
        return self.alt_color if self.using_alt_color else self.color
        
    def toggle_color(self, use_alt):
        """Toggle between normal and alternate colors"""
        self.using_alt_color = use_alt
        self.color = COLORS[self.shape_name]
        self.alt_color = ALT_COLORS[self.shape_name]

    def get_positions(self):
        """Returns list of (x, y) positions of all blocks in the tetromino"""
        positions = []
        shape = self.get_current_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    positions.append((self.x + x, self.y + y))
        return positions
    
    @staticmethod
    def get_penalty_piece():
        """Returns either a square or straight line as penalty piece"""
        return Tetromino(random.choice(["O", "I"]))
    
    @staticmethod
    def get_special_piece():
        """Returns either a heart or star special piece"""
        return Tetromino(random.choice(["HEART", "STAR"]))