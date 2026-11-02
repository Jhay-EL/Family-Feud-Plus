import asyncio
import json
import logging
import os
import sys
from typing import Set
import websockets
from websockets.server import WebSocketServerProtocol

if __package__ is None or __package__ == "":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from backend.game_engine import GameEngine
else:
    from .game_engine import GameEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class GameServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.host = host
        self.port = port
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.engine = GameEngine(project_root)
        self.connected_clients: Set[WebSocketServerProtocol] = set()

    async def broadcast_state(self):
        """Broadcasts current GameState to all connected Flutter windows."""
        if not self.connected_clients:
            return
        
        payload = json.dumps({
            "event": "STATE_SYNC",
            "data": self.engine.state.to_dict()
        })
        
        # Concurrently send to all clients
        await asyncio.gather(
            *[client.send(payload) for client in self.connected_clients],
            return_exceptions=True
        )

    async def broadcast_event(self, event_name: str, data: dict):
        if not self.connected_clients:
            return
        payload = json.dumps({"event": event_name, "data": data})
        await asyncio.gather(
            *[client.send(payload) for client in self.connected_clients],
            return_exceptions=True
        )

    async def handle_action(self, action_type: str, payload: dict, websocket: WebSocketServerProtocol):
        logging.info(f"Received action: {action_type} with payload {payload}")
        
        if action_type == "GET_STATE":
            await websocket.send(json.dumps({
                "event": "STATE_SYNC",
                "data": self.engine.state.to_dict()
            }))
            return

        elif action_type == "SET_ACTIVE_SCREEN":
            screen = payload.get("screen", "welcome")
            self.engine.state.active_screen = screen

        elif action_type == "REVEAL_ANSWER":
            index = payload.get("index", 1)
            self.engine.reveal_answer(index)

        elif action_type == "ADD_STRIKE":
            team = payload.get("team", "A")
            self.engine.add_strike(team)

        elif action_type == "CLEAR_STRIKE_DISPLAY":
            self.engine.clear_strike_display()

        elif action_type == "REWARD_POINTS":
            team = payload.get("team", "A")
            self.engine.reward_team(team)

        elif action_type == "SET_MULTIPLIER":
            mult = payload.get("multiplier", 1)
            self.engine.set_multiplier(mult)

        elif action_type == "LOG_ROUND":
            self.engine.log_and_next_round()

        elif action_type == "RESET_MATCH":
            self.engine.reset_match()

        elif action_type == "SHOW_ANSWERS_COUNT":
            self.engine.set_answers_count_visible(True)

        elif action_type == "CLEAR_ANSWERS_COUNT":
            self.engine.set_answers_count_visible(False)

        elif action_type == "LOAD_QUESTION":
            qid = payload.get("id")
            if qid:
                self.engine.load_question(qid)

        elif action_type == "PLAY_AUDIO":
            cue = payload.get("cue")
            if cue:
                self.engine.audio.play(cue)

        elif action_type == "SET_TEAM_NAMES":
            name_a = payload.get("team_a", "")
            name_b = payload.get("team_b", "")
            self.engine.set_team_names(name_a, name_b)

        elif action_type == "GET_QUESTIONS_LIST":
            round_type = payload.get("round_type", "face_off")
            if round_type == "face_off":
                questions = self.engine.db.get_all_face_off_questions()
            else:
                questions = self.engine.db.get_all_fast_money_questions()
            
            await websocket.send(json.dumps({
                "event": "QUESTIONS_LIST",
                "data": [{"id": q[0], "text": q[1]} for q in questions]
            }))
            return

        elif action_type == "SAVE_QUESTION":
            q_text = payload.get("question", "")
            answers = payload.get("answers", [])  # list of [text, points]
            q_id = payload.get("id")
            self.engine.db.save_face_off_question(q_text, answers, q_id)
            if q_id and self.engine.state.active_question and self.engine.state.active_question.id == q_id:
                self.engine.load_question(q_id)

        elif action_type == "DELETE_QUESTION":
            q_id = payload.get("id")
            if q_id:
                self.engine.db.delete_face_off_question(q_id)
                self.engine.load_first_available_question()

        # Fast Money Actions
        elif action_type == "FM_SET_ENTRY":
            player = payload.get("player", 1)
            idx = payload.get("index", 0)
            ans = payload.get("answer", "")
            pts = payload.get("points", 0)
            self.engine.set_fast_money_entry(player, idx, ans, pts)

        elif action_type == "FM_REVEAL_ANSWER":
            player = payload.get("player", 1)
            idx = payload.get("index", 0)
            self.engine.reveal_fast_money_answer(player, idx)

        elif action_type == "FM_REVEAL_POINTS":
            player = payload.get("player", 1)
            idx = payload.get("index", 0)
            self.engine.reveal_fast_money_points(player, idx)

        elif action_type == "FM_RESET":
            self.engine.reset_fast_money()

        # Broadcast state update to all clients
        await self.broadcast_state()

    async def client_handler(self, websocket: WebSocketServerProtocol):
        self.connected_clients.add(websocket)
        logging.info(f"Client connected: {websocket.remote_address}. Active: {len(self.connected_clients)}")
        try:
            # Send initial state on connection
            await websocket.send(json.dumps({
                "event": "STATE_SYNC",
                "data": self.engine.state.to_dict()
            }))

            async for message in websocket:
                try:
                    data = json.loads(message)
                    action_type = data.get("type", "")
                    payload = data.get("payload", {})
                    await self.handle_action(action_type, payload, websocket)
                except json.JSONDecodeError:
                    logging.error("Failed to decode JSON message from client.")
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected_clients.remove(websocket)
            logging.info(f"Client disconnected. Active: {len(self.connected_clients)}")

    async def process_request(self, path, request_headers):
        """HTTP Health check interceptor."""
        if path == "/health":
            return (200, [("Content-Type", "application/json")], b'{"status": "ok", "app": "Family-Feud-Core"}\n')
        return None

    async def start(self):
        logging.info(f"Starting Family Feud+ Core Server on ws://{self.host}:{self.port} ...")
        # In newer websockets versions process_request can be passed
        try:
            server = await websockets.serve(
                self.client_handler,
                self.host,
                self.port,
                process_request=self.process_request
            )
        except TypeError:
            server = await websockets.serve(
                self.client_handler,
                self.host,
                self.port
            )
        logging.info("Server is listening and ready for connections.")
        await server.wait_closed()

def main():
    server = GameServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logging.info("Server shut down cleanly.")

if __name__ == "__main__":
    main()
