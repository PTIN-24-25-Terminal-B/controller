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
        
# Repositorio de recorruts
# Pot ser subsituit per accés una BD de Redis
paths_repo = {}

def delete_path(path_id: str):
    if path_id in paths_repo:
        del paths_repo[path_id]
        return {"message": f"Recorregut {path_id} eliminado correctamente."}
    else:
        raise HTTPException(status_code=404, detail="Recorregut no encontrado")
    