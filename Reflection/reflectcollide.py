import numpy as np, math

class CReflectCollid():
    def __init__(self):
        pass
    
    def checkCollide(self,ballx,bally,batx,baty,batAngle,batLength,ballAngle):
    
        
        batLength = batLength + 28                                          #should also consider balls boundaries to check for collision
        distance = math.hypot( ( ballx - batx ) , ( bally - baty) )         #Distance between the ball and the bat
        
        
        if( distance <= batLength/2.0):                                             #If distance is atleast l/2 w.r.t center of the bat
            
            angle = ballAngle - batAngle + np.pi/2.0
            angle = self.CheckAngle(angle)
            
            condition = np.abs( (batAngle + np.pi ) - angle ) * (batLength/np.pi)   #If true then collision
            
            
            if ( distance <= condition ):

                return True                     # Collision has occured
        
        return False
        
    def reflectAngle(self,ballx,bally,batx,baty,batAngle,ballAngle):    
        
        
        incidence_angle = ballAngle - batAngle + np.pi/2.0                 #to find the incidence angle w.r.t to bat
        #incidence_angle = self.CheckAngle(incidence_angle)
        
        reflectance_angle = np.pi - incidence_angle                         #Reflectance angle w.r.t bat
        #reflectance_angle = self.CheckAngle(reflectance_angle)
        
        new_angle = batAngle + reflectance_angle  + np.pi/2.0               #Change the perspective of the reflectance angle w.r.t to real world.
        new_angle = self.CheckAngle(new_angle)
        
        return new_angle
    
    def CheckAngle(self,angle):
        if not( 0 < angle < (2.0*np.pi) ):
            factor = math.floor(angle / (2.0*np.pi))
            return (angle + (np.pi*(-2.0)*factor))
        return angle