# websocket_manager.py
from typing import Dict
from fastapi import WebSocket
from typing import Tuple

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[Tuple[str, str], WebSocket] = {}

    def add(self, client_type, client_id: str, websocket: WebSocket):
        self.active_connections[(client_type, client_id)] = websocket

    def remove(self,client_type, client_id: str):
        self.active_connections.pop((client_type, client_id), None)

    def get(self,client_type, client_id: str) -> WebSocket | None:
        return self.active_connections.get((client_type, client_id))

    def has(self, client_type, client_id: str) -> bool:
        return (client_type, client_id) in self.active_connections
