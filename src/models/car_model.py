import json
from models.path_model import Point, Path

class Car:
    # variable types: carModel(integer, string, string, float, integer)
    def __init__(self, id: str, batery: float, position: Point, working: bool, currentPath: Path=None):
        self.id = id
        self.batery = batery
        self.position = position
        self.working = working
        self.currentPath = currentPath
    
    # when reading the class as a string, returns de data in the model in json format
    def __str__(self):
        return json.dumps({
            "id": self.id,
            "batery": self.batery,
            "position": self.position.to_dict(),
            "working": self.working,
            "currentPath": self.currentPath.to_dict() if self.currentPath else None
        }, indent=4)
    
    # allows to modify any of the stored data in the car model. Warning, changing it's id might create some errors
    # like the target car not being found, or modifying the values of another car
    def modifyCar(self, newBatery:float = None, newPosition: Point = None, working: bool = None, currentPath: Path = None):
        if newBatery is not None:
            self.batery = newBatery
        if newPosition is not None:
            self.position = newPosition
        if working is not None:
            self.working = working
        if currentPath is not None:
            self.mileage = currentPath
        return self
    
    # method to delete the car model
    def __del__(self):
        return
    
def delete_car(car_id: str, redis_conn):
    key = f"car:{car_id}"
    return redis_conn.delete(key)  # Retorna 1 si s'esborra, 0 si no existeix

def get_car(car_id: str, redis_conn):
    key = f"car:{car_id}"
    car_data = redis_conn.get(key)
    
    if not car_data:
        return None
    
    car_dict = json.loads(car_data)
    
    # Convertir datos crudos a objetos del modelo
    position = Point(x=car_dict["position"]["x"], y=car_dict["position"]["y"])
    
    current_path = None
    if car_dict.get("currentPath"):
        path_points = [Point(x=p["x"], y=p["y"]) for p in car_dict["currentPath"]["points"]]
        current_path = Path(pathId=car_dict["currentPath"]["id"], path=path_points)
    
    return Car(
        id=car_dict["id"],
        batery=car_dict["batery"],
        position=position,
        working=car_dict["working"],
        currentPath=current_path
    )

def save_car(car: Car, redis_conn):
    key = f"car:{car.id}"
    car_data = json.dumps({
        "id": car.id,
        "batery": car.batery,
        "position": {"x": car.position.x, "y": car.position.y},
        "working": car.working,
        "currentPath": {
            "id": car.currentPath.id,
            "points": [{"x": p.x, "y": p.y} for p in car.currentPath.path]
        } if car.currentPath else None
    }, indent=4)
    redis_conn.set(key, car_data)
    return car
