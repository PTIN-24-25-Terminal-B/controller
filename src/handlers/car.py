from WSmanager import ConnectionManager
import websockets
from models.car_model import Car, CarState
from models.user_model import User, UserState
from fastapi import WebSocket
import json

ROUTING_WS_URL = "ws://192.168.20.7:5000/recalculate"

async def update_car(client_id: str, websocket: WebSocket, params: dict, manager: ConnectionManager):
    
    updated_car = Car(**params)
    # Add a message type to the data so web clients know what kind of update this is
    message = {
        "action": "update_car",
        "params": updated_car.model_dump(mode='json')
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
    
    user_id = current_car.userId
    user = User.read_user(user_id)
    print(user_id)
    client_ws = manager["web"][current_car.userId]
    print(f"User {user_id} state: {user.state}")
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
    
    Car.set_state(current_car.id, CarState.WAITING)

    return

async def change_path(client_id: str, websocket: WebSocket, params: dict, manager: ConnectionManager):
    try:
        async with websockets.connect(ROUTING_WS_URL) as routing_ws:
            position = params.get("position")
            current_car = Car.read_car(client_id)
            await routing_ws.send(json.dumps({"position": position, "current_path": current_car.currentPath}))
            response = json.loads(await routing_ws.recv())
            new_path = response.get("new_path")
            print(f"New path for car {client_id}: {new_path}")
            if not new_path:
                raise Exception("Error in pathing, no new path received")
            current_car.currentPath = new_path
            Car.write_car(current_car)
            user_id = current_car.userId
            if not websocket:
                Car.delete_car(client_id)
                raise(f"connection with car {client_id} lost")
            else:
                await websocket.send_json({
                    "action": "start_trip",
                    "params": {"path": new_path, "userId": user_id}
                })
            message = {
                "action": "path_changed",
                "params": {
                    "carId": client_id,
                    "newPath": new_path
                }
            }
            user_ws = manager["web"].get(user_id)
            if user_ws:
                await user_ws.send_json(message)
    except Exception as e:
        return e
    return

car_actions = {
    "update_car": update_car,
    "trip_completed": trip_completed,
    "change_path": change_path
}
