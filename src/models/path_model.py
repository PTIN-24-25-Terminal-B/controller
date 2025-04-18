# Import required modules
from fastapi import HTTPException           # For handling HTTP-related errors (optional)
from pydantic import BaseModel, Field        # For creating validation and serialization classes
import json                                 # For converting Python objects to JSON strings
import redis                                # For interacting with a Redis database

# Represents a 2D point with float coordinates
class Point(BaseModel):
    x: float
    y: float

    def __str__(self):
        return json.dumps(self.model_dump())

    def to_dict(self):
        return self.model_dump()

# Factory function to create a Point instance
def toPoint(x: float, y: float):
    return Point(x=x, y=y)

# Represents a path made of multiple Point objects
class Path(BaseModel):
    id: str
    path: list[Point] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True 
        json_encoders = {
            Point: lambda p: p.model_dump()
        }

    def __str__(self):
        return json.dumps(self.model_dump(), indent=4)

    def to_dict(self):
        return self.model_dump()

    def addPoint(self, newPoint: Point):
        self.path.append(newPoint)
        return self

    def changePoint(self, index: int, pointToChange: Point):
        if index < len(self.path):
            self.path[index] = pointToChange
        else:
            print("list is shorter than index")
        return self

    def delPoint(self, index: int):
        if index < len(self.path):
            del self.path[index]
        else:
            print("list is shorter than index")
        return self

# =============================
# Functions for Redis interaction
# =============================

def read_all_paths(redis_conn):
    try:
        keys = redis_conn.keys('path:*')
        
        paths = []
        for key in keys:
            path_data = redis_conn.get(key)
            if path_data:
                path_dict = json.loads(path_data)
                paths.append(path_dict)
        
        return paths
    except Exception as e:
        raise ValueError(f"Error reading paths from database: {str(e)}")

def create_path(newPath: Path, redis_conn):
    try:
        key = f"path:{newPath.id}"
        value = newPath.model_dump_json(indent=4)
        
        if redis_conn.set(key, value, nx=True):
            return newPath
        else:
            raise ValueError("Path with given id already exists")
    except Exception as e:
        raise ValueError(f"Error adding path to database: {str(e)}")

def new_path(newPath: Path, redis_conn):
    try:
        key = f"path:{newPath.id}"
        value = newPath.model_dump_json(indent=4)
        
        if redis_conn.set(key, value, xx=True):
            return newPath
        else:
            raise ValueError("Path with given id does not exist")
    except Exception as e:
        raise ValueError(f"Error updating path in database: {str(e)}")

def delete_path(path_id: str, redis_conn):
    key = f"path:{path_id}"
    return redis_conn.delete(key) 
