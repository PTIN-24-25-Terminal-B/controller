# routes/path_routes.py

from fastapi import APIRouter
from controller import path_controller

router = APIRouter()

@router.delete("/paths/{path_id}")
async def delete_path_endpoint(path_id: str):
    return path_controller.delete_path(path_id)
