import math

debug = False

class FindIntersection():
    def __init__(self):
        
        self.slope = 0.0
        self.intermediateValue = 0.0
        
        # Quadratic Equation parameters
        self.a = 0.0
        self.b = 0.0
        self.c = 0.0 
        
        # Quadratic Formula second part (b^2 - 4ac)
        self.squareRootPart = 0.0
        
        # Points of Intersection
        self.x1,self.y1 = 0.0,0.0
        self.x2,self.y2 = 0.0,0.0
        
        # Bat Angles
        self.angle1 = 0.0
        self.angle2 = 0.0
    
    
    def findQuadraticParameters(self,slope,xcenter,intermediateValue,radius):        
        # find "a" 
        self.a = 1 + (slope**2)
        
        # find "b"
        self.b = (-2*xcenter) + (2*slope*intermediateValue)
        
        #find "c"
        self.c = (xcenter**2) + (intermediateValue**2) - (radius**2)
        
        if(debug):
            print "a : ",self.a
            print "b : ",self.b
            print "c : ",self.c
            
        return self.a,self.b,self.c
    
    def solveSquareRootPart(self,a,b,c):
       
        if(debug):
            print "b`2 : ",b**2
            print "4ac : ",4*a*c 
            print "b`2 - 4ac : ",b**2 - 4*a*c
        return math.sqrt(b**2 - 4*a*c)
        
    
    def lineCircleIntersect(self,ballx1,bally1,ballx2,bally2,ballAngle,radius,xcenter,ycenter):
        
        
        # Find slope of ball angle 
        if not (ballx2 - ballx1) == 0: 
            self.slope = (bally2 - bally1) / (ballx2 - ballx1)
        else:
            self.slope = 0
            
            
        if(debug):
            print "Slope :",self.slope
            print "Ballx1,y1 :", ballx1,bally1
            print "Ballx2,y2", ballx2,bally2
            print "BallAngle :",ballAngle
            
            
        # Find intermediate value (Like a mid value from a derivation)
        self.intermediateValue = -(self.slope*ballx1) + bally1 - ycenter
        
        
        # Find a,b,c
        self.a,self.b,self.c = self.findQuadraticParameters(self.slope,xcenter,self.intermediateValue,radius)
        
        # Find Square root part in quadratic Formula
        self.squareRootPart = self.solveSquareRootPart(self.a,self.b,self.c)
        
        
        # Use quadratic formula to find x 
        self.x1 = (-self.b + self.squareRootPart) / (2 * self.a)
        self.x2 = (-self.b - self.squareRootPart) / (2 * self.a)
        
               
        # Find y
        self.y1 = self.slope* (self.x1 - ballx1) + bally1
        self.y2 = self.slope* (self.x2 - ballx1) + bally1
        
        if(debug):
            print "x1 y1 :",self.x1,self.y1
            print "x2 y2 :",self.x2,self.y2
        
        
        return self.x1,self.y1,self.x2,self.y2
        