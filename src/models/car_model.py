from pydantic import BaseModel
import json
import redis
from typing import Optional
from enum import Enum

def get_redis_connection():
    return redis.Redis(host='192.168.20.7', port=6379, db=0, decode_responses=True)

class CarState(Enum):
    IDLE = "idle"
    WAITING = "waiting"
    TRAVELING = "traveling"

    def __str__(self):
        return self.value

class Car(BaseModel):
    id: str
    battery: float
    position: tuple[int, int]
    state: CarState = CarState.IDLE
    userId: Optional[str] = None
    currentPath: Optional[list[tuple[int, int]]] = None

    def __str__(self):
        return self.model_dump_json(indent=2)

    def modifyCar(
        self,
        newBattery: float = None,
        newPosition: tuple[int, int] = None,
        working: bool = None,
        currentPath: list[tuple[int, int]] = None
    ):
        if newBattery is not None:
            self.battery = newBattery
        if newPosition is not None:
            self.position = newPosition
        if working is not None:
            self.working = working
        if currentPath is not None:
            self.currentPath = currentPath
        return self

#    @staticmethod
#    def get_car(car_id: str, redis_conn):
#        data = redis_conn.get(f"car:{car_id}")
#        if data:
#            car_data = Car.model_validate_json(data)
#            # No need to convert position or currentPath as they're already in the right format
#            return car_data
#        return None
#
#
#    @staticmethod
#    def create_car(car: "Car", redis_conn):
#        key = f"car:{car.id}"
#        value = car.model_dump_json(indent=4)
#        if redis_conn.set(key, value, nx=True):
#            return car
#        else:
#            raise ValueError("Car with given id already exists")
#
#    @staticmethod
#    def update_car(car: "Car", redis_conn):
#        key = f"car:{car.id}"
#        value = car.model_dump_json(indent=4)
#        if redis_conn.set(key, value, xx=True):
#            return car
#        else:
#            raise ValueError("Car with given id does not exist")

    @staticmethod
    def delete_car(car_id: str):
        redis_conn = get_redis_connection()
        return redis_conn.delete(f"car:{car_id}")
    
    @staticmethod
    def write_car(car: "Car"):
        redis_conn = get_redis_connection()
        key = f"car:{car.id}"
        value = car.model_dump_json(indent=2)
        redis_conn.set(key, value)
        return car

    @staticmethod
    def read_car(car_id: str):
        redis_conn = get_redis_connection()
        car = redis_conn.get(f"car:{car_id}")
        if car == None:
            return None
        else:
            return Car.model_validate_json(car)
    
    @staticmethod
    def read_all_cars():
        redis_conn = get_redis_connection()
        keys = redis_conn.keys("car:*")
        cars = []
        for key in keys:
            raw = redis_conn.get(key)
            if raw:
                car = Car.model_validate_json(raw)
                cars.append(car)
        return cars

    @staticmethod
    def set_state(car_id: str, new_state: CarState):
        redis_conn = get_redis_connection()
        car: Car = Car.read_car(car_id)
        if car == None:
            return None
        car.state = new_state
        key = f"car:{car.id}"
        value = car.model_dump_json(indent=2)
        return redis_conn.set(key, value)