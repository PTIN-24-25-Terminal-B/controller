from WSmanager import ConnectionManager
from models.car_model import Car, CarState
from models.user_model import User, UserState
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
    
    return Car.write_car(updated_car)

async def trip_completed(client_id: str, websocket: WebSocket, params: dict, manager: ConnectionManager):
    current_car: Car = Car.read_car(client_id)
    print(f"Trip completed for car {current_car.id} with params: {params}")
    
    if not current_car:
        websocket.send_json({"error": "car not in database"})
        return
    
    if current_car.state != CarState.TRAVELING:
        websocket.send_json({"error": "car not in trip"})
        return
    user_id = current_car.userId
    user = User.read_user(user_id)
    client_ws = manager["web"][current_car.userId]
    print(f"User {user_id} state: {user.state}")
    if not client_ws:
        await websocket.send_json({"error": "web client not connected"})
        return
    if user.state == UserState.WAITING:
        await client_ws.send_json({
            "action": "car_arrived",
            "params": {"car_id": current_car.id}
        })
    elif user.state == UserState.TRAVELING:
        await client_ws.send_json({
            "action": "reached_destination",
            "params": {"car_id": current_car.id}
        })
    else:
        await websocket.send_json({"error": "user not correct"})
        return
    
    Car.set_state(current_car.id, CarState.WAITING)

    return

async def change_path(client_id: str, websocket: WebSocket, params: dict, manager: ConnectionManager):
    return

car_actions = {
    "update_car": update_car,
    "trip_completed": trip_completed,
    "change_path": change_path
}
