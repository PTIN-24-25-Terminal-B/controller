from fastapi import APIRouter
from fastapi import Body
from controllers import car_controller

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.delete("/{car_id}")
async def delete_car_endpoint(car_id: str):
    return car_controller.delete_car(car_id)

@router.get("/{car_id}")
async def get_car_endpoint(car_id: str):
    return car_controller.get_car(car_id)

@router.put("/{car_id}")
async def update_car_endpoint(car_id: str, update_data: dict = Body(...)):
    return car_controller.edit_car(car_id, update_data)

@router.get("/")
async def get_all_cars_endpoint():
    return car_controller.get_all_cars()