from fastapi import APIRouter
from controllers import car_controller
from models.car_model import Car

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.get("/{car_id}")
async def get_car(car_id: str):
    return car_controller.get_car(car_id)

@router.get("/")
async def get_all_cars():
    return car_controller.get_all_cars()

@router.post("/")
async def create_car(car: Car):
    return car_controller.create_car(car)

@router.put("/")
async def update_car(car: Car):
    return car_controller.update_car(car)

@router.delete("/{car_id}")
async def delete_car(car_id: str):
    return car_controller.delete_car(car_id)