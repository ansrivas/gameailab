import numpy as np, math

class CReflectCollid():
    def __init__(self):
        pass
    
    def checkCollide(self,ballx,bally,batx,baty,batAngle,batLength):
    
        #Distance between the ball and the bat
        distance = math.hypot( ( ballx - batx ) , ( bally - baty) )
        
        #If distance is atleast l/2
        if( distance <= batLength/2.0):
            angle = math.atan2( ( bally - baty) , ( ballx - batx) ) - batAngle - np.pi/2.0
            
            #If true then collision
            condition = np.abs( (batAngle + np.pi ) - angle ) * (batLength/np.pi)
            if ( distance <= condition ):
                # Collision has occured
                return True
        
        return False
        
    def reflectAngle(self,ballx,bally,batx,baty,batAngle):    
        
        #to find the incidence angle w.r.t to bat
        incidence_angle = batAngle + np.pi - math.atan2( ( bally - baty) , ( ballx - batx) )
        
        #Reflectance angle w.r.t bat
        reflectance_angle = np.pi - incidence_angle
        
        #Change the perspective of the reflectance angle w.r.t to real world.
        new_angle = batAngle + reflectance_angle 
        
        print new_angle
            
        return new_angle