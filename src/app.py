from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from routes.car_routes import router as car_router
from routes.path_routes import router as path_router
from WSmanager import ConnectionManager
from fastapi.middleware.cors import CORSMiddleware

# Acciones por tipo
from handlers.car import car_actions
from handlers.web import web_actions
from handlers.ia import ia_actions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes from carRoutes.py
app.include_router(car_router)
app.include_router(path_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Car API"}

manager = ConnectionManager()

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
            print(3)

            if action in actions:
                print(2)
                await actions[action](client_id, websocket, params, manager)
            else:
                await websocket.send_text(f"Unknown action: {action}")
        except Exception as e:
            await websocket.send_text(f"Error processing message: {str(e)}")

@app.websocket("/ws/{client_type}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_type: str, client_id: str):
    await websocket.accept()
    manager.add(client_type, client_id, websocket)
    print(f"{client_type.upper()} client [{client_id}] connected")

    try:
        await handle_client(client_id, client_type, websocket)
    except WebSocketDisconnect:
        manager.remove(client_type, client_id)
        print(f"{client_type.upper()} client [{client_id}] disconnected")

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")