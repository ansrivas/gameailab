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
        print "original points are :", pointp
        #if( x > 0 and y > 0):
        angle  = -np.rad2deg(np.arctan2(y,x))
        if(angle < 0):
            angle =  360 +angle
        print "angle from center is", int(np.round(angle))
        return int(np.round(angle))
    
    
        
    def findBestFitAngle(self,ballAngle, (x1,y1,x2,y2)):
        
        # Predict Angles using the points on circle
        ballAngle = np.rad2deg(ballAngle)
        
        # To find Angle from points - TECHNIQUE 1
        '''self.angle1 = -math.atan2(y1 - SCREEN_H/2, x1 - SCREEN_W/2)
        if(self.angle1 < 0):
                self.angle1 += 2*math.pi
                
                
        self.angle2 = -math.atan2(y2 - SCREEN_H/2, x2 - SCREEN_W/2)
        if(self.angle2 < 0):
                self.angle2 += 2*math.pi'''
        
        
        # To find Angle from points - TECHNIQUE 2
        if(ballAngle >= 0 and ballAngle <= 180):        
            self.angle1 = math.atan2(abs(y1-SCREEN_H/2), x1-SCREEN_W/2)
        
            if(self.angle1 < 0):
                self.angle1 += 2*math.pi
                        
            self.angle2 = math.atan2(abs(y2-SCREEN_H/2), x2-SCREEN_W/2)
                            
            if(self.angle2 < 0):
                self.angle2 += 2*math.pi
                
                
                
        if(ballAngle >= 181 and ballAngle <= 360):
            self.angle1 = math.atan2(-abs(y1-SCREEN_H/2), x1-SCREEN_W/2)
        
            if(self.angle1 < 0):
                self.angle1 += 2*math.pi
                        
            self.angle2 = math.atan2(-abs(y2-SCREEN_H/2), x2-SCREEN_W/2)
                            
            if(self.angle2 < 0):
                self.angle2 += 2*math.pi
                
        
        if(debug):    
            print ballAngle,"   ",np.rad2deg(self.angle1),"   ",np.rad2deg(self.angle2)
            
            
        ballAngle = np.deg2rad(ballAngle)  
          
        self.difference1 = abs(ballAngle - self.angle1)
        self.difference2 = abs(ballAngle - self.angle2)
        
        if(self.difference1 > self.difference2):
            return self.angle2,x2,y2
        else:
            return self.angle1,x1,y1
            
        
        