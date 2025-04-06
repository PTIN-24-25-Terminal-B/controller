from fastapi import FastAPI
import uvicorn
from routes.car_routes import router as car_router
from routes import path_routes

app = FastAPI()

# Include routes from carRoutes.py
app.include_router(car_router)
app.include_router(path_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Car API"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")