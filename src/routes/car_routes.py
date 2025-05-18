from fastapi import APIRouter
from controllers import car_controller
from models.car_model import Car
from socket_manager import get_manager
import json

router = APIRouter(prefix="/cars", tags=["Cars"])

# Get the shared manager instance
manager = get_manager()

@router.get("/{car_id}")
async def get_car(car_id: str):
    return car_controller.get_car(car_id)

@router.get("/")
async def get_all_cars():
    return car_controller.get_all_cars()

#@router.post("/")
#async def create_car(car: Car):
#    return car_controller.create_car(car)

@router.put("/")
async def update_car(car: Car):
    return car_controller.update_car(car)

#@router.delete("/{car_id}")
#async def delete_car(car_id: str):
#    return car_controller.delete_car(car_id)

@router.post("/")
async def car_connection(car: Car):
    # Convert car to a dictionary that can be serialized to JSON
    car_data = car.model_dump(mode="json")
    
    # Add a message type to the data so web clients know what kind of update this is
    message = {
        "action": "car_connected",
        "params": car_data
    }
    
    # Send notification to all connected web clients
    for client_id, websocket in manager["web"].items():
        try:
            # Using try-except to handle any potential errors with individual WebSockets
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending to web client {client_id}: {str(e)}")
    
    # Process the car connection logic
    return Car.car_connection(car)


@router.delete("/{car_id}")
async def car_disconnect(car_id: str):
    return Car.delete_car(car_id)