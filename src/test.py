from models.car_model import Car
import redis

def get_redis_connection():
    return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

r = get_redis_connection()


car1 = Car(
id="car600",
battery=85.5,
position=[1, 2], # Simple coordinate pair instead of Point object
working=True,
currentPath=[[1, 3], [2, 3], [3, 3]] # List of coordinate pairs
)

#Car.create_car(car1, r)

print(Car.read_all_cars(r))

#print (car1)