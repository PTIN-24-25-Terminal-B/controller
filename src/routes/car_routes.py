from fastapi import APIRouter

router = APIRouter(prefix="/cars", tags=["Cars"])

print("hello world")

@router.get("/")
def get_cars():
    return {"message": "List of cars"}

@router.get("/{car_id}")
def get_car(car_id: int):
    return {"message": f"Details of car {car_id}"}

@router.post("/")
def add_car(car: dict):
    return {"message": "Car added", "car": car}
