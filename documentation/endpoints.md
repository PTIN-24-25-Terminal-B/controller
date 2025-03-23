# Gestió de Cotxes - Documentació de Funcions

Aquest fitxer documenta les funcions relacionades amb la gestió de cotxes en una API REST. Les funcions realitzen operacions CRUD sobre una "base de dades" simulada amb una llista d'objectes (`cars_db`).

---

## `get_car_by_id(car_id: int)`

**Propòsit**: Obtenir les dades d'un cotxe específic pel seu ID.  

**Paràmetres**:
- `car_id` (int): ID únic del cotxe.

**Funcionament**:
1. Cerca el cotxe a `cars_db` amb una expressió generator:
   ```python
   car = next((car for car in cars_db if car.id == car_id), None)
   ```
2. Si no es troba (`if not car`), llança un error HTTP 404.
3. Retorna les dades del cotxe en format diccionari.

**Exemple de Resposta**:
```json
{
    "id": 1,
    "carType": "SUV",
    "seatCount": 5,
    "mileage": 15000.5,
    "completedRuns": 12
}
```

---

## `get_all_cars()`

**Propòsit**: Llistar tots els cotxes disponibles.  

**Funcionament**:
1. Comprova si `cars_db` està buida (`if not cars_db`). Si ho està, llança error 404.
2. Retorna una llista de diccionaris amb totes les dades dels cotxes.

**Exemple de Resposta**:
```json
[
    {"id": 1, "carType": "SUV", "seatCount": 5, "mileage": 15000.5, "completedRuns": 12},
    {"id": 2, "carType": "Sedan", "seatCount": 4, "mileage": 20000.0, "completedRuns": 8}
]
```

---

## `update_car(car_id: int, updated_data: dict)`

**Propòsit**: Actualitzar **tots** els camps modificables d'un cotxe (operació PUT).  

**Validacions**:
- Només permet camps: `carType`, `seatCount`, `mileage`, `completedRuns`.
- Rebutja camps no permesos amb error 400.

**Funcionament**:
1. Troba l'índex del cotxe a `cars_db`:
   ```python
   car_index = next((i for i, car in enumerate(cars_db) if car.id == car_id), None)
   ```
2. Si no es troba el cotxe, llança un error HTTP 404.
3. Actualitza el cotxe amb el mètode `modifyCar`:
   ```python
   car.modifyCar(
       newType=updated_data.get("carType"),
       newSeat=updated_data.get("seatCount"),
       newMileage=updated_data.get("mileage"),
       newRuns=updated_data.get("completedRuns")
   )
   ```

**Exemple d'Ús**:
```python
update_car(1, {"carType": "SUV", "seatCount": 7, "mileage": 20000.0, "completedRuns": 15})
```

---

## `partial_update_car(car_id: int, updated_data: dict)`

**Propòsit**: Actualitzar **només camps específics** d'un cotxe (operació PATCH).  

**Diferències amb `update_car`**:
- No requereix tots els camps.
- Modifica directament els atributs de l'objecte (no usa `modifyCar`).

**Funcionament**:
1. Troba el cotxe a `cars_db`:
   ```python
   car = next((car for car in cars_db if car.id == car_id), None)
   ```
2. Si no es troba, llança un error HTTP 404.
3. Actualitza només els camps proporcionats a `updated_data`.

**Exemple d'Ús**:
```python
partial_update_car(1, {"mileage": 20000.0})  # Actualitza només el quilometratge
```

---

## `create_car(car_data: dict)`

**Propòsit**: Crear un nou cotxe.  

**Camps Obligatoris**:
- `carType`: Tipus del cotxe (ex: "SUV").
- `seatCount`: Nombre de seients.

**Funcionament**:
1. Valida que els camps obligatoris estiguin presents:
   ```python
   required_fields = {"carType", "seatCount"}
   if not required_fields.issubset(car_data.keys()):
       raise HTTPException(status_code=400, detail="Faltan campos obligatorios: carType y seatCount")
   ```
2. Genera un ID nou incrementant el màxim existent:
   ```python
   new_id = max(car.id for car in cars_db) + 1 if cars_db else 1
   ```
3. Crea un objecte `carModel` amb valors per defecte:
   ```python
   new_car = carModel(
       id=new_id,
       carType=car_data["carType"],
       seatCount=car_data["seatCount"],
       mileage=car_data.get("mileage", 0.0),
       completedRuns=car_data.get("completedRuns", 0)
   )
   ```
4. Afegeix el nou cotxe a `cars_db`.

**Exemple d'Ús**:
```python
create_car({"carType": "SUV", "seatCount": 5})
```

---

## `delete_car(car_id: int)`

**Propòsit**: Eliminar un cotxe de la base de dades.  

**Funcionament**:
1. Troba el cotxe a `cars_db`:
   ```python
   car = next((car for car in cars_db if car.id == car_id), None)
   ```
2. Si no es troba, llança un error HTTP 404.
3. Elimina l'objecte de `cars_db` amb `cars_db.remove(car)`.
4. Executa `del car` per alliberar memòria (pot disparar el destructor `__del__`).

**Exemple de Resposta**:
```json
{
    "message": "Car 1 deleted"
}
```

---

## Estructura de la Base de Dades

- **Variable**: `cars_db` (llista d'objectes `carModel`).
- **Camps de cada Cotxe**:
  ```python
  class carModel:
      id: int
      carType: str
      seatCount: int
      mileage: float
      completedRuns: int
  ```

---

## Errors Comuns

- **404 Not Found**: Quan no es troba un cotxe o la base de dades està buida.
- **400 Bad Request**: Quan es proporcionen camps no vàlids o falten camps obligatoris.
