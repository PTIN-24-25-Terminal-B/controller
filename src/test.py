from models.car_model import Car
import redis

def get_redis_connection():
    return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

r = get_redis_connection()


print("\n\n")

print (Car.read_all_cars(r)[0].id)