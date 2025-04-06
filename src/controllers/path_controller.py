# controller/path_controller.py

from fastapi import HTTPException
from models.path_model import Path

# Repositorio de recorruts
# Pot ser subsituit per accés una BD de Redis
paths_repo = {}

def delete_path(path_id: str):
    if path_id in paths_repo:
        del paths_repo[path_id]
        return {"message": f"Recorregut {path_id} eliminado correctamente."}
    else:
        raise HTTPException(status_code=404, detail="Recorregut no encontrado")
