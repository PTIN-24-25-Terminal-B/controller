from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from routes.car_routes import router as car_router
from routes.path_routes import router as path_router
from WSmanager import ConnectionManager, handle_client
from fastapi.middleware.cors import CORSMiddleware



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