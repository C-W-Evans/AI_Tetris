import tkinter as tk
from constants import (
    SCORE_SINGLE, SCORE_DOUBLE, SCORE_TRIPLE, SCORE_TETRIS, SCORE_SPECIAL,
    BLOCK_SIZE, WHITE, GRID_WIDTH
)

class Player:
    def __init__(self, canvas, grid, is_human=True, name="Player"):
        self.canvas = canvas
        self.grid = grid
        self.is_human = is_human
        self.name = name
        self.score = 0
        self.current_tetromino = None
        self.next_tetromino = None
        self.score_label = None
        self.is_game_over = False
    
    def update_score(self, lines_cleared, special_piece=False):
        """Update the player's score based on lines cleared"""
        if special_piece:
            self.score += SCORE_SPECIAL
        else:
            if lines_cleared == 1:
                self.score += SCORE_SINGLE
            elif lines_cleared == 2:
                self.score += SCORE_DOUBLE
            elif lines_cleared == 3:
                self.score += SCORE_TRIPLE
            elif lines_cleared == 4:
                self.score += SCORE_TETRIS
                
        self.update_score_display()
        return lines_cleared == 2  # Return True if two lines were cleared
    
    def update_score_display(self):
        """Update the score display on canvas"""
        if self.score_label:
            self.canvas.delete(self.score_label)
            
        x_offset = self.grid.x_offset + (GRID_WIDTH * BLOCK_SIZE) // 2
        y_offset = self.grid.y_offset - 20  # Position score above the grid
        
        self.score_label = self.canvas.create_text(
            x_offset, y_offset,
            text=f"{self.name}: {self.score}",
            fill=WHITE,
            font=("Arial", 16)
        )
    
    def move_left(self):
        """Move the current tetromino left if possible"""
        if not self.current_tetromino or self.is_game_over:
            return False
            
        self.current_tetromino.x -= 1
        
        # If collision, move back
        if self.grid.is_collision(self.current_tetromino):
            self.current_tetromino.x += 1
            return False
        return True
    
    def move_right(self):
        """Move the current tetromino right if possible"""
        if not self.current_tetromino or self.is_game_over:
            return False
            
        self.current_tetromino.x += 1
        
        # If collision, move back
        if self.grid.is_collision(self.current_tetromino):
            self.current_tetromino.x -= 1
            return False
        return True
    
    def move_down(self):
        """Move the current tetromino down if possible"""
        if not self.current_tetromino or self.is_game_over:
            return False, False
            
        self.current_tetromino.y += 1
        
        # If collision, move back and lock the tetromino
        if self.grid.is_collision(self.current_tetromino):
            self.current_tetromino.y -= 1
            self.grid.lock_tetromino(self.current_tetromino)
            
            # Check for completed lines
            lines_cleared = self.grid.clear_lines()
            two_lines_cleared = self.update_score(lines_cleared, 
                                                 special_piece=(self.current_tetromino.shape_name in ["HEART", "STAR"]))
            
            # Process next tetromino
            self.current_tetromino = self.next_tetromino
            self.next_tetromino = None
            
            # Check for game over
            if self.grid.is_game_over():
                self.is_game_over = True
                
            return False, two_lines_cleared
            
        return True, False
    
    def rotate(self):
        """Rotate the current tetromino if possible"""
        if not self.current_tetromino or self.is_game_over:
            return False
            
        original_rotation = self.current_tetromino.rotation
        self.current_tetromino.rotate()
        
        # If collision, rotate back
        if self.grid.is_collision(self.current_tetromino):
            self.current_tetromino.rotation = original_rotation
            return False
        return True
    
    def draw(self):
        """Draw the current tetromino"""
        if not self.current_tetromino:
            return
            
        positions = self.current_tetromino.get_positions()
        for x, y in positions:
            self.canvas.create_rectangle(
                self.grid.x_offset + x * BLOCK_SIZE,
                self.grid.y_offset + y * BLOCK_SIZE,
                self.grid.x_offset + (x + 1) * BLOCK_SIZE,
                self.grid.y_offset + (y + 1) * BLOCK_SIZE,
                fill=self.current_tetromino.get_color(),
                outline=WHITE
            )
    
    def toggle_colors(self, use_alt_colors):
        """Toggle tetromino colors"""
        if self.current_tetromino:
            self.current_tetromino.toggle_color(use_alt_colors)
        if self.next_tetromino:
            self.next_tetromino.toggle_color(use_alt_colors)