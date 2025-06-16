# Tic-Tac-Toe
Real Time Multiplayer Game with FastAPI & WebSockets  

Project Description:

This project is a real-time multiplayer game implemented using FastAPI and WebSockets. 
The game allows two players to connect to a shared game room, make moves, and see each other’s actions in real-time. 

Project Structure:

project/
├── main.py                      # Entry point: FastAPI app and routes
├── app/
|    ├── websocket.py            # WebSocket connection handling
|    ├── game.py                 # Game room and game logic management
|    ├── player.py               # Player logic
├── static/
│   ├── index.html               # Main frontend HTML

