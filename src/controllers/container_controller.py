from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Container(BaseModel):
    id: str
    config: dict

class VirtualMachine(BaseModel):
    id: str
    name: str
    ip: str

@router.post("/vm")
def create_vm(vm: VirtualMachine):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        key = f"vm:{vm.id}"
        if r.exists(key):
            raise HTTPException(status_code=400, detail="VM already exists")
        r.hset(key, mapping={"name": vm.name, "ip": vm.ip})
        return JSONResponse(content={"message": "VM created"}, status_code=201)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error creating VM: {str(e)}")

@router.post("/vm/{vm_id}/container")
def add_container_to_vm(vm_id: str, container: Container):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        vm_key = f"vm:{vm_id}"
        if not r.exists(vm_key):
            raise HTTPException(status_code=404, detail="VM not found")
        container_key = f"container:{container.id}"
        if r.exists(container_key):
            raise HTTPException(status_code=400, detail="Container already exists")
        r.hset(container_key, mapping={"config": str(container.config)})
        r.rpush(f"vm:{vm_id}:containers", container.id)
        return JSONResponse(content={"message": "Container added to VM"}, status_code=201)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error adding container: {str(e)}")

@router.get("/vm/{vm_id}/containers")
def list_vm_containers(vm_id: str):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        if not r.exists(f"vm:{vm_id}"):
            raise HTTPException(status_code=404, detail="VM not found")
        container_ids = r.lrange(f"vm:{vm_id}:containers", 0, -1)
        container_data = []
        for cid in container_ids:
            cid = cid.decode("utf-8")
            key = f"container:{cid}"
            if r.exists(key):
                config = eval(r.hget(key, "config").decode("utf-8"))
                container_data.append({"id": cid, "config": config})
        return JSONResponse(content={"containers": container_data}, status_code=200)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error listing containers: {str(e)}")

@router.delete("/vm/{vm_id}/container/{container_id}")
def delete_container_from_vm(vm_id: str, container_id: str):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        if not r.exists(f"vm:{vm_id}"):
            raise HTTPException(status_code=404, detail="VM not found")
        r.delete(f"container:{container_id}")
        r.lrem(f"vm:{vm_id}:containers", 0, container_id)
        return JSONResponse(content={"message": "Container deleted from VM"}, status_code=200)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error deleting container: {str(e)}")
