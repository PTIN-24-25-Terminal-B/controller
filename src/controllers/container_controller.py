from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Container(BaseModel):
    id: str
    config: dict

# Crear contenidor
@router.post("/container")
def create_container(container: Container):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        key = f"container:{container.id}"

        if r.exists(key):
            raise HTTPException(status_code=400, detail="Container already exists")

        r.hset(key, mapping={"config": str(container.config)})
        return JSONResponse(content={"message": "Container created"}, status_code=201)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error creating container: {str(e)}")

# Consultar contenidor
@router.get("/container/{container_id}")
def get_container(container_id: str):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        key = f"container:{container_id}"

        if not r.exists(key):
            raise HTTPException(status_code=404, detail="Container not found")

        config = eval(r.hget(key, "config").decode("utf-8"))
        return JSONResponse(content={"id": container_id, "config": config}, status_code=200)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error retrieving container: {str(e)}")

# Configurar contenidor (editar)
@router.put("/container/{container_id}")
def update_container(container_id: str, config: dict = Body(...)):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        key = f"container:{container_id}"

        if not r.exists(key):
            raise HTTPException(status_code=404, detail="Container not found")

        r.hset(key, mapping={"config": str(config)})
        return JSONResponse(content={"message": "Container updated"}, status_code=200)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error updating container: {str(e)}")

# Eliminar contenidor
@router.delete("/container/{container_id}")
def delete_container(container_id: str):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        key = f"container:{container_id}"

        deleted = r.delete(key)
        if deleted == 0:
            raise HTTPException(status_code=404, detail="Container not found")

        return JSONResponse(content={"message": "Container deleted"}, status_code=200)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error deleting container: {str(e)}")
