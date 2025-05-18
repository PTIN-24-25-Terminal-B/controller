from pydantic import BaseModel, Field
from models.path_model import Point
import json
import redis

from pydantic import BaseModel, Field
import json
import redis
from typing import List, Tuple

def get_redis_connection():
    return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class Car(BaseModel):
    id: str
    battery: float
    position: Tuple[int, int]  # Simple coordinate tuple instead of Point
    working: bool = False
    currentPath: List[Tuple[int, int]] = Field(default_factory=list)  # List of coordinate tuples

    def __str__(self):
        return json.dumps(self.model_dump(mode="json"), indent=4)

    def modifyCar(
        self,
        newBattery: float = None,
        newPosition: Tuple[int, int] = None,
        working: bool = None,
        currentPath: List[Tuple[int, int]] = None
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

    @staticmethod
    def get_car(car_id: str, redis_conn):
        data = redis_conn.get(f"car:{car_id}")
        if data:
            car_data = json.loads(data)
            # No need to convert position or currentPath as they're already in the right format
            return Car(**car_data)
        return None

    @staticmethod
    def read_all_cars(redis_conn):
        keys = redis_conn.keys("car:*")
        cars = []
        for key in keys:
            raw = redis_conn.get(key)
            if raw:
                data = json.loads(raw)
                # No need to convert position or currentPath
                car = Car(**data)
                cars.append(car)
        return cars

    @staticmethod
    def create_car(car: "Car", redis_conn):
        key = f"car:{car.id}"
        value = car.model_dump_json(indent=4)
        if redis_conn.set(key, value, nx=True):
            return car
        else:
            raise ValueError("Car with given id already exists")

    @staticmethod
    def update_car(car: "Car", redis_conn):
        key = f"car:{car.id}"
        value = car.model_dump_json(indent=4)
        if redis_conn.set(key, value, xx=True):
            return car
        else:
            raise ValueError("Car with given id does not exist")

    @staticmethod
    def delete_car(car_id: str):
        redis_conn = get_redis_connection()
        return redis_conn.delete(f"car:{car_id}")
    
    @staticmethod
    def car_connection(car: "Car"):
        redis_conn = get_redis_connection()
        key = f"car:{car.id}"
        value = car.model_dump_json(indent=4)
        redis_conn.set(key, value)
        return car
