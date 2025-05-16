from fastapi import HTTPException
from fastapi.responses import JSONResponse
from models.car_model import Car
import redis
import uuid

def get_redis_connection():
    return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_car(car_id: str):
    r = get_redis_connection()
    car = Car.get_car(car_id, r)  # Your model function
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

def get_all_cars():
    r = get_redis_connection()
    return Car.read_all_cars(r)


def create_car(car: Car):
    r = get_redis_connection()
    try:
        return Car.create_car(car, r)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def update_car(car: Car):
    r = get_redis_connection()
    try:
        return Car.update_car(car, r)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

def delete_car(car_id: str):
    r = get_redis_connection()
    deleted = Car.delete_car(car_id, r)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}
