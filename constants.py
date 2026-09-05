# constants.py
# This file stores all the constant values used throughout the game
# Constants are values that never change during the game

# Board settings
BOARD_SIZE = 3  # Tic-Tac-Toe board is 3x3
EMPTY_CELL = ' '  # What we display for empty cells
PLAYER_X = 'X'  # Player 1 symbol
PLAYER_O = 'O'  # Player 2 (or computer) symbol

# Game modes
MODE_PVP = '1'  # Player vs Player
MODE_PVC = '2'  # Player vs Computer

# Difficulty levels (for computer AI)
DIFFICULTY_EASY = '1'      # Random moves
DIFFICULTY_MEDIUM = '2'    # Smart but not perfect
DIFFICULTY_UNBEATABLE = '3' # Minimax algorithm

# All possible winning combinations (rows, columns, diagonals)
# Each tuple contains (row, col) positions that form a winning line
WINNING_COMBINATIONS = [
    # Rows
    [(0, 0), (0, 1), (0, 2)],  # Top row
    [(1, 0), (1, 1), (1, 2)],  # Middle row
    [(2, 0), (2, 1), (2, 2)],  # Bottom row
    # Columns
    [(0, 0), (1, 0), (2, 0)],  # Left column
    [(0, 1), (1, 1), (2, 1)],  # Middle column
    [(0, 2), (1, 2), (2, 2)],  # Right column
    # Diagonals
    [(0, 0), (1, 1), (2, 2)],  # Main diagonal
    [(0, 2), (1, 1), (2, 0)]   # Anti-diagonal
]

# Visual settings
SEPARATOR = '-' * 20  # A line of 20 dashes for visual separation