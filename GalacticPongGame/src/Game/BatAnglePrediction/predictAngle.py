from sympy import *
from sympy.geometry import *
from numpy import rad2deg
from math import atan2
from Game.constants import *

debug = False

class Prediction:

    def _lineCircleIntersect(self, (ballx1,bally1,ballx2,bally2)):
        c = Circle(Point(SCREEN_W/2, SCREEN_H/2), RADIUS)
        l = Line(Point(ballx1, bally1), Point(ballx2, bally2))
        
        p, q = intersection(c, l)

#         print (p.x.evalf(), p.y.evalf(), q.x.evalf(), q.y.evalf())
#         return (p.x.evalf(), p.y.evalf(), q.x.evalf(), q.y.evalf())
        
        return p, q
    
    def predictedBatAngle(self, ball):
        p, q = self._lineCircleIntersect(ball)
        
        front = Point(ball[2:])
        back = Point(ball[:2])
        
        if front.distance(p) < back.distance(p):
            target = int(p.x.evalf()), int(p.y.evalf())
        else:
            target = int(q.x.evalf()), int(q.y.evalf())
        
        angle = rad2deg(atan2(target[1]-RING_CENTER[1], target[0]-RING_CENTER[0]))
        
        return int(angle)
        


#     def __init__(self):
#         self.angle1 = 0.0
#         self.angle2 = 0.0
#         
#         # Get the difference of predicted angles from ball angle
#         self.difference1 = 0.0
#         self.difference2 = 0.0
#         
#     def findBestFitAngle(self, ballAngle, (x1,y1,x2,y2)):
#         # Predict Angles using the points on circle
#         ballAngle = np.rad2deg(ballAngle)
#         
#         # To find Angle from points - TECHNIQUE 1
#         '''self.angle1 = -math.atan2(y1 - SCREEN_H/2, x1 - SCREEN_W/2)
#         if(self.angle1 < 0):
#                 self.angle1 += 2*math.pi
#                 
#                 
#         self.angle2 = -math.atan2(y2 - SCREEN_H/2, x2 - SCREEN_W/2)
#         if(self.angle2 < 0):
#                 self.angle2 += 2*math.pi'''
#         
#         
#         # To find Angle from points - TECHNIQUE 2
#         if(ballAngle >= 0 and ballAngle <= 180):        
#             self.angle1 = math.atan2(abs(y1-SCREEN_H/2), x1-SCREEN_W/2)
#         
#             if(self.angle1 < 0):
#                 self.angle1 += 2*math.pi
#                         
#             self.angle2 = math.atan2(abs(y2-SCREEN_H/2), x2-SCREEN_W/2)
#                             
#             if(self.angle2 < 0):
#                 self.angle2 += 2*math.pi
#                 
#                 
#                 
#         if(ballAngle >= 181 and ballAngle <= 360):
#             self.angle1 = math.atan2(-abs(y1-SCREEN_H/2), x1-SCREEN_W/2)
#         
#             if(self.angle1 < 0):
#                 self.angle1 += 2*math.pi
#                         
#             self.angle2 = math.atan2(-abs(y2-SCREEN_H/2), x2-SCREEN_W/2)
#                             
#             if(self.angle2 < 0):
#                 self.angle2 += 2*math.pi
#                 
#         
#         if(debug):    
#             print ballAngle,"   ",np.rad2deg(self.angle1),"   ",np.rad2deg(self.angle2)
#             
#             
#         ballAngle = np.deg2rad(ballAngle)  
#           
#         self.difference1 = abs(ballAngle - self.angle1)
#         self.difference2 = abs(ballAngle - self.angle2)
#         
#         if(self.difference1 > self.difference2):
#             return self.angle2,x2,y2
#         else:
#             return self.angle1,x1,y1
            
        
        