from fastapi import APIRouter
from ..controllers import car_controller

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.delete("/{car_id}")
async def delete_car_endpoint(car_id: str):
    return car_controller.delete_car(car_id)

