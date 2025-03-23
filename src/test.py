from models.car_model import carModel

carId = 1234

car1 = carModel(4, "sedan", id=carId)

print(car1)

car1.completeRun(12)

print(car1)