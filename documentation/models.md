# Database Models

The models use the structure from the database and atributes as follows:

## carModel

The `carModel` represents a vehicle and contains the following attributes:

### **Attributes**
* `id` (string | None) - A unique identifier for the car.
* `seatCount` (integer) - The number of seats in the car.
* `carType` (string) - The type of car (e.g., sedan, SUV).
* `mileage` (float) - The total distance the car has traveled.
* `completedRuns` (integer) - The number of completed trips.

---

### **Methods**

#### `__init__(carType: str, seatCount: int, id: str = None, mileage: float = 0.0, completedRuns: int = 0)`
**Description:**  
Initializes a new car model instance.

**Parameters:**
- `carType` (string) – The type of the car.
- `seatCount` (integer) – The number of seats in the car.
- `id` (string | None) – The car's unique identifier (default: `None`).
- `mileage` (float) – The initial mileage of the car (default: `0.0`).
- `completedRuns` (integer) – The number of completed trips (default: `0`).

**Returns:**  
- `None`

---

#### `__str__() -> str`
**Description:**  
Returns a JSON-formatted string representation of the car model.

**Returns:**  
- `str`: The object’s data in JSON format.

**Example Output:**
```json
{
    "id": "abc123",
    "seatCount": 4,
    "carType": "Sedan",
    "mileage": 12000.5,
    "completedRuns": 30
}
```

---

#### `completeRun(miles: float = 0.0) -> None`
**Description:**
Adds a new completed run and increases the car's mileage

**Returns:**
- `None`

---

### `modifyCar(newType: str = None, newSeat: int = None, newId: str = None, newMileage: float = None, newRuns: int = None) -> None`

**Description:**
Allows modification of any stored data in the car model.
**Warning:** Changing the `id` may cause issues such as maing the car untracable or modifying another car's values.

**Parameters:**
- `newId` (string | None) – The new identifier.
- `newType` (string | None) – The new car type.
- `newSeat` (integer | None) – The new number of seats.
- `newMileage` (float | None) – The new mileage.
- `newRuns` (integer | None) – The new number of completed runs.

**Returns**
- `None`

---

### `__del__() -> None`

**Desription:**
Destructor method called when the object is deleted. This currently does nothing and can be omitted unless you plan to implement cleanup logic.

**Returns**
- `None`