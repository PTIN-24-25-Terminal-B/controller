from models.user_model import User, UserState
from models.car_model import Car, CarState
from socket_manager import get_manager

car1 = Car(
    id="car1",
    battery=85.0,
    position=(22, 16),
    state=CarState.IDLE,
    userId=None,
    currentPath=None
)

car2 = Car(
    id="car2",
    battery=50.0,
    position=(0, 0)
)

Car.write_car(car1)
Car.write_car(car2)

car3 = Car.read_car("car1")

if car3.state == CarState.IDLE:
    print(car3)

Car.delete_car("car2")

cars: list[Car] = Car.read_all_cars()
for car in cars:
    if car.state == CarState.IDLE:
        print(car)

manager = get_manager()

for socket in manager["web"]:
    print(socket)

#print (car1)

#{"action": "request_car", "params": {"origin": [10, 10], "destination": [10, 10]}}

#wscat -c ws://localhost:8000/ws/web/123
