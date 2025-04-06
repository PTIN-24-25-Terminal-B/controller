from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import Body
from models.car_model import Car, Point
from models.path_model import Point, Path
import models.car_model as car_model
import redis

def delete_car(car_id: str):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        deleted_count = car_model.delete_car(car_id, r)
        
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Car not found")
            
        return JSONResponse(
            content={"message": "Car deleted successfully"},
            status_code=200
        )
    except HTTPException as he:
        return he
    except Exception as e:
        return HTTPException(
            status_code=500,
            detail=f"Error deleting car: {str(e)}"
        )
    
def get_car(car_id: str):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        car = car_model.get_car(car_id, r)
        
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        
        # Convertir objeto Car a JSON
        car_data = {
            "id": car.id,
            "batery": car.batery,
            "position": {"x": car.position.x, "y": car.position.y},
            "working": car.working,
            "currentPath": {
                "id": car.currentPath.id,
                "points": [{"x": p.x, "y": p.y} for p in car.currentPath.path]
            } if car.currentPath else None
        }
        
        return JSONResponse(content=car_data, status_code=200)
    
    except HTTPException as he:
        return he
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error retrieving car: {str(e)}")
  
def edit_car(car_id: str, update_data: dict = Body(...)):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        
        # Parsear datos de actualización
        new_battery = update_data.get("batery")
        new_position_data = update_data.get("position")
        new_position = Point(x=new_position_data["x"], y=new_position_data["y"]) if new_position_data else None
        working_status = update_data.get("working")
        
        # Procesar ruta si existe
        current_path_data = update_data.get("currentPath")
        current_path = None
        if current_path_data:
            path_id = current_path_data.get("id")
            points = [Point(x=p["x"], y=p["y"]) for p in current_path_data.get("points", [])]
            current_path = Path(pathId=path_id, path=points)
        
        # Obtener coche existente
        car = car_model.get_car(car_id, r)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        
        # Aplicar cambios
        car.modifyCar(
            newBatery=new_battery,
            newPosition=new_position,
            working=working_status,
            currentPath=current_path
        )
        
        # Guardar cambios
        car_model.save_car(car, r)
        
        # Preparar respuesta
        updated_car = {
            "id": car.id,
            "batery": car.batery,
            "position": {"x": car.position.x, "y": car.position.y},
            "working": car.working,
            "currentPath": {
                "id": car.currentPath.id,
                "points": [{"x": p.x, "y": p.y} for p in car.currentPath.path]
            } if car.currentPath else None
        }
        
        return JSONResponse(content=updated_car, status_code=200)
    
    except KeyError as e:
        return HTTPException(status_code=400, detail=f"Invalid field: {str(e)}")
    except HTTPException as he:
        return he
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error updating car: {str(e)}")

def get_all_cars():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        cars = car_model.get_all_cars(r)
        
        # Convertir lista de objetos Car a JSON
        cars_data = []
        for car in cars:
            car_json = {
                "id": car.id,
                "batery": car.batery,
                "position": {"x": car.position.x, "y": car.position.y},
                "working": car.working,
                "currentPath": {
                    "id": car.currentPath.id,
                    "points": [{"x": p.x, "y": p.y} for p in car.currentPath.path]
                } if car.currentPath else None
            }
            cars_data.append(car_json)
        
        return JSONResponse(content={"cars": cars_data}, status_code=200)
    
    except Exception as e:
        return HTTPException(
            status_code=500,
            detail=f"Error retrieving cars: {str(e)}"
        )