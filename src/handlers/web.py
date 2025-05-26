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
        print("a")
        async with websockets.connect(ROUTING_WS_URL) as routing_ws:
            print(start_coords)
            await routing_ws.send(json.dumps({"start": start_coords, "goal": destination}))
            print("a2")
            result_to_user = json.loads(await routing_ws.recv())
            print(result_to_user)

            car_index = result_to_user.get("car")
            print("a4")
            path_to_user = result_to_user.get("path")
            print("a5")

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
        print("asdasdasdasdf,gjhasdrfglkjasrflkHJNKL:DSVChkovdfpsza")

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

        print(selected_car)

        selected_car.userId = user_id
        selected_car.currentPath = path_to_user
        selected_car.state = CarState.TRAVELING

        print(selected_car)

        Car.write_car(selected_car)

        print(selected_car)

        User.write_user(User(
            id = user_id,
            state = UserState.WAITING,
            carId = car_id,
            origin = origin,
            destination = None
        ))
        
        return
    except Exception as e:
        return e

async def continue_to_destination(client_id: str, websocket: WebSocket, params: dict, manager: ConnectionManager):
    try:
        destination = params.get("destination")
        user_id = params.get("userId")
    
        client = User.read_user(user_id)
        selected_car: Car = Car.read_car(client.carId)
        
        car_ws = manager["car"][selected_car.id]

        if selected_car.state == CarState.WAITING:

            car_index, path_to_destination = get_new_route(selected_car.position, destination)

            car_ws.send_json({
                "action": "start_trip",
                "params": {"path": path_to_destination}
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

        car_ws.send_json({"action": "trip_finished"})

        User.write_user(User(
            id = user_id,
            state = UserState.IDLE
        ))

        Car.set_state(user.carId, CarState.IDLE)

        return
    except:
        return

web_actions = {
    "request_car": request_car,
    "start_trip": continue_to_destination,
    "trip_finished": trip_finished
}
