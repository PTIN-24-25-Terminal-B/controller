import json

class carModel:
    # variable types: carModel(integer, string, string, float, integer)
    def __init__(self, carType, seatCount, id=None, mileage=0.0, completedRuns=0):
        self.id = id
        self.seatCount = seatCount
        self.carType = carType
        self.mileage = mileage
        self.completedRuns = completedRuns
        return
    
    # when reading the class as a string, returns de data in the model in json format
    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
    
    # adds a new completed run, including it's length in the car mileage
    def completeRun(self, miles=0.0):
        self.mileage+=miles
        self.completedRuns+=1
        return
    
    # allows to modify any of the stored data in the car model. Warning, changing it's id might create some errors
    # like the target car not being found, or modifying the values of another car
    def modifyCar(self, newId=None, newType=None, newSeat=None, newMileage=None, newRuns=None):
        if newId is not None:
            self.id = newId
        if newType is not None:
            self.carType = newType
        if newSeat is not None:
            self.seatCount = newSeat
        if newMileage is not None:
            self.mileage = newMileage
        if newRuns is not None:
            self.completedRuns = newRuns
        return
    
    # method to delete the car model
    def __del__(self):
        return
    
    def to_dict(self):
        return {
            "id": self.id,
            "carType": self.carType,
            "seatCount": self.seatCount,
            "mileage": self.mileage,
            "completedRuns": self.completedRuns
        }
