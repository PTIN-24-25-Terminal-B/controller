from pydantic import BaseModel, Field
from models.path_model import Point, Path
import json
import redis

from pydantic import BaseModel
from typing import Optional
import json

# Assuming Point and Path are already defined as Pydantic models

class Car(BaseModel):
    id: str
    batery: float
    position: Point
    working: bool = False
    currentPath: Optional[Path] = None

    def __str__(self):
        return json.dumps(self.model_dump(mode="json"), indent=4)

    def modifyCar(
        self,
        newBatery: float = None,
        newPosition: Point = None,
        working: bool = None,
        currentPath: Path = None
    ):
        if newBatery is not None:
            self.batery = newBatery
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
        return Car(**json.loads(data)) if data else None

    @staticmethod
    def read_all_cars(redis_conn):
        keys = redis_conn.keys("car:*")
        return [json.loads(redis_conn.get(k)) for k in keys if redis_conn.get(k)]

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
    def delete_car(car_id: str, redis_conn):
        return redis_conn.delete(f"car:{car_id}")