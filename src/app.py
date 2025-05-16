from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from routes.car_routes import router as car_router
from routes.path_routes import router as path_router
from ws.WSmanager import ConnectionManager

app = FastAPI()

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
    manager.add(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"[{client_id}] received: {data}")
    except WebSocketDisconnect:
        manager.remove(client_id)
        print(f"{client_id} disconnected")


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")