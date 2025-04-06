from models.path_model import Path
from models.path_model import Point
import models.path_model as path_model

carId = 1234

point1 = Point(1.3, 3)
point2 = Point(7.1, 3)
print(point1.x, point1.y)

print(point1)

path1 = Path("asd123", [point1, point2])

print(path1)

path1.addPoint(point1)

print(path1)

path1.changePoint(2, path_model.toPoint(2.2, 1.3))

print(path1)

path1.delPoint(1)

print(path1)