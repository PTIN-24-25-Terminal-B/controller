import json
from fastapi import WebSocket
from typing import List, Dict
import websockets
from WSmanager import ConnectionManager

async def update_car(client_id: str, websocket: WebSocket, params: Dict, manager: ConnectionManager):
    return

async def change_path(client_id: str, websocket: WebSocket, params: Dict, manager: ConnectionManager):
    return

car_actions = {
    "update_car": update_car,
    "change_path": change_path
}
