# board.py
# This file handles all board-related operations
# It creates, displays, and manages the game board

from constants import BOARD_SIZE, EMPTY_CELL, WINNING_COMBINATIONS, PLAYER_X, PLAYER_O

class Board:
    """
    The Board class represents the Tic-Tac-Toe game board.
    It manages the grid, placing marks, checking win conditions,
    and displaying the board to the player.
    """
    
    def __init__(self):
        """
        Constructor - creates a new empty board.
        This runs automatically when we create a Board object.
        """
        # Create a 2D list (3x3 grid) filled with empty cells
        # This is called a "list comprehension" - it creates a 3x3 grid
        # The outer list has 3 rows, each row is a list of 3 empty cells
        self.grid = [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        # Initialize scores for both players
        # X is player 1, O is player 2 (or computer)
        self.score_x = 0  # Player X's wins
        self.score_o = 0  # Player O's wins
        self.ties = 0     # Number of tie games
    
    def display(self):
        """
        Display the current board in a nice visual format.
        Shows numbers (1-9) to help players choose positions.
        """
        # Clear the screen for cleaner display (optional)
        # import os
        # os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + " " * 10 + "TIC · TAC · TOE")  # Centered title
        print(SEPARATOR)
        
        # Display scoreboard
        print(f"  X {self.score_x}    O {self.score_o}    Ties {self.ties}")
        print(SEPARATOR)
        
        # Display the board with numbered positions
        # We'll show numbers 1-9 for easy position selection
        # The numbers correspond to:
        # 1 2 3
        # 4 5 6
        # 7 8 9
        
        print("    |   |   ")
        print(f"  {self._get_cell_display(0, 0)} | {self._get_cell_display(0, 1)} | {self._get_cell_display(0, 2)} ")
        print("____|___|____")
        print("    |   |   ")
        print(f"  {self._get_cell_display(1, 0)} | {self._get_cell_display(1, 1)} | {self._get_cell_display(1, 2)} ")
        print("____|___|____")
        print("    |   |   ")
        print(f"  {self._get_cell_display(2, 0)} | {self._get_cell_display(2, 1)} | {self._get_cell_display(2, 2)} ")
        print("    |   |   ")
        print(SEPARATOR)
    
    def _get_cell_display(self, row, col):
        """
        Private method (starts with underscore) to get what to display in a cell.
        If the cell is empty, show the position number (1-9) as a hint.
        If occupied, show the player's symbol (X or O).
        
        Args:
            row: Row index (0, 1, 2)
            col: Column index (0, 1, 2)
        
        Returns:
            String to display in the cell
        """
        # Calculate the position number (1-9) from row and column
        # row 0, col 0 -> 1, row 0, col 1 -> 2, etc.
        position = (row * BOARD_SIZE) + col + 1
        
        # If the cell is empty, show the number
        # If occupied, show the symbol (X or O)
        if self.grid[row][col] == EMPTY_CELL:
            return str(position)  # Convert number to string
        else:
            return self.grid[row][col]  # Return 'X' or 'O'
    
    def place_mark(self, row, col, symbol):
        """
        Place a mark on the board at the specified position.
        
        Args:
            row: Row index (0, 1, 2)
            col: Column index (0, 1, 2)
            symbol: 'X' or 'O'
        
        Returns:
            True if placement was successful, False if cell was occupied
        """
        # Check if the cell is empty
        if self.grid[row][col] == EMPTY_CELL:
            self.grid[row][col] = symbol  # Place the symbol
            return True
        return False  # Cell was already taken
    
    def is_empty(self, row, col):
        """
        Check if a specific cell is empty.
        
        Args:
            row: Row index
            col: Column index
        
        Returns:
            True if empty, False if occupied
        """
        return self.grid[row][col] == EMPTY_CELL
    
    def is_full(self):
        """
        Check if the entire board is full (no empty cells left).
        Used to detect tie games.
        
        Returns:
            True if board is full, False if there are empty cells
        """
        # Loop through every cell in the grid
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.grid[row][col] == EMPTY_CELL:
                    return False  # Found an empty cell
        return True  # No empty cells found
    
    def get_empty_cells(self):
        """
        Get a list of all empty cells on the board.
        Used for computer AI to choose moves.
        
        Returns:
            List of (row, col) tuples for all empty cells
        """
        empty_cells = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.grid[row][col] == EMPTY_CELL:
                    empty_cells.append((row, col))
        return empty_cells
    
    def check_win(self, symbol):
        """
        Check if a player with the given symbol has won.
        Checks all 8 winning combinations.
        
        Args:
            symbol: 'X' or 'O' to check for
        
        Returns:
            True if the player has won, False otherwise
        """
        # Check each winning combination
        for combination in WINNING_COMBINATIONS:
            # Check if all three cells in this combination have the player's symbol
            if all(self.grid[row][col] == symbol for (row, col) in combination):
                return True
        return False
    
    def get_winning_combination(self, symbol):
        """
        Similar to check_win, but returns the actual winning combination.
        Useful for highlighting the win on the board.
        
        Args:
            symbol: 'X' or 'O'
        
        Returns:
            The winning combination list if found, None otherwise
        """
        for combination in WINNING_COMBINATIONS:
            if all(self.grid[row][col] == symbol for (row, col) in combination):
                return combination
        return None
    
    def clear(self):
        """
        Reset the board to empty for a new game.
        Keeps the score intact.
        """
        self.grid = [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    def update_score(self, winner):
        """
        Update the score based on who won.
        
        Args:
            winner: 'X', 'O', or None for tie
        """
        if winner == PLAYER_X:
            self.score_x += 1
        elif winner == PLAYER_O:
            self.score_o += 1
        else:
            self.ties += 1  # Tie game
    
    def reset_scores(self):
        """
        Reset all scores to zero.
        Used when starting a new session.
        """
        self.score_x = 0
        self.score_o = 0
        self.ties = 0