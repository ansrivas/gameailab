import math
import numpy as np
from Game.constants import *

debug = False


class AnglePrediction():
    def __init__(self):
        self.angle1 = 0.0
        self.angle2 = 0.0
        
        # Get the difference of predicted angles from ball angle
        self.difference1 = 0.0
        self.difference2 = 0.0
        
        
    def predictbatangle(self,pointp):
        y = pointp[1]-SCREEN_H/2
        x = pointp[0]-SCREEN_W/2
 
        angle  = -np.rad2deg(np.arctan2(y,x))
        if(angle < 0):
            angle =  360 +angle

        return int(np.round(angle))
           
        
        