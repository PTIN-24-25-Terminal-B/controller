from fastapi import APIRouter
from controllers import path_controller

router = APIRouter(prefix="/paths", tags=["Paths"])

@router.post("/")
async def get_cars(x0: float, y0: float, x1:float, y1: float):      #Looking for a way to recieve the data, not finished
    return path_controller.create_path(x0, y0, x1, y1)

@router.get("/")
async def get_all_paths():
    return path_controller.read_all_paths()

@router.delete("/{path_id}")
async def delete_path_endpoint(path_id: str):
    return path_controller.delete_path(path_id)
