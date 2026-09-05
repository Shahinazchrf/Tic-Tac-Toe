# player.py
# This file handles all player-related logic
# It defines HumanPlayer (keyboard input) and ComputerPlayer (AI)

import random
from constants import PLAYER_X, PLAYER_O, EMPTY_CELL, DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_UNBEATABLE

class Player:
    """
    Base Player class - parent class for all players.
    All players have a name and a symbol (X or O).
    """
    
    def __init__(self, name, symbol):
        """
        Initialize a player with a name and symbol.
        
        Args:
            name: Player's name (e.g., "Player 1", "Computer")
            symbol: 'X' or 'O'
        """
        self.name = name
        self.symbol = symbol
    
    def get_move(self, board):
        """
        Get the player's next move.
        This is a placeholder - child classes will override this.
        
        Args:
            board: The current Board object
        
        Returns:
            (row, col) tuple for the move
        """
        # This method will be overridden by HumanPlayer and ComputerPlayer
        pass


class HumanPlayer(Player):
    """
    HumanPlayer class - handles keyboard input from a real person.
    Inherits from Player class.
    """
    
    def __init__(self, name, symbol):
        """Initialize a human player."""
        # Call the parent class constructor
        super().__init__(name, symbol)
    
    def get_move(self, board):
        """
        Get a move from the human player via keyboard input.
        Displays the board and asks for a position (1-9).
        
        Args:
            board: The current Board object
        
        Returns:
            (row, col) tuple for the chosen position
        """
        while True:
            try:
                # Show whose turn it is
                print(f"\n{self.name} ({self.symbol}) - Your turn!")
                
                # Ask for input
                move = input("Choose a position (1-9): ")
                
                # Check if user wants to quit
                if move.lower() == 'q':
                    print("Game quit by player.")
                    exit()
                
                # Convert input to integer
                position = int(move)
                
                # Validate position is between 1 and 9
                if position < 1 or position > 9:
                    print("❌ Please enter a number between 1 and 9!")
                    continue
                
                # Convert position (1-9) to (row, col) coordinates
                # Position 1 → (0,0), 2 → (0,1), 3 → (0,2)
                # Position 4 → (1,0), 5 → (1,1), 6 → (1,2)
                # Position 7 → (2,0), 8 → (2,1), 9 → (2,2)
                row = (position - 1) // 3  # Integer division
                col = (position - 1) % 3   # Remainder
                
                # Check if the cell is empty
                if not board.is_empty(row, col):
                    print("❌ That cell is already taken! Choose another.")
                    continue
                
                # Valid move found - return it
                return (row, col)
                
            except ValueError:
                # User entered something that's not a number
                print("❌ Invalid input! Please enter a number (1-9) or 'q' to quit.")


