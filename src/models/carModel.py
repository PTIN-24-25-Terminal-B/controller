import json

class carModel:
    def __init__(self, seatCount, carType, id=None, mileage=0, totalRuns=0):
        self.id = id
        self.seatCount = seatCount
        self.carType = carType
        self.mileage = mileage
        self.totalRuns = totalRuns
        return
    
    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
    
    def completeRun(self, miles=0):
        self.mileage+=miles
        self.totalRuns+=1
        return
    
    def modifyCar(self, newSeat=None, newType=None, newId=None, newMileage=None, newRuns=None):
        if newSeat is not None:
            self.seatCount = newSeat
        if newType is not None:
            self.carType = newType
        if newId is not None:
            self.id = newId
        if newMileage is not None:
            self.mileage = newMileage
        if newRuns is not None:
            self.totalRuns = newRuns
        return
    
    def __del__(self):
        return