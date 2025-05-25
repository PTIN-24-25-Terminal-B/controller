from WSmanager import ConnectionManager
from models.car_model import Car, CarState
from fastapi import WebSocket
import json

async def update_car(client_id: str, websocket: WebSocket, params: dict, manager: ConnectionManager):
    
    updated_car = Car(**params["car"])
    
    # Add a message type to the data so web clients know what kind of update this is
    message = {
        "action": "car_connected",
        "params": updated_car.model_dump_json(mode=json)
    }
    
    # Send notification to all connected web clients
    for client_id, websocket in manager["web"].items():
        try:
            # Using try-except to handle any potential errors with individual WebSockets
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending to web client {client_id}: {str(e)}")
    
    return Car.car_connection(updated_car)

async def trip_completed(client_id: str, websocket: WebSocket, params: dict, manager: ConnectionManager):
    current_car: Car = Car.read_car(client_id)
    
    if not current_car:
        websocket.send_text("error: car not in database")
        return
    elif current_car.state != CarState.TRAVELING:
        websocket.send_text("error: car was not in a trip")
    else:
        client_ws = manager["web"][current_car.userId]
        client_ws.send_json({
            "action": "car_arrived",
            "params": {"car_id": current_car.id}
        })
    return

async def change_path(client_id: str, websocket: WebSocket, params: dict, manager: ConnectionManager):
    return

car_actions = {
    "trip_completed": trip_completed,
    "update_car": update_car,
    "change_path": change_path
}