class ComputerPlayer(Player):
    """
    ComputerPlayer class - handles AI logic.
    Supports three difficulty levels:
    - Easy: Random moves
    - Medium: Strategic (win/block)
    - Unbeatable: Minimax algorithm
    """
    
    def __init__(self, name, symbol, difficulty=DIFFICULTY_EASY):
        """
        Initialize a computer player.
        
        Args:
            name: Player's name (e.g., "Computer")
            symbol: 'X' or 'O'
            difficulty: '1' (easy), '2' (medium), or '3' (unbeatable)
        """
        super().__init__(name, symbol)
        self.difficulty = difficulty
    
    def get_move(self, board):
        """
        Get a move from the computer based on difficulty level.
        
        Args:
            board: The current Board object
        
        Returns:
            (row, col) tuple for the chosen position
        """
        print(f"\n{self.name} ({self.symbol}) is thinking...")
        
        # Choose strategy based on difficulty
        if self.difficulty == DIFFICULTY_EASY:
            return self._get_random_move(board)
        elif self.difficulty == DIFFICULTY_MEDIUM:
            return self._get_medium_move(board)
        else:  # DIFFICULTY_UNBEATABLE
            return self._get_unbeatable_move(board)
    
    def _get_random_move(self, board):
        """
        Easy difficulty: Choose a random empty cell.
        
        Args:
            board: The current Board object
        
        Returns:
            (row, col) tuple for random move
        """
        empty_cells = board.get_empty_cells()
        if empty_cells:
            return random.choice(empty_cells)
        return None  # No moves available
    
    def _get_medium_move(self, board):
        """
        Medium difficulty: Try to win, then block opponent, else random.
        
        Args:
            board: The current Board object
        
        Returns:
            (row, col) tuple for strategic move
        """
        # First, try to win
        win_move = self._find_winning_move(board, self.symbol)
        if win_move:
            return win_move
        
        # If can't win, block opponent's winning move
        opponent_symbol = PLAYER_O if self.symbol == PLAYER_X else PLAYER_X
        block_move = self._find_winning_move(board, opponent_symbol)
        if block_move:
            return block_move
        
        # If no strategic move, play random
        return self._get_random_move(board)
    
    def _find_winning_move(self, board, symbol):
        """
        Find a move that would win the game for the given symbol.
        
        Args:
            board: The current Board object
            symbol: 'X' or 'O' to check for
        
        Returns:
            (row, col) tuple if winning move found, None otherwise
        """
        # Get all empty cells
        empty_cells = board.get_empty_cells()
        
        # Try each empty cell
        for row, col in empty_cells:
            # Temporarily place the mark
            board.grid[row][col] = symbol
            
            # Check if this move wins
            if board.check_win(symbol):
                # Undo the move
                board.grid[row][col] = EMPTY_CELL
                return (row, col)
            
            # Undo the move
            board.grid[row][col] = EMPTY_CELL
        
        return None  # No winning move found
    
    def _get_unbeatable_move(self, board):
        """
        Unbeatable difficulty: Use Minimax algorithm.
        The computer will never lose (will win or tie).
        
        Args:
            board: The current Board object
        
        Returns:
            (row, col) tuple for the best move
        """
        # If board is empty, choose center or corner for optimal play
        if len(board.get_empty_cells()) == 9:
            # Center is best first move
            return (1, 1)
        
        # Use minimax to find best move
        best_score = float('-inf')  # Negative infinity
        best_move = None
        
        # Try all empty cells
        for row, col in board.get_empty_cells():
            # Try this move
            board.grid[row][col] = self.symbol
            
            # Calculate score using minimax
            score = self._minimax(board, 0, False)
            
            # Undo the move
            board.grid[row][col] = EMPTY_CELL
            
            # Update best move if score is better
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        return best_move
    
    def _minimax(self, board, depth, is_maximizing):
        """
        Minimax algorithm - evaluates all possible moves.
        
        Args:
            board: The current Board object
            depth: How deep in the tree (used for tie-breaking)
            is_maximizing: True if maximizing player (computer), False if minimizing (human)
        
        Returns:
            Score for the current board state
        """
        opponent_symbol = PLAYER_O if self.symbol == PLAYER_X else PLAYER_X
        
        # Check terminal states (win/loss/tie)
        if board.check_win(self.symbol):
            return 10 - depth  # Win is good, but closer to end is better
        
        if board.check_win(opponent_symbol):
            return -10 + depth  # Loss is bad, but closer to end is better
        
        if board.is_full():
            return 0  # Tie game
        
        # If maximizing (computer's turn)
        if is_maximizing:
            best_score = float('-inf')
            for row, col in board.get_empty_cells():
                # Try move
                board.grid[row][col] = self.symbol
                
                # Recursively evaluate
                score = self._minimax(board, depth + 1, False)
                
                # Undo move
                board.grid[row][col] = EMPTY_CELL
                
                # Update best score
                best_score = max(score, best_score)
            return best_score
        
        # If minimizing (human's turn)
        else:
            best_score = float('inf')
            for row, col in board.get_empty_cells():
                # Try move
                board.grid[row][col] = opponent_symbol
                
                # Recursively evaluate
                score = self._minimax(board, depth + 1, True)
                
                # Undo move
                board.grid[row][col] = EMPTY_CELL
                
                # Update best score
                best_score = min(score, best_score)
            return best_score