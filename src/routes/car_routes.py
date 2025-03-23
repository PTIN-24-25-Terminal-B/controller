from fastapi import APIRouter
from ..models.car_model import carModel
from ..services import car_service

router = APIRouter(prefix="/cars", tags=["Cars"])

print("hello world")

@router.get("/")
def get_cars():
    return car_service.get_all_cars()

@router.get("/{car_id}")
def get_car(car_id: int):
    return car_service.get_car_by_id(car_id)

@router.put("/{car_id}")
def update_car(car_id: int, updated_data: dict):
    return car_service.update_car(car_id, updated_data)

@router.post("/")
def add_car(car_data: dict):
    return car_service.create_car(car_data)

@router.patch("/{car_id}")
def partial_update_car(car_id: int, updated_data: dict):
    return car_service.partial_update_car(car_id, updated_data)

@router.delete("/{car_id}")
def delete_car(car_id: int):
    return car_service.delete_car(car_id)