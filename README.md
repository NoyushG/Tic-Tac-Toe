# Tic-Tac-Toe
Real Time Multiplayer Game with FastAPI & WebSockets  

Project Description:
This project is a real-time multiplayer game implemented using FastAPI and WebSockets. 
The game allows two players to connect to a shared game room, make moves, and see each other’s actions in real-time. 

## Project Structure:

project/
├── main.py                      # Entry point: FastAPI app and routes
├── app/
|    ├── websocket.py            # WebSocket connection handling
|    ├── game.py                 # Game room and game logic management
|    ├── player.py               # Player logic
├── static/
│   ├── index.html               # Main frontend HTML

## Design Highlights:
- Each player is tracked by a unique player_id in a room_id.
- The backend holds the game state in memory (GameRoom objects).
- Client moves are sent via WebSocket messages and broadcasted to other players in the same room.
- The UI supports real-time updates, and keyboard input.


## How to Run Locally:

1. Clone the project:
   git clone Tic-Tac-Toe
   cd project

2. Install dependencies:
   "uvicorn[standard]", fastapi uvicorn

3. Run the development server:
   uvicorn main:app --reload

4. Open your browser and visit:
   http://127.0.0.1:8000

5. Play the Game:
   - Enter a nickname and room ID.
   - Open multiple tabs or devices to simulate multiple players in the same room.
