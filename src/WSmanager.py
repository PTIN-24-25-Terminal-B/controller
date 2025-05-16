# websocket_manager.py
from typing import Dict
from fastapi import WebSocket

# Acciones por tipo
from handlers.car import car_actions
from handlers.web import web_actions
from handlers.ia import ia_actions

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {
            "web": {},
            "car": {},
            "ia": {}
        }

    def add(self, client_type: str, client_id: str, websocket: WebSocket):
        self.active_connections[client_type][client_id] = websocket

    def remove(self, client_type: str, client_id: str):
        self.active_connections[client_type].pop(client_id, None)

    def get(self, client_type: str, client_id: str) -> WebSocket | None:
        return self.active_connections[client_type].get(client_id)

    def has(self, client_type: str, client_id: str) -> bool:
        return client_id in self.active_connections[client_type]

async def handle_client(client_id: str, client_type: str, websocket: WebSocket):
    action_map = {
        "web": web_actions,
        "car": car_actions,
        "ia": ia_actions
    }

    if client_type not in action_map:
        await websocket.send_text("Unknown client type")
        await websocket.close()
        return

    actions = action_map[client_type]

    while True:
        try:
            message = await websocket.receive_json()
            action = message.get("action")
            params = message.get("params", {})


            if action in actions:
                await actions[action](client_id, websocket, params)
            else:
                await websocket.send_text(f"Unknown action: {action}")
        except Exception as e:
            await websocket.send_text(f"Error processing message: {str(e)}")
