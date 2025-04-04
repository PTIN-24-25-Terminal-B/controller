from fastapi import HTTPException
from dataclasses import dataclass, asdict
from typing import List
import string
import json
import redis

@dataclass
class Point:
    x: float
    y: float

def toPoint(x: float,y: float):
    return Point(x, y)

class path :
    def __init__(self, pathId: string, path: List[Point]):
        self.id = pathId
        self.coordList = path
        return
    
    def __str__(self):
        return json.dumps({
            "points": [asdict(p) for p in self.points]
        }, indent=4)

    def __delattr__(self):       
        return
    
    def addPoint(self, newPoint: Point):
        self.coordList.append(Point)
        return path