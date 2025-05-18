
# 📄 Documentación del WebSocket con FastAPI

## 📌 Descripción General

Este módulo define una API WebSocket utilizando **FastAPI**, la cual permite la comunicación en tiempo real entre distintos tipos de clientes (`web`, `car`, `ia`). Dependiendo del tipo de cliente conectado, el servidor ejecuta distintas acciones definidas en módulos externos.

---

## 📂 Estructura del Código

### 1. Imports
```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from handlers.car import car_actions
from handlers.web2 import web_actions
from handlers.ia import ia_actions
from WSmanager import ConnectionManager
import asyncio
```

- Se importa FastAPI para manejo de WebSockets.
- Se importan las acciones específicas de cada tipo de cliente (`car`, `web`, `ia`).
- `ConnectionManager` se encarga de gestionar las conexiones activas.

---

### 2. Instanciación de Objetos

```python
router = APIRouter(tags=["WebSocket"])
manager = ConnectionManager()
```

- `router`: Contenedor de rutas para WebSocket.
- `manager`: Maneja todas las conexiones de los clientes, permitiendo agregarlas y eliminarlas.

---

## 🔄 Función `handle_client`

```python
async def handle_client(client_id: str, client_type: str, websocket: WebSocket):
```

### Propósito:
Gestiona los mensajes entrantes de un cliente y ejecuta la acción correspondiente.

### Parámetros:
- `client_id`: ID único del cliente.
- `client_type`: Tipo de cliente (`web`, `car`, `ia`).
- `websocket`: Conexión WebSocket abierta.

### Lógica:
- Se selecciona el diccionario de acciones basado en el tipo de cliente.
- Si el tipo es inválido, se cierra la conexión.
- Si es válido, entra en un bucle infinito:
  - Espera mensajes en formato JSON con una acción y parámetros.
  - Ejecuta la función correspondiente de `actions`.

---

## 🔌 WebSocket Endpoint

```python
@router.websocket("/ws/{client_type}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_type: str, client_id: str):
```

### Propósito:
Define el punto de conexión WebSocket para cualquier cliente, según su tipo e ID.

### Lógica:
- Acepta la conexión WebSocket.
- Registra al cliente en el `ConnectionManager`.
- Si el cliente es de tipo `web`, inicia el manejo de mensajes.
- Para otros tipos, mantiene la conexión abierta con un `sleep` infinito.
- Al desconectarse, elimina al cliente del `manager`.

---

## 📎 Endpoint Informativo (GET)

```python
@router.get("/ws/web/clientid")
def websocket_info():
```

### Propósito:
Proporciona información al cliente web sobre cómo conectarse e interactuar con el WebSocket.

### Respuesta:
- URL de conexión.
- Ejemplos de mensajes que puede enviar un cliente.
- Ejemplos de respuestas del servidor.

---

## 🔁 Ejemplo de Flujo

1. El cliente se conecta a:  
   `ws://localhost:8000/ws/web/abc123`

2. Envía el mensaje:
```json
{
  "action": "request_car",
  "params": {
    "origin": [10, 20],
    "destination": [30, 40]
  }
}
```

3. El servidor responde con:
```json
{
  "action": "car_selected",
  "params": {
    "carId": "car123",
    "path": [[10, 20], [15, 25], [20, 30]]
  }
}
```

4. Una vez el auto llega:
```json
{
  "action": "car_arrived",
  "params": {
    "carId": "car123",
    "path": [[30, 40], [35, 45], [40, 50]]
  }
}
```

5. El cliente envía:
```json
{ "action": "start_trip" }
```

6. El servidor responde al finalizar:
```json
{
  "action": "trip_finished",
  "params": {
    "carId": "car123"
  }
}
```

---

## 🧠 Notas Técnicas

- El manejo de acciones depende de los diccionarios importados (`car_actions`, `web_actions`, `ia_actions`).
- Las conexiones son gestionadas mediante una instancia compartida de `ConnectionManager`.
- Cada cliente tiene su propio ID y tipo, lo que permite tener múltiples conexiones diferenciadas.

---

---

## 🧠 Clase `ConnectionManager`

```python
from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {
            "web": {},
            "car": {},
            "ia": {}
        }

    def __getitem__(self, client_type: str) -> Dict[str, WebSocket]:
        return self.active_connections[client_type]

    def add(self, client_type: str, client_id: str, websocket: WebSocket):
        self.active_connections[client_type][client_id] = websocket

    def remove(self, client_type: str, client_id: str):
        self.active_connections[client_type].pop(client_id, None)

    def get(self, client_type: str, client_id: str) -> WebSocket | None:
        return self.active_connections[client_type].get(client_id)

    def has(self, client_type: str, client_id: str) -> bool:
        return client_id in self.active_connections[client_type]
```

### Propósito:
Gestiona todas las conexiones WebSocket activas organizadas por tipo de cliente (`web`, `car`, `ia`).

### Métodos:
- `__getitem__(client_type)`: Devuelve todas las conexiones activas de un tipo.
- `add(client_type, client_id, websocket)`: Registra una nueva conexión.
- `remove(client_type, client_id)`: Elimina una conexión por ID.
- `get(client_type, client_id)`: Obtiene una conexión específica.
- `has(client_type, client_id)`: Verifica si una conexión existe.

Este gestor permite acceder a conexiones activas por tipo de cliente e ID, facilitando la comunicación dirigida (por ejemplo, del servidor a un cliente específico).

---
