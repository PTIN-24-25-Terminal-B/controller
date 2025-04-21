from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
import redis
import uuid
import random

router = APIRouter()

# ────────────────────────────────────────────────────────────────────────────────
# Simulació de gestió de contenidors i màquines virtuals
# ────────────────────────────────────────────────────────────────────────────────

@router.post("/vm")
def create_virtual_machine():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        vm_id = str(uuid.uuid4())
        r.sadd("vms", vm_id)
        r.set(f"vm:{vm_id}", "active")
        r.delete(f"vm:{vm_id}:containers")
        return JSONResponse(content={"vm_id": vm_id, "status": "created"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vm/{vm_id}/container")
def create_container(vm_id: str, config: dict = Body(...)):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        if not r.exists(f"vm:{vm_id}"):
            raise HTTPException(status_code=404, detail="VM not found")

        container_id = str(uuid.uuid4())
        r.hset(f"container:{container_id}", mapping={
            "status": "running",
            "cpu": str(random.randint(1, 100)),
            "memory": str(random.randint(50, 500)),
            "network": str(random.randint(0, 1000)),
            "logs": "Container created",
            "vm": vm_id
        })
        r.rpush(f"vm:{vm_id}:containers", container_id)
        return JSONResponse(content={"container_id": container_id, "status": "created"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vm/{vm_id}/containers")
def list_containers(vm_id: str):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        if not r.exists(f"vm:{vm_id}"):
            raise HTTPException(status_code=404, detail="VM not found")

        container_ids = r.lrange(f"vm:{vm_id}:containers", 0, -1)
        containers = []
        for cid in container_ids:
            cid = cid.decode("utf-8")
            data = r.hgetall(f"container:{cid}")
            container_info = {k.decode("utf-8"): v.decode("utf-8") for k, v in data.items()}
            container_info["id"] = cid
            containers.append(container_info)

        return JSONResponse(content={"vm_id": vm_id, "containers": containers}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/vm/{vm_id}/container/{container_id}")
def delete_container(vm_id: str, container_id: str):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        if not r.exists(f"container:{container_id}"):
            raise HTTPException(status_code=404, detail="Container not found")

        r.delete(f"container:{container_id}")
        r.lrem(f"vm:{vm_id}:containers", 0, container_id)
        return JSONResponse(content={"message": "Container deleted"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/container/{container_id}/status")
def container_status(container_id: str):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        if not r.exists(f"container:{container_id}"):
            raise HTTPException(status_code=404, detail="Container not found")

        data = r.hgetall(f"container:{container_id}")
        info = {k.decode("utf-8"): v.decode("utf-8") for k, v in data.items()}
        return JSONResponse(content={"container_id": container_id, "info": info}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/container/{container_id}/restart")
def restart_container(container_id: str):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        if not r.exists(f"container:{container_id}"):
            raise HTTPException(status_code=404, detail="Container not found")

        r.hset(f"container:{container_id}", "status", "restarting")
        return JSONResponse(content={"container_id": container_id, "status": "restarting"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/container/{container_id}/update")
def update_container(container_id: str, config: dict = Body(...)):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        if not r.exists(f"container:{container_id}"):
            raise HTTPException(status_code=404, detail="Container not found")

        for key, value in config.items():
            r.hset(f"container:{container_id}", key, str(value))

        r.hset(f"container:{container_id}", "status", "updated")
        return JSONResponse(content={"container_id": container_id, "status": "updated"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vm/{vm_id}/scale")
def scale_vm(vm_id: str, scale_count: int = Body(...)):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        if not r.exists(f"vm:{vm_id}"):
            raise HTTPException(status_code=404, detail="VM not found")

        created = []
        for _ in range(scale_count):
            container_id = str(uuid.uuid4())
            r.hset(f"container:{container_id}", mapping={
                "status": "running",
                "cpu": str(random.randint(1, 100)),
                "memory": str(random.randint(50, 500)),
                "network": str(random.randint(0, 1000)),
                "logs": "Scaled container created",
                "vm": vm_id
            })
            r.rpush(f"vm:{vm_id}:containers", container_id)
            created.append(container_id)

        return JSONResponse(content={"scaled": created}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vm/{vm_id}/isolation-check")
def check_vm_isolation(vm_id: str):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        if not r.exists(f"vm:{vm_id}"):
            raise HTTPException(status_code=404, detail="VM not found")

        container_ids = r.lrange(f"vm:{vm_id}:containers", 0, -1)
        isolation_report = {}

        for cid in container_ids:
            cid = cid.decode("utf-8")
            container_key = f"container:{cid}"
            if not r.exists(container_key):
                isolation_report[cid] = "missing"
                continue

            container_data = r.hgetall(container_key)
            # Simulació d’aïllament correcte
            isolation_report[cid] = "aïllament correcte"

        return JSONResponse(content={"isolation_status": isolation_report}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking isolation: {str(e)}")
