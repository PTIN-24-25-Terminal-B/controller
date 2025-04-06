# Database Models

The models use the structure from the database and atributes as follows:

## Car

The `Car` class represents a vehicle in the system and contains information such as its battery level, current position, and path status.

---

### **Attributes**

- `id` (string): A unique identifier for the car.
- `batery` (float): The remaining battery level of the car.
- `position` (Point): The current position of the car (from `path_model.Point`).
- `working` (bool): Indicates whether the car is currently in operation.
- `currentPath` (Path | None): The current assigned path of the car, if any (from `path_model.Path`).

---

### **Methods**

#### `__init__(id: str, batery: float, position: Point, working: bool, currentPath: Path = None)`
**Description:**  
Initializes a new car instance with its ID, battery, position, working status, and optional path.

**Parameters:**
- `id` (string) – The car's unique identifier.
- `batery` (float) – The battery percentage or charge of the car.
- `position` (Point) – A Point object representing the car's current location.
- `working` (bool) – Indicates whether the car is in use.
- `currentPath` (Path | None) – The path assigned to the car, if any.

**Returns:**  
- `None`

---

#### `__str__() -> str`
**Description:**  
Returns a JSON-formatted string representation of the car instance.

**Returns:**  
- `str`: The object's data in JSON format.

**Example Output:**
```json
{
    "id": "abc123",
    "batery": 78.5,
    "position": {
        "x": 12.3,
        "y": 45.6
    },
    "working": true,
    "currentPath": {
        "id": "path001",
        "points": [
            {"x": 12.3, "y": 45.6},
            {"x": 20.0, "y": 30.0}
        ]
    }
}
```

---

#### `modifyCar(newBatery: float = None, newPosition: Point = None, working: bool = None, currentPath: Path = None) -> Self`
**Description:**  
Allows modification of any stored data in the car instance.

**Warning:** Changing the `id` is not allowed in this method and should be handled carefully elsewhere if required.

**Parameters:**
- `newBatery` (float | None) – New battery level.
- `newPosition` (Point | None) – New car position.
- `working` (bool | None) – Update working status.
- `currentPath` (Path | None) – Assign a new path.

**Returns:**  
- `Self`: The updated car object.

---

#### `__del__() -> None`
**Description:**  
Destructor method called when the object is deleted. Currently does nothing.

**Returns:**  
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