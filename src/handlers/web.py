import json
import time
from fastapi import WebSocket
from typing import List, Dict
import websockets
from WSmanager import ConnectionManager


#Provisional hasta que este connexion a BD
AVAILABLE_CARS = [
    {"id": "1234", "position": [15, 66]},
    {"id": "car2", "position": [12, 91]},
    {"id": "car3", "position": [48, 66]},
    {"id": "car4", "position": [55, 93]},
    {"id": "car5", "position": [10, 66]},
    {"id": "car6", "position": [49, 87]},
]

ROUTING_WS_URL = "ws://192.168.20.7:5000/path"


def is_valid_coord(coord: List) -> bool:
    return (
        isinstance(coord, list) and
        len(coord) == 2 and
        all(isinstance(x, (int, float)) for x in coord)
    )


async def request_car(client_id: str, websocket: WebSocket, params: Dict, manager: ConnectionManager):
    print(1)
    origin = params.get("origin")
    destination = params.get("destination")

    print(0)
    if not (is_valid_coord(origin) and is_valid_coord(destination)):
        await websocket.send_text("Invalid or missing origin/destination format")
        return

#   this is temporary for testing

    car_ws = manager["car"]["1234"]
    print("123123")
    path_to_user = [[10,10],[10,10],[10,10]]
    path_to_destination = [[12, 12],[12, 12],[12, 12]]
    selected_car = AVAILABLE_CARS[0]
    car_id = selected_car["id"]

#    start_coords = [car["position"] for car in AVAILABLE_CARS]
#
#    try:
#        async with websockets.connect(ROUTING_WS_URL) as routing_ws:
#            # a. Rutas coches → usuario
#            await routing_ws.send(json.dumps({"start": start_coords, "goal": origin}))
#            result_to_user = json.loads(await routing_ws.recv())
#
#            car_index = result_to_user.get("car")
#            path_to_user = result_to_user.get("path")
#
#            if car_index is None or path_to_user is None:
#                await websocket.send_text("Invalid response from routing service")
#                return
#
#            selected_car = AVAILABLE_CARS[car_index]
#            car_id = selected_car["id"]
#
#            car_ws = manager.get("car", car_id)
#            if car_ws:
#                await websocket.send_josn({
#                    "action": "car_selected",
#                    "params": {
#                        "carId": car_id
#                    }
#                })  
#            else:
#                await websocket.send_text(f"Error connecting with car, please try again")
#                return
#
#            # b. Ruta usuario → destino
#            await routing_ws.send(json.dumps({
#                "action": "calculate_routes",
#                "params": {
#                    "start": origin,
#                    "goal": destination
#                }
#            }))
#            path_to_destination = json.loads(await routing_ws.recv())
#
#    except Exception as e:
#        await websocket.send_text(f"Routing service error: {str(e)}")
#        return

    # ➤ Enviar la primera ruta al coche
    print(manager["car"]["1234"])
    await car_ws.send_json({
        "action": "start_trip",
        "params": {
            "path": path_to_user
        }
    })

    # ➤ Esperar confirmación del coche (llegada al usuario)
    
    time.sleep(2)
    
    while True:
        message = await car_ws.receive_json()
        if message.get("action") == "trip_completed":
            break
        if message.get("action") == "trip_cancelled":
            await websocket.send_json({
                "action": "trip_cancelled"
            })
            return
        if message.get("action") == "recalc_path":
            #call ia to recalc path
            print()

    # ➤ Avisar al cliente web que el coche ha llegado
    await websocket.send_json({
        "action": "car_arrived",
        "params": {
            "car_id": car_id
        }
    })

    # ➤ Esperar confirmación del cliente para iniciar viaje
    while True:
        message = await websocket.receive_json()
        if message.get("action") == "start_trip":
            break

    # ➤ Enviar ruta al coche para llevar al usuario al destino
    await car_ws.send_json({
        "action": "start_trip",
        "params": {
            "path": path_to_destination.get("path")
        }
    })

    # ➤ Esperar confirmación del coche (viaje finalizado)
    while True:
        message = await car_ws.receive_json()
        if message.get("action") == "trip_completed":
            break
        if message.get("action") == "recalc_path":
            #call ia to recalc path
            print()

    await car_ws.send_json({
        "action": "trip_finished",
    })

    # ➤ Avisar al cliente que el viaje terminó
    await websocket.send_json({
        "action": "trip_finished",
        "params": {
            "car_id": car_id
        }
    })


web_actions = {
    "request_car": request_car
}
