from models.user_model import User, UserState
from models.car_model import Car, CarState
from socket_manager import get_manager
import pydantic
car1234 = Car(
    id="car1234",
    battery=85.0,
    position=(35, 90),
    state=CarState.TRAVELING,
    userId="1000",
    currentPath=[[22,50],[22,51],[22,52],[22,53],[22,54],[22,55],[22,56],[22,57],[22,58],[22,59],[22,60],[22,61],[22,62],[22,63],[22,64],[22,65],[22,66],[22,67],[22,68],[22,69],[22,70],[22,71],[22,72],[22,73],[22,74],[22,75],[22,76],[22,77],[22,78],[22,79],[22,80],[22,81],[22,82],[22,83],[22,84],[22,85],[22,86],[22,87],[22,88],[23,89],[24,89],[25,89],[26,89],[27,89],[28,89],[29,89],[30,89],[31,89],[32,89],[33,89],[34,89],[35,90],[35,91],[35,92],[35,93],[35,94],[35,95],[35,96],[35,97],[35,98],[35,99],[35,100],[35,101],[35,102],[35,103],[35,104],[35,105],[35,106],[35,107],[36,108],[37,109],[38,109],[39,109],[40,109],[41,109],[42,109],[43,109]]
)
#
Car.write_car(car1234)
#Car.delete_car("car1234")
#
#User.write_user(User(
#    id="user1"
#))
print(Car.read_all_cars())
#
#manager = get_manager()
#
#for socket in manager["web"]:
#    print(socket)

#print (car1)

#{"action": "request_car", "params": {"origin": [42,88], "destination": [10, 10]}}

#{"action": "request_car", "params": {"carId": "0", "position": [10, 10]}}

#wscat -c ws://localhost:8000/ws/web/123
