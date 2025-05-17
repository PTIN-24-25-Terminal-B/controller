# websocket_manager.py
from typing import Dict
from fastapi import WebSocket



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