from fastapi import WebSocket

class Player:
    def __init__(self, player_id: str, name: str, symbol: str, websocket: WebSocket):
        """
        Initializes a new player.

        Args:
            player_id (str): Unique ID for the player.
            name (str): Player's name.
            symbol (str): Symbol used in the game ('X' or 'O').
            websocket (WebSocket): WebSocket object to communicate with the player.
        """
        self.id = player_id
        self.name = name
        self.symbol = symbol
        self.websocket = websocket
        self.score = 0
