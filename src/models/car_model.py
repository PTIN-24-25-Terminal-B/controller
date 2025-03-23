import json

class carModel:
    #variable types: carModel(integer, string, string, float, integer)
    def __init__(self, carType, seatCount, id=None, mileage=0.0, completedRuns=0):
        self.id = id
        self.seatCount = seatCount
        self.carType = carType
        self.mileage = mileage
        self.completedRuns = completedRuns
        return
    
    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
    
    def completeRun(self, miles=0.0):
        self.mileage+=miles
        self.completedRuns+=1
        return
    
    def modifyCar(self, newType=None, newSeat=None, newId=None, newMileage=None, newRuns=None):
        if newType is not None:
            self.carType = newType
        if newSeat is not None:
            self.seatCount = newSeat
        if newId is not None:
            self.id = newId
        if newMileage is not None:
            self.mileage = newMileage
        if newRuns is not None:
            self.completedRuns = newRuns
        return
    
    def __del__(self):
        return