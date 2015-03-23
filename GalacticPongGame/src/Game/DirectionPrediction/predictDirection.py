class Direction():
    
    def __init__(self):
        self.clockwiseDirection = 0
        self.antiClockwiseDirection = 0
        self.clockwiseAngle = 0.0
        self.antiClockwiseAngle = 0.0
        self.direction = 0.0
        
        
        
    def directionToPredict(self,currentBatAngle,predictedBatAngle):
        
        # Current Bat in 1st Quadrant
        if(predictedBatAngle >=0 and predictedBatAngle < 90):
            # Predicted Bat Angle in 1st Quadrant
            if(currentBatAngle >= 0 and currentBatAngle < 90):
                if(currentBatAngle > predictedBatAngle):
                    if(currentBatAngle+1 == predictedBatAngle or currentBatAngle-1 == predictedBatAngle):
                        self.direction = 0
                    else:
                        self.direction = -1
                else:
                    self.direction = 1
            # Predicted Bat Angle in 2nd Quadrant
            elif(currentBatAngle >=90 and currentBatAngle < 180):
                self.direction = -1
            # Predicted Bat Angle in 3rd Quadrant
            elif(currentBatAngle >= 180 and currentBatAngle < 270):
                if(currentBatAngle >= 180 and currentBatAngle < 225):
                    if(predictedBatAngle >=45 and predictedBatAngle < 90):
                        self.direction = -1
                    else:
                        self.direction = 1
                elif(currentBatAngle >= 225 and currentBatAngle < 270):
                    if(predictedBatAngle >= 0 and predictedBatAngle > 45):
                        self.direction = 1
                    else:
                        self.direction = -1
            # Predicted Bat Angle in 4th Quadrant
            elif(currentBatAngle >= 270 and currentBatAngle < 360):
                self.direction = 1
                
                
        
        # Current Bat in 2nd Quadrant
        if(predictedBatAngle >=90 and predictedBatAngle < 180):
            # Predicted Bat Angle in 1st Quadrant
            if(currentBatAngle >= 0 and currentBatAngle < 90):
                self.direction = 1
            # Predicted Bat Angle in 2nd Quadrant
            elif(currentBatAngle >=90 and currentBatAngle < 180):
                if(currentBatAngle > predictedBatAngle):
                    if(currentBatAngle+1 == predictedBatAngle or currentBatAngle-1 == predictedBatAngle):
                        self.direction = 0
                    else:
                        self.direction = -1
                else:
                    self.direction = 1
            # Predicted Bat Angle in 3rd Quadrant
            elif(currentBatAngle >= 180 and currentBatAngle < 270):
                self.direction = -1
            # Predicted Bat Angle in 4th Quadrant
            elif(currentBatAngle >= 270 and currentBatAngle < 360):
                if(currentBatAngle >= 270 and currentBatAngle < 315):
                    if(predictedBatAngle >= 135 and predictedBatAngle < 180):
                        self.direction = -1
                    else:
                        self.direction = 1
                elif(currentBatAngle >= 315 and currentBatAngle < 360):
                    if(predictedBatAngle >= 90 and predictedBatAngle < 135):
                        self.direction = 1
                    else:
                        self.direction = -1
                        
                        
        
                
        
        # Current Bat in 3rd Quadrant
        if(predictedBatAngle >=180 and predictedBatAngle < 270):
            # Predicted Bat Angle in 1st Quadrant
            if(currentBatAngle >= 0 and currentBatAngle < 90):
                if(currentBatAngle >= 0 and currentBatAngle < 45):
                    if(predictedBatAngle >= 225 and predictedBatAngle < 270):
                        self.direction = -1
                    else:
                        self.direction = 1
                elif(currentBatAngle >=45 and currentBatAngle < 90):
                    if(predictedBatAngle >=180 and predictedBatAngle < 225):
                        self.direction = 1
                    else:
                        self.direction = -1
            # Predicted Bat Angle in 2nd Quadrant
            elif(currentBatAngle >=90 and currentBatAngle < 180):
                self.direction = 1
            # Predicted Bat Angle in 3rd Quadrant
            elif(currentBatAngle >= 180 and currentBatAngle < 270):
                if(currentBatAngle > predictedBatAngle):
                    if(currentBatAngle+1 == predictedBatAngle or currentBatAngle-1 == predictedBatAngle):
                        self.direction = 0
                    else:
                        self.direction = -1
                else:
                    self.direction = 1
            # Predicted Bat Angle in 4th Quadrant
            elif(currentBatAngle >= 270 and currentBatAngle < 360):
                self.direction = -1
                
                
        
        
        # Current Bat in 4th Quadrant
        if(predictedBatAngle >=270 and predictedBatAngle < 360):
            # Predicted Bat Angle in 1st Quadrant
            if(currentBatAngle >= 0 and currentBatAngle < 90):
                self.direction = -1
                
            # Predicted Bat Angle in 2nd Quadrant
            elif(currentBatAngle >=90 and currentBatAngle < 180):
                if(currentBatAngle >= 90 and currentBatAngle < 135):
                    if(predictedBatAngle >= 315 and predictedBatAngle < 360):
                        self.direction = -1
                    else:
                        self.direction = 1
                elif(currentBatAngle >=135 and currentBatAngle < 180):
                    if(predictedBatAngle >=270 and predictedBatAngle < 315):
                        self.direction = 1
                    else:
                        self.direction = -1
            # Predicted Bat Angle in 3rd Quadrant
            elif(currentBatAngle >= 180 and currentBatAngle < 270):
                self.direction = 1
            # Predicted Bat Angle in 4th Quadrant
            elif(currentBatAngle >= 270 and currentBatAngle < 360):
                if(currentBatAngle > predictedBatAngle):
                    if(currentBatAngle+1 == predictedBatAngle or currentBatAngle-1 == predictedBatAngle):
                        self.direction = 0
                    else:
                        self.direction = -1
                else:
                    self.direction = 1
                    
            
        return self.direction
            
        