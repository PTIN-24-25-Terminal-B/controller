from ..models.car_model import carModel
from fastapi import HTTPException

#BBDD temporal en memoria per fer proves
cars_db = [
    carModel(id=1, carType="Sedan", seatCount=4),
    carModel(id=2, carType="SUV", seatCount=6)
]

def get_car_by_id(car_id: int):
    #Buscar el cotxe en la "base de dades"
    car = next((car for car in cars_db if car.id == car_id), None)
    
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    #Convertir l'objecte a diccionari per FastAPI
    return {
        "id": car.id,
        "carType": car.carType,
        "seatCount": car.seatCount,
        "mileage": car.mileage,
        "completedRuns": car.completedRuns
    }

def get_all_cars():
    #Mirar si hi ha cotxes a la "base de dades"
    if not cars_db:
        raise HTTPException(status_code=404, detail="No cars found in database")
    #Retorna una llista amb tots els cotxes i tota la seva info
    return [
        {
            "id": car.id,
            "carType": car.carType,
            "seatCount": car.seatCount,
            "mileage": car.mileage,
            "completedRuns": car.completedRuns
        }
        for car in cars_db
    ]

def update_car(car_id: int, updated_data: dict):
    #Camps que es poden modificar, verificació
    allowed_fields = {"carType", "seatCount", "mileage", "completedRuns"}
    if not set(updated_data.keys()).issubset(allowed_fields):
        raise HTTPException(status_code=400, detail="Campos no permitidos para actualización")
    
    #Buscar el coche
    car_index = next((i for i, car in enumerate(cars_db) if car.id == car_id), None)
    
    if car_index is None:
        raise HTTPException(status_code=404, detail="Car not found")
    
    #Actualizar camps
    car = cars_db[car_index]
    
    #Metode modifyCar del model
    car.modifyCar(
        newType=updated_data.get("carType"),
        newSeat=updated_data.get("seatCount"),
        newId=None,  #Canvia el id por portar inconsistencies
        newMileage=updated_data.get("mileage"),
        newRuns=updated_data.get("completedRuns")
    )

    return car.to_dict()


def partial_update_car(car_id: int, updated_data: dict):
    car_index = next((i for i, car in enumerate(cars_db) if car.id == car_id), None)
    
    if car_index is None:
        raise HTTPException(status_code=404, detail="Car not found")
    
    car = cars_db[car_index]
    
    #Actualizar només el camp rebut
    if "carType" in updated_data:
        car.carType = updated_data["carType"]
    if "seatCount" in updated_data:
        car.seatCount = updated_data["seatCount"]
    if "mileage" in updated_data:
        car.mileage = updated_data["mileage"]
    if "completedRuns" in updated_data:
        car.completedRuns = updated_data["completedRuns"]
    
    return car.to_dict()

def create_car(car_data: dict):
    #Validar camps requerits
    required_fields = {"carType", "seatCount"}
    if not required_fields.issubset(car_data.keys()):
        raise HTTPException(status_code=400, detail="Faltan campos obligatorios: carType y seatCount")
    
    #Generar nou ID
    new_id = max(car.id for car in cars_db) + 1 if cars_db else 1
    
    #Crear instancia del model
    new_car = carModel(
        id=new_id,
        carType=car_data["carType"],
        seatCount=car_data["seatCount"],
        mileage=car_data.get("mileage", 0.0),
        completedRuns=car_data.get("completedRuns", 0)
    )
    
    cars_db.append(new_car)
    return new_car.to_dict()


def delete_car(car_id: int):
    car = next((car for car in cars_db if car.id == car_id), None)
    
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    cars_db.remove(car)
    del car  # Llama automáticamente a __del__
    
    return {"message": f"Car {car_id} deleted"}
