import tkinter as tk
from game import TetrisGame

def main():
    """Entry point of the application"""
    # Create the main window
    root = tk.Tk()
    root.resizable(False, False)
    
    # Create and start the game
    game = TetrisGame(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()