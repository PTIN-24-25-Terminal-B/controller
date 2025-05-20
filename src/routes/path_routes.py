from fastapi import APIRouter
from controllers import path_controller
from models.path_model import Point, Path

router = APIRouter(prefix="/paths", tags=["Paths"])

@router.get("/", response_model=list[Path])
async def get_all_paths():
    paths = path_controller.read_all_paths()
    return paths  # FastAPI will serialize it to JSON automatically

@router.post("/")
def create_path(points: list[Point]):
    return path_controller.create_path(points)

@router.put("/")
def update_path(path: Path):
    return path_controller.update_path(path)