
# 📘 Documentación: Acción `request_car` del Cliente Web

## 🧾 Descripción General

La acción `request_car` permite a un cliente de tipo `web` solicitar un coche disponible para viajar desde una coordenada de origen hasta una de destino. El servidor realiza las validaciones, selecciona un vehículo disponible, consulta rutas, coordina la comunicación con el vehículo y supervisa todo el ciclo del viaje.

---

## 🧪 Parámetros de Entrada

```json
{
  "action": "request_car",
  "params": {
    "origin": [10, 20],
    "destination": [30, 40]
  }
}
```

### Parámetros:
- `origin` (`[float, float]`): Coordenadas de inicio del viaje.
- `destination` (`[float, float]`): Coordenadas del destino final.

---

## 🔁 Flujo de Ejecución

1. **Validación de parámetros:** Se verifica que `origin` y `destination` sean listas válidas de dos números.
2. **Búsqueda de coches disponibles:** Se consultan en Redis los coches que no están trabajando (`working == False`).
3. **Petición al servicio de rutas** (`ROUTING_WS_URL`):
   - Primero se calcula la ruta desde cada coche hasta el usuario.
   - Luego, se calcula la ruta del usuario al destino.
4. **Selección del coche óptimo:** Basado en la ruta más corta desde coches al usuario.
5. **Notificación al cliente:** Se envía una respuesta `car_selected` con la ruta del coche al usuario.
6. **Comunicación con el coche:**
   - Se envía al coche la ruta hacia el usuario.
   - Se espera que el coche llegue y confirme (`trip_completed`).
7. **Inicio del viaje:**
   - El cliente debe confirmar con `start_trip`.
   - Se envía al coche la ruta hacia el destino.
8. **Finalización del viaje:** El coche confirma el fin del viaje, y se envía la acción `trip_finished`.

---

## 📤 Mensajes del Servidor al Cliente

### ✅ Confirmación de selección
```json
{
  "action": "car_selected",
  "params": {
    "carId": "car123",
    "path": [[10, 20], [15, 25], [20, 30]]
  }
}
```

### 🚗 Coche llegó al cliente
```json
{
  "action": "car_arrived",
  "params": {
    "car_id": "car123",
    "path": [[30, 40], [35, 45], [40, 50]]
  }
}
```

### 🏁 Viaje finalizado
```json
{
  "action": "trip_finished",
  "params": {
    "car_id": "car123"
  }
}
```

---

## ⚠️ Posibles Errores

- `"Invalid or missing origin/destination format"`: Coordenadas malformadas.
- `"Routing service error"`: Fallo en la conexión con el servicio de rutas.
- `"Error connecting with car"`: No se pudo comunicar con el coche seleccionado.

---

## 🧱 Dependencias y Componentes Clave

- `Car.read_all_cars(redis)`: Obtiene el listado de coches.
- `websockets.connect(...)`: Comunicación con servicio de rutas externo.
- `ConnectionManager`: Maneja conexiones WebSocket de clientes y coches.
- `models.car_model.Car`: Modelo de datos de coches.

---

## ✅ Conclusión

La acción `request_car` es el corazón del sistema de transporte automatizado. Orquesta múltiples componentes para emparejar usuarios con vehículos en tiempo real, garantizando una experiencia fluida y dinámica.

