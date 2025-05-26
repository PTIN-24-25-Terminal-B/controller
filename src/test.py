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

Car.write_car(car1)

User.write_user(User(
    id="user1"
))
print(User.read_user("user1"))

manager = get_manager()

for socket in manager["web"]:
    print(socket)

#print (car1)

#{"action": "request_car", "params": {"origin": [10, 10], "destination": [10, 10]}}

#wscat -c ws://localhost:8000/ws/web/123
