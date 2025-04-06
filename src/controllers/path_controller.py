from fastapi.responses import JSONResponse
from fastapi import HTTPException
from models.path_model import Point, Path
import models.path_model as path_model
import redis

def create_path(x0: float, y0: float, x1:float, y1: float):
    try:
        for item in [x0, y0, x1, y1]:
            if not isinstance(item, float):
                raise HTTPException(status_code=400, detail="input data has to be float")
            if item > 100 or item < 0: ##temporary coordinate max and min values
                raise HTTPException(status_code=400, detail="coordinates do not fit in the map")
        
        newPath = Path("", [path_model.toPoint(x0, y0), path_model.toPoint(x1, y1)])
        ##here call to AI to make the path from the end and start points

        r = redis.Redis(host='localhost', port=6379, db=0) ##placeholder db connection, not real variables

        path_model.create_path(newPath, r)

        return JSONResponse(content={"message": "path created succesfully"}, status_code=200)
    except (ValueError, TypeError, HTTPException) as e:
        if isinstance(e, HTTPException):
            return e
        else:
            return HTTPException(status_code=500, detail=e)

def read_all_paths():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)  # Same connection as create
        
        paths = path_model.read_all_paths(r)
        
        return JSONResponse(content={"paths": paths}, status_code=200)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
        
def delete_path(path_id: str):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        deleted_count = path_model.delete_path(path_id, r)
        
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Path not found")
            
        return JSONResponse(
            content={"message": "Path deleted successfully"},
            status_code=200
        )
    except HTTPException as he:
        return he
    except Exception as e:
        return HTTPException(
            status_code=500,
            detail=f"Error deleting path: {str(e)}"
        )