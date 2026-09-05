# game_manager.py
# This file controls the game flow
# It manages turns, checks game over conditions, and handles score updates

from board import Board
from player import HumanPlayer, ComputerPlayer
from constants import PLAYER_X, PLAYER_O, MODE_PVP, MODE_PVC, DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_UNBEATABLE

class GameManager:
    """
    GameManager class - controls the entire game flow.
    Handles:
    - Setting up players based on game mode
    - Alternating turns between players
    - Checking for game over (win/tie)
    - Updating scores
    - Offering replay
    """
    
    def __init__(self):
        """
        Constructor - initializes the game manager.
        Creates a new board and sets up game state.
        """
        self.board = Board()  # Create a new board
        self.player1 = None   # Will be set in setup_game()
        self.player2 = None   # Will be set in setup_game()
        self.current_player = None  # Whose turn it is
        self.game_mode = None  # '1' for PvP, '2' for PvC
        self.is_running = False  # Is the game currently active?
    
    def setup_game(self):
        """
        Set up the game by choosing mode and creating players.
        Displays menu and gets user choices.
        """
        print("\n" + "=" * 50)
        print("      WELCOME TO TIC-TAC-TOE!")
        print("=" * 50)
        
        # Display game modes
        print("\nChoose game mode:")
        print(f"  {MODE_PVP}. Two Players (vs another person)")
        print(f"  {MODE_PVC}. vs Computer")
        print("  q. Quit")
        
        # Get mode selection
        while True:
            choice = input("\nEnter your choice: ").lower()
            
            if choice == 'q':
                print("Thanks for playing! Goodbye!")
                exit()
            
            if choice == MODE_PVP:
                self.game_mode = MODE_PVP
                self._setup_pvp_mode()
                break
            elif choice == MODE_PVC:
                self.game_mode = MODE_PVC
                self._setup_pvc_mode()
                break
            else:
                print("❌ Invalid choice! Please enter 1, 2, or q.")
    
    def _setup_pvp_mode(self):
        """
        Set up Player vs Player mode.
        Creates two human players.
        """
        print("\n--- Player vs Player Mode ---")
        
        # Get player names
        name1 = input("Enter name for Player 1 (X): ") or "Player 1"
        name2 = input("Enter name for Player 2 (O): ") or "Player 2"
        
        # Create players
        self.player1 = HumanPlayer(name1, PLAYER_X)
        self.player2 = HumanPlayer(name2, PLAYER_O)
        
        # X always goes first
        self.current_player = self.player1
        
        print(f"\n✅ Game ready! {name1} (X) vs {name2} (O)")
        print(f"   {name1} goes first!")
    
    def _setup_pvc_mode(self):
        """
        Set up Player vs Computer mode.
        Creates one human player and one computer player.
        """
        print("\n--- Player vs Computer Mode ---")
        
        # Get player name
        name = input("Enter your name (X): ") or "You"
        
        # Choose difficulty
        print("\nChoose difficulty:")
        print(f"  {DIFFICULTY_EASY}. Easy (Random moves)")
        print(f"  {DIFFICULTY_MEDIUM}. Medium (Strategic)")
        print(f"  {DIFFICULTY_UNBEATABLE}. Unbeatable (Impossible to win!)")
        
        while True:
            difficulty = input("\nEnter your choice (1-3): ")
            if difficulty in [DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_UNBEATABLE]:
                break
            print("❌ Invalid choice! Please enter 1, 2, or 3.")
        
        # Create players
        self.player1 = HumanPlayer(name, PLAYER_X)
        self.player2 = ComputerPlayer("Computer", PLAYER_O, difficulty)
        
        # X (human) always goes first
        self.current_player = self.player1
        
        # Set difficulty name for display
        difficulty_names = {
            DIFFICULTY_EASY: "Easy",
            DIFFICULTY_MEDIUM: "Medium",
            DIFFICULTY_UNBEATABLE: "Unbeatable"
        }
        
        print(f"\n✅ Game ready! {name} (X) vs Computer (O) - {difficulty_names[difficulty]} mode")
        print(f"   You go first!")
    
    def play_game(self):
        """
        Main game loop - runs the entire game.
        Handles turns, checks for game over, and manages replay.
        """
        self.is_running = True
        
        while self.is_running:
            # Display the board
            self.board.display()
            
            # Show whose turn it is
            print(f"\n{self.current_player.name}'s turn ({self.current_player.symbol})")
            
            # Get the player's move
            move = self.current_player.get_move(self.board)
            
            # If move is None (shouldn't happen, but just in case)
            if move is None:
                print("No moves available!")
                break
            
            row, col = move
            
            # Place the mark on the board
            self.board.place_mark(row, col, self.current_player.symbol)
            
            # Check if the game is over
            if self._check_game_over():
                # Game is over, ask to play again
                if not self._play_again():
                    self.is_running = False
                else:
                    # Reset board for new game
                    self.board.clear()
                    # X always goes first in new game
                    self.current_player = self.player1
            else:
                # Switch to the next player
                self._switch_player()
    
    def _check_game_over(self):
        """
        Check if the game is over (win or tie).
        Updates scores and displays result.
        
        Returns:
            True if game is over, False otherwise
        """
        current_symbol = self.current_player.symbol
        
        # Check if current player won
        if self.board.check_win(current_symbol):
            # Get the winning combination
            winning_cells = self.board.get_winning_combination(current_symbol)
            
            # Update score
            self.board.update_score(current_symbol)
            
            # Display result
            self.board.display()
            print("\n" + "🎉" * 10)
            print(f"🏆 {self.current_player.name} WINS! 🏆")
            print("🎉" * 10)
            
            # Show winning cells (optional highlight)
            if winning_cells:
                print(f"\nWinning cells: {winning_cells}")
            
            return True
        
        # Check if board is full (tie)
        elif self.board.is_full():
            # Update tie score
            self.board.update_score(None)
            
            # Display result
            self.board.display()
            print("\n" + "🤝" * 10)
            print("   IT'S A TIE! 🤝")
            print("🤝" * 10)
            
            return True
        
        # Game continues
        return False
    
    def _switch_player(self):
        """
        Switch the current player to the other player.
        """
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
    
    def _play_again(self):
        """
        Ask the player if they want to play again.
        
        Returns:
            True if yes, False if no
        """
        print("\n" + "-" * 50)
        print("📊 Current Scores:")
        print(f"   {self.player1.name} (X): {self.board.score_x}")
        print(f"   {self.player2.name} (O): {self.board.score_o}")
        print(f"   Ties: {self.board.ties}")
        print("-" * 50)
        
        # Ask to play again
        while True:
            choice = input("\nPlay again? (y/n): ").lower()
            if choice == 'y':
                return True
            elif choice == 'n':
                # Show final scores before quitting
                print("\n" + "=" * 50)
                print("   FINAL SCORES")
                print("=" * 50)
                print(f"   {self.player1.name} (X): {self.board.score_x}")
                print(f"   {self.player2.name} (O): {self.board.score_o}")
                print(f"   Ties: {self.board.ties}")
                print("=" * 50)
                print("\nThanks for playing! Goodbye! 👋")
                return False
            else:
                print("❌ Invalid input! Please enter 'y' or 'n'.")