import json
import websockets
from fastapi import WebSocket
from typing import Dict
from WSmanager import ConnectionManager
from models.car_model import Car, CarState
from models.user_model import User, UserState

ROUTING_WS_URL = "ws://192.168.20.7:5000/path"

def is_valid_coord(coord: list) -> bool:
    return (
        isinstance(coord, list)
        and len(coord) == 2
        and all(isinstance(x, (int, float)) for x in coord)
    )


#async def validate_params(origin, destination, websocket: WebSocket) -> bool:
#    # print(f"Validating params: origin={origin}, destination={destination}")
#    if not (is_valid_coord(origin) and is_valid_coord(destination)):
#        await websocket.send_text("Invalid or missing origin/destination format")
#        return False
#    return True

def available_cars() -> list[Car]:
    allCars: list[Car] = Car.read_all_cars()
    print(allCars)
    availableCars: list[Car] = [] 
    for currentCar in allCars:
        if currentCar.state == CarState.IDLE:
            availableCars.append(currentCar)
    return availableCars

async def get_new_route(start_coords: list[tuple[float, float]], destination: tuple[int, int]):
    try:
        async with websockets.connect(ROUTING_WS_URL) as routing_ws:
            print(start_coords, destination)
            await routing_ws.send(json.dumps({"start": start_coords, "goal": destination}))
            result_to_user = json.loads(await routing_ws.recv())

            car_index = result_to_user.get("car")
            path_to_user = result_to_user.get("path")
            if car_index is None or path_to_user is None:
                print(car_index, path_to_user)
                raise("error in pathing")
            
        return car_index, path_to_user
    except Exception as e:
        return e

async def request_car(client_id: str, websocket: WebSocket, params: dict, manager: ConnectionManager):
    try:

        user_id = params.get("userId")
        origin = params.get("origin")

        free_cars: list[Car] = available_cars()
        print(free_cars)
        start_coords: list[tuple[float, float]] = []
        for car in free_cars:
            start_coords.append(car.position)

        car_index, path_to_user = await get_new_route(start_coords, origin)

        selected_car = free_cars[car_index]
        car_id = selected_car.id
        
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

        selected_car.userId = user_id
        selected_car.currentPath = path_to_user
        selected_car.state = CarState.TRAVELING

        Car.write_car(selected_car)

        print(Car.read_car(car_id))

        User.write_user(User(
            id = user_id,
            state = UserState.WAITING,
            carId = car_id,
            origin = origin,
            destination = None
        ))

        print(User.read_user(user_id))
        
        return
    except Exception as e:
        return e

async def continue_to_destination(client_id: str, websocket: WebSocket, params: dict, manager: ConnectionManager):
    try:
        destination = params.get("destination")
        user_id = params.get("userId")
    
        client = User.read_user(user_id)
        selected_car: Car = Car.read_car(client.carId)
        origin: list[tuple[float, float]] = []
        origin.append(selected_car.position)
        car_ws = manager["car"][selected_car.id]

        if selected_car.state == CarState.WAITING:

            car_index, path_to_destination = await get_new_route(origin, destination)

            await car_ws.send_json({
                "action": "start_trip",
                "params": {"path": path_to_destination}
            })

            await websocket.send_json({
                "action": "car_selected",
                "params": {"userId": user_id, "carId": selected_car.id, "path": path_to_destination}
            })

            selected_car.userId = user_id
            selected_car.currentPath = path_to_destination
            selected_car.state = CarState.TRAVELING
            Car.write_car(selected_car)

            User.write_user(User(
                id = user_id,
                state = UserState.TRAVELING,
                carId = client.carId,
                origin = client.origin,
                destination = destination
            ))

        else:
            WebSocket.send_text("error: car not arrived yet")
            return

        return
    except Exception as e:
        return e
    
async def trip_finished(client_id: str, websocket: WebSocket, params: dict, manager: ConnectionManager):
    try:
        user_id = params.get("userId")
        user = User.read_user(user_id)
        car_ws = manager["car"][user.carId]

        await car_ws.send_json({"action": "trip_finished"})

        User.write_user(User(
            id = user_id,
            state = UserState.IDLE
        ))

        selected_car: Car = Car.read_car(user.carId)
        selected_car.userId = None
        selected_car.currentPath = None
        selected_car.state = CarState.IDLE
        Car.write_car(selected_car)
        print(Car.read_car(user.carId), User.read_user(user_id))
        return
    except:
        return

web_actions = {
    "request_car": request_car,
    "start_trip": continue_to_destination,
    "trip_finished": trip_finished
}
