import numpy as np
import math
from sympy import *
from sympy.geometry import *
from Game.constants import *
from sympy.polys.tests.test_injections import __make_f2

class CReflectCollide:
    
#     def __init__(self):
#         pass
#     
#     def checkCollide(self, (ballx, bally), (batx, baty), batAngle, batLength, ballAngle):
#     
# #         ballx, bally = ball
# #         batx, baty = bat
#         batLength = batLength #+ 28                                          #should also consider balls boundaries to check for collision
#         distance = math.hypot( ( ballx - batx ) , ( bally - baty) )         #Distance between the ball and the bat
#         
#         
#         if( distance <= batLength/2.0):                                             #If distance is atleast l/2 w.r.t center of the bat
#             
#             angle = ballAngle - batAngle + np.pi/2.0
#             angle = self.CheckAngle(angle)
#             
#             condition = np.abs( (batAngle + np.pi ) - angle ) * (batLength/np.pi)   #If true then collision
#             
#             
#             if ( distance <= condition ):
# 
#                 return True                     # Collision has occured
#         
#         return False
        
    def reflectAngle(self, (batx, baty), lastCollisonPoint):
#        print "Line : {} to {}".format(lastCollisonPoint, (batx, baty))
        ballLine = Line(Point(lastCollisonPoint), Point(batx, baty))
        radialLine = Line(RING_CENTER, Point(batx, baty))
        normal = radialLine.perpendicular_line(Point(batx, baty))
        refLine = ballLine.reflect(normal)
        c = Circle(RING_CENTER, RADIUS)
        p1, p2 = intersection(c, refLine)

        if p1.distance(Point(batx, baty)) > p2.distance(Point(batx, baty)):
            target = p1
        else:
            target = p2

        target = [int(round(target.x.evalf())), int(round(target.y.evalf()))]
        angle = np.rad2deg(-math.atan2(target[1]-baty, target[0]-batx))
        if angle < 0:
            angle += 360
        
        return int(angle), target
        
#         incidence_angle = ballAngle - batAngle + np.pi/2.0                 #to find the incidence angle w.r.t to bat
#         
#         reflectance_angle = np.pi - incidence_angle                         #Reflectance angle w.r.t bat
#         
#         new_angle = batAngle + reflectance_angle  + np.pi/2.0               #Change the perspective of the reflectance angle w.r.t to real world.
#         new_angle = self.CheckAngle(new_angle)
#         
#         return new_angle
    
#     def CheckAngle(self,angle):
#         if not( 0 < angle < (2.0*np.pi) ):
#             factor = math.floor(angle / (2.0*np.pi))
#             return (angle + (np.pi*(-2.0)*factor))
#         return angle

if __name__ == "__main__":
    cl = CReflectCollide()
    print cl.reflectAngle((610, 400), RING_CENTER)