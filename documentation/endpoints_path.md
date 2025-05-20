# Gestió de Rutes - Documentació de Funcions

Aquest fitxer documenta les funcions relacionades amb la gestió de rutes en una API REST. Les funcions permeten crear rutes a partir de punts d’inici i final, i emmagatzemar-les a Redis com a "base de dades" simulada.

---

## `create_path(x0: float, y0: float, x1: float, y1: float)`

**Propòsit**: Crear una nova ruta entre dues coordenades i desar-la a Redis.**Flux de treball**: `request ➜ route ➜ controller ➜ model ➜ controller ➜ response`

---

### 1. **Request**

**Mètode HTTP**: `POST`**Endpoint**: `/paths/`**Paràmetres (query o JSON body)**:

- `x0`, `y0`: coordenades d’origen (`float`)
- `x1`, `y1`: coordenades de destí (`float`)

---

### 2. **Route Layer**

```python
@router.post("/")
async def get_cars(x0: float, y0: float, x1: float, y1: float):
    return path_controller.create_path(x0, y0, x1, y1)
```

- Rep els paràmetres del client.
- Passa les coordenades al controlador `create_path`.

---

### 3. **Controller Layer**

```python
def create_path(x0: float, y0: float, x1: float, y1: float):
    ...
```

**Funcionament**:

1. **Validació**:

   - Comprova que totes les coordenades siguin `float`.
   - Comprova que estiguin dins l’interval `[0, 100]`.     Si no compleixen, es retorna un error `HTTP 400`.

2. **Creació de la ruta**:

   - Crea un objecte `Path` amb dues coordenades (`from`, `to`).

3. **Desament**:

   - Crea una connexió amb Redis.
   - Truca a `path_model.create_path(...)` per guardar-la.

4. **Resposta**:

   - Retorna un missatge de confirmació (`HTTP 200`) si té èxit.
   - Captura i retorna errors (`HTTP 400`, `HTTP 500`) si cal.

---

### 4. **Model Layer**

```python
def create_path(newPath: Path, redis_conn):
    ...
```

**Funcionament**:

1. Construeix la clau Redis amb format `path:{id}`.
2. Serialitza l’objecte `Path` a JSON (incloent els punts).
3. Desa la ruta a Redis mitjançant `.set()`.

**Error Handling**:

- Si hi ha algun error, retorna un `ValueError` amb informació addicional.

---

### 5. **Resposta Exemple**

**Èxit** (`HTTP 200`):

```json
{
    "message": "path created succesfully"
}
```

**Error de Validació** (`HTTP 400`):

```json
{
    "detail": "coordinates do not fit in the map"
}
```

**Error Intern** (`HTTP 500`):

```json
{
    "detail": "Error reading adding path to database: connection refused"
}
```

---

## `read_all_paths()`

**Propòsit**: Recuperar totes les rutes emmagatzemades al sistema.  
**Flux de treball**: `request ➜ route ➜ controller ➜ model ➜ controller ➜ response`

---

### 1. **Request**

**Mètode HTTP**: `GET`  
**Endpoint**: `/paths/`  
**Paràmetres**: Cap

---

### 2. **Route Layer**

```python
@router.get("/")
async def get_all_paths():
    return path_controller.read_all_paths()
```

- Gestiona les peticions GET a l'endpoint base.
- Crida al controlador `read_all_paths` sense necessitat de paràmetres.

---

### 3. **Controller Layer**

```python
def read_all_paths():
    ...
```

**Funcionament**:

1. **Connexió a Redis**:
   - Estableix la connexió amb Redis (mateixa configuració que `create_path`).

2. **Recuperació de dades**:
   - Crida a `path_model.read_all_paths()` per obtenir totes les rutes.

3. **Resposta**:
   - Retorna les rutes en format JSON amb codi `HTTP 200` si té èxit.
   - Captura i retorna errors interns amb codi `HTTP 500`.

---

### 4. **Model Layer**

```python
def read_all_paths(redis_conn):
    ...
```

**Funcionament**:

1. **Consulta a Redis**:
   - Busca totes les claus amb patró `path:*` mitjançant `.keys()`.
   - Per cada clau, obté el valor serialitzat en JSON.

2. **Processament**:
   - Desserialitza cada ruta de JSON a diccionari Python.
   - Afegeix les rutes a una llista de retorn.

**Error Handling**:
- Si hi ha errors en la connexió o consulta, llança `ValueError`.

---

### 5. **Resposta Exemple**

**Èxit** (`HTTP 200`):

```json
{
    "paths": [
        {
            "id": "path123",
            "points": [
                {"x": 10.5, "y": 20.3},
                {"x": 11.2, "y": 21.0}
            ]
        },
        {
            "id": "path456",
            "points": [
                {"x": 15.0, "y": 25.5},
                {"x": 16.0, "y": 26.5}
            ]
        }
    ]
}
```

**Error Intern** (`HTTP 500`):

```json
{
    "detail": "Error reading paths from Redis: connection timeout"
}
```

## `delete_path(path_id: str)`

**Propòsit**: Eliminar una ruta existent identificada pel seu `path_id` emmagatzemada a Redis.  
**Flux de treball**: `request ➜ route ➜ controller ➜ model ➜ controller ➜ response`

---

### 1. **Request**

**Mètode HTTP**: `DELETE`  
**Endpoint**: `/paths/{path_id}`  
**Paràmetres**:  
- `path_id`: Identificador únic de la ruta a eliminar (`string`)

---

### 2. **Route Layer**

```python
@router.delete("/{path_id}")
async def delete_path_endpoint(path_id: str):
    return path_controller.delete_path(path_id)
```

- Rep el paràmetre `path_id` de la sol·licitud.
- Invoca la funció `delete_path` del controlador passant el `path_id`.

---

### 3. **Controller Layer**

```python
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
```

**Funcionament**:

1. **Connexió a Redis**:  
   - Estableix una connexió amb la base de dades Redis.

2. **Eliminació de la ruta**:  
   - Crida a `path_model.delete_path(path_id, r)` per eliminar la clau `path:{path_id}`.  
   - Si `delete` retorna `0`, significa que la ruta no existia, i es llança un error `HTTP 404`.

3. **Resposta**:  
   - Si l'eliminació és exitosa, retorna un missatge de confirmació (`HTTP 200`).  
   - Captura errors específics (`HTTP 404` i `HTTP 500`) i retorna la resposta adequada.

---

### 4. **Model Layer**

```python
def delete_path(path_id: str, redis_conn):
    key = f"path:{path_id}"
    return redis_conn.delete(key)  # Retorna 1 si s'elimina, 0 si no existeix
```

**Funcionament**:

1. **Construcció de la clau**:  
   - La clau a eliminar es construeix amb el format `path:{path_id}`.

2. **Eliminació de la ruta**:  
   - Executa la funció `.delete()` de Redis per eliminar la clau.
   - Retorna `1` si s'ha eliminat la ruta o `0` si la ruta no existia.

**Error Handling**:  
- Si hi ha algun error en la comunicació amb Redis, es captura i es retorna un error intern (`HTTP 500`).

---

### 5. **Respostes Exemple**

**Èxit** (`HTTP 200`):

```json
{
    "message": "Path deleted successfully"
}
```

**Error de Ruta No Trobada** (`HTTP 404`):

```json
{
    "detail": "Path not found"
}
```

**Error Intern** (`HTTP 500`):

```json
{
    "detail": "Error deleting path: <error message>"
}
```
