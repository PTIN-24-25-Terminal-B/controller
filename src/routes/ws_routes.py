from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from handlers.car import car_actions
from handlers.web2 import web_actions
from handlers.ia import ia_actions
from socket_manager import get_manager


import asyncio

router = APIRouter(tags=["WebSocket"])

# Get the shared manager instance
manager = get_manager()

async def handle_client(client_id: str, client_type: str, websocket: WebSocket):
    action_map = {
        "web": web_actions,
        "car": car_actions,
        "ia": ia_actions
    }

    if client_type not in action_map:
        await websocket.send_text("Unknown client type")
        await websocket.close()
        return

    actions = action_map[client_type]

    while True:
        try:
            message = await websocket.receive_json()
            action = message.get("action")
            params = message.get("params", {})

            if action in actions:
                print(params)
                await actions[action](client_id, websocket, params, manager)
            else:
                await websocket.send_text(f"Unknown action: {action}")
        except Exception as e:
            await websocket.send_text(f"Error processing message: {str(e)}")

@router.websocket("/ws/{client_type}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_type: str, client_id: str):
    await websocket.accept()
    
    manager.add(client_type, client_id, websocket)
    print(f"{client_type.upper()} client [{client_id}] connected")

    try:
        if client_type == "web":
            print("connected_cars: ", manager["car"])
            await handle_client(client_id, client_type, websocket)
        else:
            while True:
                await asyncio.sleep(5)
    except WebSocketDisconnect:
        manager.remove(client_type, client_id)
        print(f"{client_type.upper()} client [{client_id}] disconnected")


@router.get("/ws/web/clientid")
def websocket_info():
    return {
        "description": "Use WebSocket at /ws/client/{client_id} to send action messages.",
        "example": {
            "url": "ws://localhost:8000/ws/client/abc123",
            "message1": {
                "action": "request_car",
                "params": {
                    "origin": [10, 20],
                    "destination": [30, 40]
                }
            },
            "response1": {
                "action": "car_selected",
                "params": {
                    "carId": "car123",
                    "path": [[10, 20], [15, 25], [20, 30]]
                }
            },
            "response2": {
                "action": "car_arrived",
                "params": {
                    "carId": "car123",
                    "path": [[30, 40], [35, 45], [40, 50]]
                }
            },
            "message2": {
                "action": "start_trip"
            },
            "response3": {
                "action": "trip_finished",
                "params": {
                    "carId": "car123"
                }
            }
        }
    }