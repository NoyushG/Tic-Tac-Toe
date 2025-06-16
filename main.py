from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.websocket_handler import websocket_endpoint

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """
    Serves the main HTML page.

    Returns:
        HTMLResponse: The content of 'index.html' as the homepage.
    """
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.websocket("/ws/{room_id}/{player_id}")
async def websocket_route(websocket: WebSocket, room_id: str, player_id: str):
    """
    WebSocket endpoint for real-time communication.

    Args:
        websocket (WebSocket): The WebSocket connection object.
        room_id (str): Unique identifier for the game room.
        player_id (str): Unique identifier for the player.

    """
    await websocket_endpoint(websocket, room_id, player_id)
