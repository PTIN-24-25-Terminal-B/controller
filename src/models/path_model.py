# Import required modules
from fastapi import HTTPException           # For handling HTTP-related errors (not used in this snippet)
from dataclasses import dataclass, asdict   # For creating simple data containers and converting them to dicts
import json                                 # For converting Python objects to JSON strings
import redis                                # For interacting with a Redis database (currently unused)

# Represents a 2D point with float coordinates
@dataclass
class Point:
    x: float
    y: float

    def __str__(self):
        return json.dumps(asdict(self))

# Factory function to create a Point instance
def toPoint(x: float, y: float):
    return Point(x, y)

# Represents a path made of multiple Point objects
class Path:
    def __init__(self, pathId: str, path: list[Point]):
        self.id = pathId       # Unique identifier for the path
        self.path = path       # Internal list of Point objects

    # String representation of the path in JSON format
    def __str__(self):
        return json.dumps({
            "id": self.id,
            "points": [asdict(p) for p in self.path]
        }, indent=4)

    # Destructor method (not doing anything currently)
    def __del__(self):       
        return

    # Add a new point to the path
    def addPoint(self, newPoint: Point):
        self.path.append(newPoint)
        return self  # Enables method chaining

    # Replace the point at a given index with a new one
    def changePoint(self, index: int, pointToChange: Point):
        if index < len(self.path):
            self.path[index] = pointToChange
        else:
            print("list is shorter than index")
        return self  # Enables method chaining

    # Delete the point at the specified index
    def delPoint(self, index):
        if index < len(self.path):
            del self.path[index]
        else:
            print("list is shorter than index")
        return self  # Enables method chaining


def create_path(newPath: Path, redis_conn):
        key = f"path:{newPath.id}"
        value = json.dumps({
            "id": newPath.id,
            "points": [asdict(p) for p in newPath.path]
        })
        redis_conn.set(key, value)
        return newPath

def read_all_paths(redis_conn):
    try:
        # Obtenir totes les claus que comencen amb 'path:'
        keys = redis_conn.keys('path:*')
        
        paths = []
        for key in keys:
            # Obtenir el valor de cada clau
            path_data = redis_conn.get(key)
            if path_data:
                # Convertir de JSON a diccionari
                path_dict = json.loads(path_data)
                paths.append(path_dict)
        
        return paths
    except Exception as e:
        raise ValueError(f"Error reading paths from Redis: {str(e)}")
def delete_path(path_id: str, redis_conn):
    key = f"path:{path_id}"
    return redis_conn.delete(key)  # Retorna 1 si s'esborra, 0 si no existeix
