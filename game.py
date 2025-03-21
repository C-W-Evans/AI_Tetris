import tkinter as tk
import time
import random
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE,
    BLACK, WHITE, INITIAL_FALL_SPEED, GAME_DURATION,
    COLOR_CHANGE_INTERVAL, COLOR_CHANGE_DURATION, SPEED_BOOST_DURATION,
    SLOW_DOWN_THRESHOLD, SPECIAL_PIECE_THRESHOLD
)
from tetromino import Tetromino
from grid import Grid
from player import Player
from ai import AI

class TetrisGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tetris Battle")
        
        # Set window size and position
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create canvas
        self.canvas = tk.Canvas(root, width=window_width, height=window_height, bg="black")
        self.canvas.pack()
        
        # Create grids with adjusted positions
        grid_top_padding = 100
        self.human_grid = Grid(self.canvas, 50, y_offset=grid_top_padding)
        self.ai_grid = Grid(self.canvas, 450, y_offset=grid_top_padding)
        
        # Create players
        self.human_player = Player(self.canvas, self.human_grid, is_human=True, name="Human")
        self.ai_player = Player(self.canvas, self.ai_grid, is_human=False, name="AI")
        
        # Create AI
        self.ai = AI(self.ai_player)
        
        # Initialize game state
        self.is_running = True
        self.last_fall_time = time.time()
        self.last_ai_move_time = time.time()
        self.last_color_change = time.time()
        self.points_to_win = 5000
        self.using_alt_colors = False
        self.game_start_time = time.time()
        
        # Create initial tetrominos
        self.create_new_tetromino(self.human_player)
        self.create_new_tetromino(self.ai_player)
        
        # Bind controls
        self.root.bind("<Left>", lambda e: self.safe_action(self.human_player.move_left))
        self.root.bind("<Right>", lambda e: self.safe_action(self.human_player.move_right))
        self.root.bind("<Down>", lambda e: self.safe_action(lambda: self.human_player.move_down()[0]))
        self.root.bind("<Up>", lambda e: self.safe_action(self.human_player.rotate))
        self.root.bind("<space>", lambda e: self.safe_action(lambda: self.hard_drop(self.human_player)))
        self.root.bind("<Escape>", lambda e: self.quit_game())
        
        # Start game loop at 30 FPS
        self.update()

    def update(self):
        """Update game state"""
        if not self.is_running:
            return
            
        current_time = time.time()
        
        # Check win conditions
        if (self.human_player.score >= self.points_to_win or 
            self.ai_player.score >= self.points_to_win or 
            self.human_player.is_game_over or 
            self.ai_player.is_game_over):
            self.end_game()
            return
            
        # Handle color changes directly in update loop
        if self.using_alt_colors and current_time - self.last_color_change >= 20:
            self.toggle_colors(False)
            self.last_color_change = current_time
        elif not self.using_alt_colors and current_time - self.last_color_change >= 120:
            self.toggle_colors(True)
            self.last_color_change = current_time
            
        # Calculate current fall speed (25% faster than default)
        current_fall_speed = 0.75
        ai_fall_speed = current_fall_speed / 4
        
        # Handle human moves
        if not self.human_player.is_game_over and current_time - self.last_fall_time >= current_fall_speed:
            success, two_lines = self.human_player.move_down()
            if not success:
                if two_lines and not self.ai_player.is_game_over:
                    self.ai_player.next_tetromino = Tetromino.get_penalty_piece()
                self.create_new_tetromino(self.human_player)
            self.last_fall_time = current_time
            
        # Handle AI moves
        if not self.ai_player.is_game_over and current_time - self.last_ai_move_time >= ai_fall_speed:
            self.ai.make_move()
            success, two_lines = self.ai_player.move_down()
            if not success:
                if two_lines and not self.human_player.is_game_over:
                    self.human_player.next_tetromino = Tetromino.get_penalty_piece()
                self.create_new_tetromino(self.ai_player)
            self.last_ai_move_time = current_time
            
        # Draw game state
        self.redraw()
        
        # Schedule next update (30 FPS)
        self.root.after(33, self.update)

    def safe_action(self, action):
        """Wrapper to safely execute player actions"""
        if self.is_running:
            try:
                action()
            except Exception as e:
                print(f"Error in action: {e}")
                
    def toggle_colors(self, use_alt):
        """Toggle colors for all game elements"""
        if not self.is_running:
            return
            
        self.human_player.toggle_colors(use_alt)
        self.ai_player.toggle_colors(use_alt)
        self.human_grid.toggle_colors(use_alt)
        self.ai_grid.toggle_colors(use_alt)
        self.using_alt_colors = use_alt

    def redraw(self):
        """Redraw the entire game state"""
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw timer and title in one text element
        current_time = time.time()
        elapsed_time = int(current_time - self.game_start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        
        header_text = f"TWO-PLAYER TETRIS\nTime: {minutes:02d}:{seconds:02d}"
        if self.using_alt_colors:
            header_text += " - RAINBOW MODE!!!"
            
        self.canvas.create_text(
            WINDOW_WIDTH // 2, 45,
            text=header_text,
            fill=WHITE,
            font=("Arial", 24, "bold"),
            justify="center"
        )
        
        # Draw game elements
        self.human_grid.draw()
        self.ai_grid.draw()
        self.human_player.draw()
        self.ai_player.draw()
        self.human_player.update_score_display()
        self.ai_player.update_score_display()

    def end_game(self):
        """End the game and show results"""
        self.is_running = False
        
        # Clear canvas one last time
        self.canvas.delete("all")
        
        # Determine winner
        winner_text = "Game Over!"
        if self.human_player.score >= self.points_to_win:
            winner_text = "Human Wins by Points!"
        elif self.ai_player.score >= self.points_to_win:
            winner_text = "AI Wins by Points!"
        elif self.human_player.is_game_over:
            winner_text = "AI Wins! Human Grid Full!"
        elif self.ai_player.is_game_over:
            winner_text = "Human Wins! AI Grid Full!"
            
        # Display game over and results
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50,
            text="GAME OVER",
            fill="red",
            font=("Arial", 36, "bold")
        )
        
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20,
            text=winner_text,
            fill="white",
            font=("Arial", 28)
        )
        
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80,
            text=f"Final Scores:\nHuman: {self.human_player.score}\nAI: {self.ai_player.score}",
            fill="white",
            font=("Arial", 24)
        )
        
        # Wait 6 seconds before closing
        self.root.after(6000, self.quit_game)

    def create_new_tetromino(self, player):
        """Create a new tetromino for the player"""
        if player.next_tetromino:
            player.current_tetromino = player.next_tetromino
            player.next_tetromino = None
        else:
            # Check if we should spawn a special piece
            if self.human_player.score >= self.points_to_win or self.ai_player.score >= self.points_to_win:
                player.current_tetromino = Tetromino.get_special_piece()
            else:
                player.current_tetromino = Tetromino()
    
    def quit_game(self):
        """Quit the game"""
        self.root.quit()
        
    def hard_drop(self, player):
        """Instantly drop the tetromino to the bottom"""
        if not player.current_tetromino or player.is_game_over:
            return
            
        # Keep moving down until collision
        while player.move_down()[0]:
            pass