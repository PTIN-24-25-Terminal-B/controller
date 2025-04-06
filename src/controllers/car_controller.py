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
  
    
