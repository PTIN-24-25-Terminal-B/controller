import json
import websockets
from fastapi import WebSocket
from typing import Dict
from WSmanager import ConnectionManager
from models.car_model import Car, CarState
from models.user_model import User, UserState
import redis

ROUTING_WS_URL = "ws://192.168.20.7:5000/path"

# Temporary # connection for the database while con pool is missing

def get_redis_connection():
    return redis.Redis(host='redis-db', port=6379, db=0, decode_responses=True)


def is_valid_coord(coord: list) -> bool:
    return (
        isinstance(coord, list)
        and len(coord) == 2
        and all(isinstance(x, (int, float)) for x in coord)
    )


async def validate_params(origin, destination, websocket: WebSocket) -> bool:
    # print(f"Validating params: origin={origin}, destination={destination}")
    if not (is_valid_coord(origin) and is_valid_coord(destination)):
        await websocket.send_text("Invalid or missing origin/destination format")
        return False
    return True

def available_cars() -> list[Car]:
    r = get_redis_connection()
    allCars: list[Car] = Car.read_all_cars(r)
    availableCars: list[Car] = [] 
    for currentCar in allCars:
        if currentCar.working == False:
            availableCars.append(currentCar)
    return availableCars

async def get_new_route(start_coords: list[tuple[float, float]], destination: tuple[int, int]):
    try:

        async with websockets.connect(ROUTING_WS_URL) as routing_ws:

            await routing_ws.send(json.dumps({"start": start_coords, "goal": destination}))
            result_to_user = json.loads(await routing_ws.recv())

            car_index = result_to_user.get("car")
            path_to_user = result_to_user.get("path")

            if car_index is None or path_to_user is None:
                raise("error in pathing")
            
        return car_index, path_to_user
    except Exception as e:
        return e

async def request_car(client_id: str, websocket: WebSocket, params: dict, manager: ConnectionManager):
    try:
        user_id = params.get("userId")
        origin = params.get("origin")
        destination = params.get("destination")

        if not await validate_params(origin, destination, websocket):
            return

        free_cars: list[Car] = available_cars()
        start_coords: list[tuple[float, float]] = []
        for car in free_cars:
            start_coords.append(car.position)

        car_index, path_to_user = await get_new_route(start_coords, origin)

        car_id = free_cars[car_index].id
        
        car_ws = manager["car"].get(car_id)

        if not car_ws:
            Car.delete_car(car_id)
            raise(f"error connecting with car {car_id}, please try again")
        else:
            await car_ws.send_json({
                "action": "start_trip",
                "params": {"path": path_to_user}
            })

        await websocket.send_json({
            "action": "car_selected",
            "params": {"userId": user_id, "carId": car_id, "path": path_to_user}
        })

        User.write_user(User(
            id = user_id,
            state = UserState.WAITING,
            carId = car_id,
            origin = origin,
            destination = destination
        ))
        
        return
    except Exception as e:
        return e

async def continue_to_destination(client_id: str, websocket: WebSocket, params: dict, manager: ConnectionManager):
    try:
        user_id = params.get("userId")
    
        client = User.read_user(user_id)
        selected_car: Car = Car.read_car_id(client.carId)
        
        car_ws = manager["car"][selected_car.id]

        if selected_car.state == CarState.WAITING:

            car_index, path_to_destination = get_new_route(selected_car.position, client.destination)

            car_ws.send_json({
                "action": "start_trip",
                "params": {"path": path_to_destination}
            })

            User.write_user(User(
                id = user_id,
                state = UserState.TRAVELING,
                carId = client.carId,
                origin = client.origin,
                destination = client.destination
            ))
        else:
            WebSocket.send_text("error: car not arrived yet")
            return

        return
    except Exception as e:
        return e

web_actions = {
    "request_car": request_car,
    "start_trip": continue_to_destination
}
