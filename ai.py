from constants import GRID_WIDTH, GRID_HEIGHT

class AI:
    def __init__(self, player):
        self.player = player
        
    def make_move(self):
        """Make a move for the AI player to target the lowest gap"""
        if not self.player.current_tetromino or self.player.is_game_over:
            return
        
        # Find the best horizontal position and rotation
        best_position = self.find_best_position()
        
        # Apply moves to get to best position
        self.apply_moves(best_position)
    
    def find_best_position(self):
        """Find the best position for the current tetromino"""
        tetromino = self.player.current_tetromino
        original_x = tetromino.x
        original_y = tetromino.y
        original_rotation = tetromino.rotation
        
        best_score = float('-inf')
        best_position = {'x': original_x, 'rotation': original_rotation}
        
        # Try each rotation
        for rotation in range(len(tetromino.shape)):
            tetromino.rotation = rotation
            
            # Try each horizontal position
            for x in range(-2, GRID_WIDTH + 2):  # Range extended to handle wide pieces
                tetromino.x = x
                tetromino.y = original_y
                
                # Skip invalid positions
                if self.player.grid.is_collision(tetromino):
                    continue
                
                # Drop the piece all the way down
                drop_y = original_y
                while not self.player.grid.is_collision(tetromino):
                    drop_y = tetromino.y
                    tetromino.y += 1
                
                tetromino.y = drop_y
                
                # Calculate a score for this position
                score = self.evaluate_position(tetromino)
                
                if score > best_score:
                    best_score = score
                    best_position = {'x': x, 'rotation': rotation}
                
                # Reset for next try
                tetromino.y = original_y
        
        # Reset tetromino to original position
        tetromino.x = original_x
        tetromino.y = original_y
        tetromino.rotation = original_rotation
        
        return best_position
    
    def evaluate_position(self, tetromino):
        """Evaluate the position of a tetromino, focusing on filling lowest gaps"""
        # Simple heuristic: prefer positions that are lower (fill gaps at the bottom)
        y_positions = [y for _, y in tetromino.get_positions()]
        
        # Calculate height score - prefer lower positions
        height_score = sum(y_positions)
        
        # Get a copy of the grid with the tetromino placed
        temp_grid = [row[:] for row in self.player.grid.grid]
        for x, y in tetromino.get_positions():
            if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                temp_grid[y][x] = 1
        
        # Check for completed lines
        completed_lines = 0
        for y in range(GRID_HEIGHT):
            if all(temp_grid[y][x] is not None for x in range(GRID_WIDTH)):
                completed_lines += 1
        
        # Award points for completed lines
        lines_score = completed_lines * 50
        
        # Count adjacent blocks (tetromino to existing blocks)
        adjacency_score = 0
        for x, y in tetromino.get_positions():
            if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                # Check adjacent cells
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                        if (nx, ny) not in tetromino.get_positions() and temp_grid[ny][nx] is not None:
                            adjacency_score += 1
        
        return height_score + lines_score * 10 + adjacency_score * 2
    
    def apply_moves(self, best_position):
        """Apply moves to get to the best position"""
        tetromino = self.player.current_tetromino
        
        # Rotate to target rotation
        while tetromino.rotation != best_position['rotation']:
            self.player.rotate()
        
        # Move horizontally to target position
        while tetromino.x < best_position['x']:
            self.player.move_right()
        while tetromino.x > best_position['x']:
            self.player.move_left()