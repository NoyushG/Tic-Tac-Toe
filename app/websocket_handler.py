from fastapi import WebSocket, WebSocketDisconnect
from app.room import GameRoom
from typing import Dict


class GameManager:
    """
    Manages all active game rooms.

    Attributes:
        rooms (Dict[str, GameRoom]): Mapping of room IDs to GameRoom instances.
    """

    def __init__(self):
        """Initializes the GameManager with an empty room list."""
        self.rooms: Dict[str, GameRoom] = {}

    def get_or_create_room(self, room_id: str) -> GameRoom:
        """
        Retrieves a room by ID, or creates it if it doesn't exist.

        Args:
            room_id (str): Unique identifier of the game room.

        Returns:
            GameRoom: The existing or newly created room.
        """
        if room_id not in self.rooms:
            self.rooms[room_id] = GameRoom(room_id)
        return self.rooms[room_id]


# Singleton instance of GameManager
game_manager = GameManager()


async def websocket_endpoint(websocket: WebSocket, room_id: str, player_id: str):
    """
    Handles a player's WebSocket connection to the game room.

    Args:
        websocket (WebSocket): The WebSocket connection.
        room_id (str): The ID of the room the player is joining.
        player_id (str): Unique ID of the player.
    """
    await websocket.accept()
    room = game_manager.get_or_create_room(room_id)
    player = None

    try:
        # Receive the initial join message with player name
        join_data = await websocket.receive_json()
        name = join_data.get("name", "Anonymous Player")

        # Assign player to the room
        player = room.assign_player(player_id, name, websocket)
        if not player:
            await websocket.send_json({"error": "Room is full."})
            await websocket.close()
            return

        await websocket.send_json({"symbol": player.symbol})
        await broadcast(room, f"{player.name} joined the room.")

        # Notify players when room is full and game starts
        if room.is_full():
            await broadcast(room, "The game begins!")
            await broadcast(room, room.serialize())
        else:
            await broadcast(room, "Waiting for another player...")

        # Main game loop
        while True:
            data = await websocket.receive_json()

            if data.get("action") == "reset":
                room.reset_game(player)
                await broadcast(room, "Game has been reset.")
                await broadcast(room, room.serialize())
                continue

            # Handle move
            row, col = data.get("row"), data.get("col")
            if room.make_move(player, row, col):
                await broadcast(room, room.serialize())

                if not room.game_active:
                    # Notify each player of the result
                    for p in room.players.values():
                        msg = {"message_type": "", "message": ""}
                        if room.winner == "Draw":
                            msg = {"message_type": "draw", "message": "It's a draw!"}
                        elif room.winner == p.name:
                            msg = {"message_type": "win", "message": "You won! 🎉"}
                        else:
                            msg = {"message_type": "lose", "message": "You lost 😞"}
                        await p.websocket.send_json(msg)
            else:
                await websocket.send_json({"error": "Invalid move or not your turn."})

    except WebSocketDisconnect:
        # Handle player disconnection
        if player:
            room.players.pop(player.id, None)
        await broadcast(room, f"{player.name if player else 'A player'} disconnected.")


async def broadcast(room: GameRoom, message):
    """
    Sends a message to all players in a room.

    Args:
        room (GameRoom): The game room to broadcast in.
        message: Either a string (text message) or dict (JSON payload).
    """
    disconnected = []
    for p in room.players.values():
        try:
            if isinstance(message, str):
                await p.websocket.send_text(message)
            else:
                await p.websocket.send_json(message)
        except WebSocketDisconnect:
            disconnected.append(p.id)

    # Remove disconnected players
    for pid in disconnected:
        room.players.pop(pid, None)
