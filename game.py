# game.py
# This is the main entry point for the Tic-Tac-Toe game.
# It creates a GameManager and starts the game.

from game_manager import GameManager

def main():
    """
    Main function - entry point of the program.
    Creates a GameManager and runs the game.
    """
    # Create a new game manager
    game = GameManager()
    
    # Set up the game (choose mode, create players)
    game.setup_game()
    
    # Play the game (main game loop)
    game.play_game()

# This is the standard Python way to check if this file is being run directly
# If this file is imported as a module, main() won't run
# If this file is run directly, main() will run
if __name__ == "__main__":
    main()