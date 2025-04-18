from fastapi import APIRouter
from controllers import path_controller
from models.path_model import Point, Path

router = APIRouter(prefix="/paths", tags=["Paths"])

@router.get("/")
async def get_all_paths():
    return path_controller.read_all_paths()

@router.post("/")
def create_path(points: list[Point]):
    for p in points:
        print(p.x, p.y)
    return path_controller.create_path(points)

@router.put("/")
def update_path(path: Path):
    return path_controller.update_path(path)