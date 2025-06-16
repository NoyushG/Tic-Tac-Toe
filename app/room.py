from typing import Dict, Optional
from app.player import Player

BOARD_SIZE = 3

class GameRoom:
    def __init__(self, room_id: str):
        """
        Initializes a new game room with an empty board and settings.

        Attributes:
            room_id (str): Unique identifier for the room.
            players (Dict[str, Player]): Mapping of player IDs to Player objects.
            board (list): 2D list representing the game board.
            turn_symbol (str): The symbol ('X' or 'O') whose turn it is.
            winner (Optional[str]): Name of the winning player, or "Draw", or None.
            moves_made (int): Count of moves made in the current game.
            game_active (bool): Indicates whether the game is currently active.
        """
        self.room_id = room_id
        self.players: Dict[str, Player] = {}
        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn_symbol = "X"
        self.winner: Optional[str] = None
        self.moves_made = 0
        self.game_active = True

    def is_full(self) -> bool:
        """
        Returns whether the room has two players.
        """
        return len(self.players) == 2

    def assign_player(self, player_id: str, name: str, websocket) -> Optional[Player]:
        """
        Assigns a player to the room with a free symbol ('X' or 'O').

        Args:
            player_id (str): Unique ID of the player.
            name (str): Display name of the player.
            websocket: WebSocket connection of the player.

        Returns:
            Optional[Player]: The Player object if successfully assigned, else None.
        """
        symbols = [p.symbol for p in self.players.values()]
        symbol = "X" if "X" not in symbols else ("O" if "O" not in symbols else None)
        if not symbol:
            return None
        player = Player(player_id, name, symbol, websocket)
        self.players[player_id] = player
        return player

    def get_by_symbol(self, symbol: str) -> Optional[Player]:
        """
        Retrieves a player object by their game symbol.

        Args:
            symbol (str): The symbol to search for ('X' or 'O').

        Returns:
            Player or None
        """
        return next((p for p in self.players.values() if p.symbol == symbol), None)

    def valid_move(self, player: Player, row: int, col: int) -> bool:
        """
        Validates if a move is legal.

        Args:
            player (Player): The player attempting the move.
            row (int): Row index of the move.
            col (int): Column index of the move.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return (
            0 <= row < BOARD_SIZE and
            0 <= col < BOARD_SIZE and
            self.board[row][col] == "" and
            self.turn_symbol == player.symbol and
            self.game_active and
            self.is_full()
        )

    def make_move(self, player: Player, row: int, col: int) -> bool:
        """
        Processes a player's move and updates the game state.

        Args:
            player (Player): The player making the move.
            row (int): Row index of the move.
            col (int): Column index of the move.

        Returns:
            bool: True if the move was accepted, False if invalid.
        """
        if not self.valid_move(player, row, col):
            return False

        self.board[row][col] = player.symbol
        self.moves_made += 1

        if self.check_winner(player.symbol, row, col):
            self.winner = player.name
            player.score += 1
            self.game_active = False
        elif self.moves_made == BOARD_SIZE * BOARD_SIZE:
            self.winner = "Draw"
            self.game_active = False
        else:
            self.turn_symbol = "O" if self.turn_symbol == "X" else "X"

        return True

    def check_winner(self, symbol: str, row: int, col: int) -> bool:
        """
        Checks whether the current move leads to a win.

        Args:
            symbol (str): Symbol of the player who made the move.
            row (int): Row index of the move.
            col (int): Column index of the move.

        Returns:
            bool: True if the move resulted in a win.
        """
        win_row = all(self.board[row][c] == symbol for c in range(BOARD_SIZE))
        win_col = all(self.board[r][col] == symbol for r in range(BOARD_SIZE))
        win_diag = all(self.board[i][i] == symbol for i in range(BOARD_SIZE)) if row == col else False
        win_anti = all(self.board[i][BOARD_SIZE - 1 - i] == symbol for i in range(BOARD_SIZE)) if row + col == BOARD_SIZE - 1 else False
        return win_row or win_col or win_diag or win_anti

    def reset_game(self, reset_by: Player):
        """
        Resets the game board and state.

        Args:
            reset_by (Player): The player who initiated the reset.
        """
        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn_symbol = reset_by.symbol
        self.winner = None
        self.moves_made = 0
        self.game_active = True

    def serialize(self) -> dict:
        """
        Serializes the current game state for sending to clients.

        Returns:
            dict: A dictionary containing board state, turn info, winner, and scores.
        """
        return {
            "board": self.board,
            "turn": self.turn_symbol,
            "turn_name": self.get_by_symbol(self.turn_symbol).name if self.turn_symbol else "",
            "winner": self.winner,
            "game_active": self.game_active,
            "name_score": {p.name: p.score for p in self.players.values()}
        }
