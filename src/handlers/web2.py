import json
import websockets
from fastapi import WebSocket
from typing import Dict, Tuple
from WSmanager import ConnectionManager
from models.car_model import Car
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

async def notify_car_arrival(car_ws: WebSocket, path_to_user: list[list[int]]):
    # print(f"Sending car arrival path: {path_to_user}")
    await car_ws.send_json({
        "action": "start_trip",
        "params": {"path": path_to_user}
    })
    # print(f"Sent")


async def wait_for_car_arrival(car_ws: WebSocket, websocket: WebSocket) -> bool:
    while True:
        message = await car_ws.receive_json()
        action = message.get("action")
        if action == "trip_completed":
            break
        elif action == "trip_cancelled":
            await websocket.send_json({"action": "trip_cancelled"})
            return False
        elif action == "recalc_path":
            # print("Recalculating path (car side)...")
            print("Recalculating path...")
    # print("Waiting for car arrival...")

async def notify_client_car_arrived(websocket: WebSocket, car_id: str, path_to_destination: list[list[int]]):
    # print(f"Notifying client car {car_id} has arrived")
    await websocket.send_json({
        "action": "car_arrived",
        "params": {"car_id": car_id, "path": path_to_destination}
    })


async def wait_for_client_to_start(websocket: WebSocket):
    # print("Waiting for client to start trip...")
    while True:
        message = await websocket.receive_json()
        # print(f"Received from client: {message}")
        if message.get("action") == "start_trip":
            break


async def send_trip_to_destination(car_ws: WebSocket, path_to_destination: list[list[int]]):
    # print(f"Sending path to destination: {path_to_destination}")
    await car_ws.send_json({
        "action": "start_trip",
        "params": {"path": path_to_destination}
    })


async def wait_for_trip_completion(car_ws: WebSocket):
    # print("Waiting for trip completion...")
    while True:
        message = await car_ws.receive_json()
        # print(f"Received from car: {message}")
        if message.get("action") == "trip_completed":
            break
        elif message.get("action") == "recalc_path":
            print("Recalculating path...")


async def notify_trip_finished(car_ws: WebSocket, websocket: WebSocket, car_id: str):
    # print(f"Notifying trip finished for car {car_id}")
    await car_ws.send_json({"action": "trip_finished"})
    await websocket.send_json({
        "action": "trip_finished",
        "params": {"car_id": car_id}
    })


async def get_routing_info(origin, destination, websocket: WebSocket):
    try:
        free_cars: list[Car] = available_cars()
        start_coords: list[Tuple[float, float]] = []
        for car in free_cars:
            start_coords.append(car.position)       

        # print(f"Connecting to routing service at {ROUTING_WS_URL}")
        async with websockets.connect(ROUTING_WS_URL) as routing_ws:
            # a. Rutes: cotxes → usuari
            await routing_ws.send(json.dumps({"start": start_coords, "goal": origin}))
            result_to_user = json.loads(await routing_ws.recv())
            # print(f"Routing response to user: {result_to_user}")

            car_index = result_to_user.get("car")
            path_to_user = result_to_user.get("path")

            if car_index is None or path_to_user is None:
                await websocket.send_text("Invalid response from routing service (step 1)")
                return None, None, None

            selected_car = free_cars[car_index]
            car_id = selected_car.id
            origin_coords: list[Tuple[float, float]] = []
            origin_coords.append(origin)
            # b. Ruta: usuari → destí
            await routing_ws.send(json.dumps({"start": origin_coords, "goal": destination}))
            path_to_destination_resp = json.loads(await routing_ws.recv())
            # print(f"Routing response to destination: {path_to_destination_resp}")
            path_to_destination = path_to_destination_resp.get("path")

            if path_to_destination is None:
                await websocket.send_text(f"Invalid response from routing service (step 2): {path_to_destination_resp}")
                return None, None, None

            return car_id, path_to_user, path_to_destination

    except Exception as e:
        # print(f"Exception during routing: {e}")
        await websocket.send_text(f"Routing service error: {str(e)}")
        return None, None, None


async def request_car(client_id: str, websocket: WebSocket, params: Dict, manager: ConnectionManager):
    origin = params.get("origin")
    destination = params.get("destination")

    # print(f"Client {client_id} requesting car from {origin} to {destination}")
    if not await validate_params(origin, destination, websocket):
        return

    car_id, path_to_user, path_to_destination = await get_routing_info(origin, destination, websocket)
    if not car_id:
        return

    
    car_ws = manager["car"].get(car_id)

    if not car_ws:
        await websocket.send_text(f"Error connecting with car {car_id}, please try again")
        return

    await websocket.send_json({
        "action": "car_selected",
        "params": {"carId": car_id, "path": path_to_user}
    })
    # print(f"Car {car_id} selected and notified to client")

    await notify_car_arrival(car_ws, path_to_user)

    await wait_for_car_arrival(car_ws, websocket)

    await notify_client_car_arrived(websocket, car_id, path_to_destination)
    await wait_for_client_to_start(websocket)
    await send_trip_to_destination(car_ws, path_to_destination)
    await wait_for_trip_completion(car_ws)
    await notify_trip_finished(car_ws, websocket, car_id)
    await websocket.close()


web_actions = {
    "request_car": request_car
}
