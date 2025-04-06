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

---
---

## Point

The `Point` represents a coordinate in 2D space.

### **Attributes**
* `x` (float) - The X-axis coordinate.
* `y` (float) - The Y-axis coordinate.

---

### **Methods**

#### `__str__() -> str`
**Description:**  
Returns a JSON-formatted string representation of the point.

**Returns:**  
- `str`: The object’s data in JSON format.

**Example Output:**
```json
{
    "x": 1.5,
    "y": 3.2
}
```

---

## toPoint

A factory function for creating `Point` instances.

---

### **Signature**
```python
toPoint(x: float, y: float) -> Point
```

**Description:**  
Creates a new `Point` object with the given coordinates.

**Parameters:**
- `x` (float) – The X coordinate.
- `y` (float) – The Y coordinate.

**Returns:**  
- `Point`: A new `Point` instance.

---
---

## Path

The `Path` represents a collection of `Point` instances forming a route or trajectory.

### **Attributes**
* `id` (string) - A unique identifier for the path.
* `path` (list of `Point`) - A list of points forming the path.

---

### **Methods**

#### `__init__(pathId: str, path: list[Point])`
**Description:**  
Initializes a new path with an identifier and a list of points.

**Parameters:**
- `pathId` (string) – The path's unique identifier.
- `path` (list[Point]) – A list of Point objects.

**Returns:**  
- `None`

---

#### `__str__() -> str`
**Description:**  
Returns a JSON-formatted string representation of the path, including all points.

**Returns:**  
- `str`: A JSON representation of the path and its points.

**Example Output:**
```json
{
    "id": "path01",
    "points": [
        {
            "x": 1.0,
            "y": 2.0
        },
        {
            "x": 3.5,
            "y": 4.1
        }
    ]
}
```

---

#### `addPoint(newPoint: Point) -> Path`
**Description:**  
Adds a new point to the path.

**Parameters:**
- `newPoint` (Point) – A new point to add to the path.

**Returns:**  
- `Path`: The updated path (to allow method chaining).

---

#### `changePoint(index: int, pointToChange: Point) -> Path`
**Description:**  
Replaces the point at the specified index with a new point.

**Parameters:**
- `index` (int) – The position of the point to replace.
- `pointToChange` (Point) – The new point to insert.

**Returns:**  
- `Path`: The updated path (to allow method chaining).

**Note:**  
If the index is out of bounds, a warning is printed and no change occurs.

---

#### `delPoint(index: int) -> Path`
**Description:**  
Deletes the point at the specified index from the path.

**Parameters:**
- `index` (int) – The index of the point to delete.

**Returns:**  
- `Path`: The updated path (to allow method chaining).

**Note:**  
If the index is out of bounds, a warning is printed and no deletion occurs.

---

#### `__del__() -> None`
**Description:**  
Destructor method called when the object is deleted. This currently does nothing and can be omitted unless you plan to implement cleanup logic.

**Returns:**  
- `None`