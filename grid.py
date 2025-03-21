import tkinter as tk
from constants import GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE, WHITE, GRAY, BLACK

class Grid:
    def __init__(self, canvas, x_offset=0, y_offset=0):
        self.canvas = canvas
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.draw_grid_lines()
        
    def draw_grid_lines(self):
        """Draw the grid background lines"""
        for x in range(GRID_WIDTH + 1):
            self.canvas.create_line(
                self.x_offset + x * BLOCK_SIZE, self.y_offset,
                self.x_offset + x * BLOCK_SIZE, self.y_offset + GRID_HEIGHT * BLOCK_SIZE,
                fill=GRAY
            )
        
        for y in range(GRID_HEIGHT + 1):
            self.canvas.create_line(
                self.x_offset, self.y_offset + y * BLOCK_SIZE,
                self.x_offset + GRID_WIDTH * BLOCK_SIZE, self.y_offset + y * BLOCK_SIZE,
                fill=GRAY
            )
            
    def is_collision(self, tetromino):
        """Check if tetromino collides with filled cells or boundaries"""
        for x, y in tetromino.get_positions():
            # Check if out of bounds
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return True
            
            # Check if collides with an existing block in the grid (but only if y is valid)
            if y >= 0 and self.grid[y][x] is not None:
                return True
                
        return False
    
    def is_game_over(self):
        """Check if any blocks in the top row"""
        return any(self.grid[0][x] is not None for x in range(GRID_WIDTH))
    
    def lock_tetromino(self, tetromino):
        """Lock the tetromino in place on the grid"""
        for x, y in tetromino.get_positions():
            if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                self.grid[y][x] = tetromino.get_color()
    
    def clear_lines(self):
        """Clear completed lines and return the number of lines cleared"""
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        
        while y >= 0:
            # Check if line is complete
            if all(self.grid[y][x] is not None for x in range(GRID_WIDTH)):
                lines_cleared += 1
                
                # Move all lines above down
                for y2 in range(y, 0, -1):
                    for x in range(GRID_WIDTH):
                        self.grid[y2][x] = self.grid[y2-1][x]
                
                # Clear the top line
                for x in range(GRID_WIDTH):
                    self.grid[0][x] = None
            else:
                y -= 1
        
        return lines_cleared
    
    def draw(self):
        """Draw the current state of the grid"""
        # Clear previous grid drawing
        self.canvas.create_rectangle(
            self.x_offset, self.y_offset,
            self.x_offset + GRID_WIDTH * BLOCK_SIZE, self.y_offset + GRID_HEIGHT * BLOCK_SIZE,
            fill=BLACK, outline=""
        )
        
        # Draw grid lines
        self.draw_grid_lines()
        
        # Draw filled blocks
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    self.canvas.create_rectangle(
                        self.x_offset + x * BLOCK_SIZE,
                        self.y_offset + y * BLOCK_SIZE,
                        self.x_offset + (x + 1) * BLOCK_SIZE,
                        self.y_offset + (y + 1) * BLOCK_SIZE,
                        fill=self.grid[y][x],
                        outline=WHITE
                    )

    def toggle_colors(self, use_alt_colors):
        """Toggle between normal and alternate colors"""
        from constants import COLORS, ALT_COLORS
        
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    # Find which color it is and change it
                    for shape, color in COLORS.items():
                        if self.grid[y][x] == color:
                            self.grid[y][x] = ALT_COLORS[shape]
                            break
                        elif self.grid[y][x] == ALT_COLORS[shape]:
                            self.grid[y][x] = COLORS[shape]
                            break