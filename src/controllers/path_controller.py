from fastapi.responses import JSONResponse
from fastapi import HTTPException
from models.path_model import Point, Path
import requests
import models.path_model as path_model
import uuid
import redis

def read_all_paths():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)  # Same connection as create
        
        paths: list[Path] = path_model.read_all_paths(r)
        return paths

    except (ValueError, TypeError, HTTPException) as e:
        if isinstance(e, HTTPException):
            return e
        else:
            return HTTPException(status_code=500, detail=e)

def create_path(point_list: list[Point]):
    try:
        if len(point_list) < 2:
            raise HTTPException(status_code=400, detail="At least two points are required")

        print({"start": point_list[0], "goal": point_list[1]})

#        res = requests.post("http://api_pathfinding:5000/set-checkpoints", json={"start": point_list[0].model_dump(), "goal": point_list[1].model_dump()})
#
 #       print ("this is the new path: ", res)
#
 #       if(res.ok):
  #          data = res.json()
   #         print(data)
    #    else:
     #       print(res.text)
        print(point_list)
        new_path = Path(
            id=str(uuid.uuid4()),
            path=point_list
        )


        ##Add path to DB, maybe temporary
        r = redis.Redis(host='localhost', port=6379, db=0)
        path_model.create_path(new_path, r)
        print(new_path)
        return JSONResponse(new_path.model_dump_json(), status_code=200)

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

def update_path(path_obj: Path):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)

        updated = path_model.update_path(path_obj, r)
        if not updated:
            raise HTTPException(status_code=404, detail="Path not found")

        return JSONResponse(content={"message": "Path updated successfully"}, status_code=200)

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
    except (ValueError, TypeError, HTTPException) as e:
        if isinstance(e, HTTPException):
            return e
        else:
            return HTTPException(status_code=500, detail=e)