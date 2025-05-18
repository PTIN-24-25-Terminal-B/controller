from fastapi import FastAPI
import uvicorn
from routes.car_routes import router as car_router
from routes.path_routes import router as path_router
from routes.ws_routes import router as ws_router
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
app.include_router(ws_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Car API"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")