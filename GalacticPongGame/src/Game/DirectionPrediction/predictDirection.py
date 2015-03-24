class Direction():
    
    def __init__(self):
        self.clockwiseDirection = 0
        self.antiClockwiseDirection = 0
        self.clockwiseAngle = 0.0
        self.antiClockwiseAngle = 0.0
        self.direction = 0.0
        
        
        
    def directionToPredict(self,batAngle,predictedBatAngle):
   
        way1 = abs(batAngle - predictedBatAngle)
        way2 = 360 - way1
                                    
        if min(way1, way2) == way1:
            if predictedBatAngle < batAngle:
                self.direction = -1
            else:
                self.direction = 1
        else:
            if predictedBatAngle > batAngle:
                self.direction = -1
            else:
                self.direction = 1                   
            
        #the angle between batangle and predicted batangle became too small, so dont change the directions now
        if (way1 < 1.2):
            self.direction = 0
        return self.direction
            
        