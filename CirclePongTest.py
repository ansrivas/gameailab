import os,sys
from random import randint
import random
import pygame
import math
import numpy as np
from pygame.locals import *
from astropy.coordinates.distances import Distance
from database import db
from Reflection import reflectcollide as refcol
from background import back as bg

# Constants 
N = 1000
SCREEN_W, SCREEN_H = (1280, 720)
debug = True
screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
MULTIPLAYER = True


class Color():
    white=(255,255,255)
    blue = (0,255,255)
    red = (255,0,0)
    snow = (205,201,201)
    palegreen= (152,251,152)

    def __init__(self):
        pass


class Pong(pygame.sprite.Sprite):
    def __init__(self,pongdimension,speed,batimagepath):
        pygame.sprite.Sprite.__init__(self)
      
        self.color = Color.red
        #self.width = width
        self.image = pygame.Surface(pongdimension).convert()
        self.image.fill((255,0,0))
        self.image.set_colorkey((255,0,0))
        
        self.x= 0
        self.y =0
        self.angle = 1
        self.theta =  90 
        self.speed = speed
        self.batdimx, self.batdimy = pongdimension
        
        self.image = pygame.image.load(batimagepath)
        if(debug):
            self.originalrect = pygame.draw.rect(self.image, self.color, (self.x,self.y,self.batdimx, self.batdimy ), 1)
        
        self.rot = pygame.transform.rotate(self.image,self.angle )
        
        self.rect = self.rot.get_rect()
        
        self.rect.center = (266,266)
        
        
        
    def findPointOnCircle(self,deg):
        """
        Give an angle in degrees and we will get a corresponding point on circle w.r.t to this angle in clockwise.
        """
        rad = np.deg2rad(deg)
             
        y = (SCREEN_H/2) - 320 * math.sin(rad)
        x = (SCREEN_W/2) + 320 * math.cos(rad)
            
        return int(x),int(y)
    
    
    def update(self,changeDirection):
        global screen
        
        if(changeDirection ==1):
            self.theta += self.speed
        if(changeDirection ==-1):
            if(self.theta>= 0):
                self.theta -=self.speed
            if(self.theta<0):
                self.theta = 360- self.speed
            
        if(self.theta >= 360):
            self.theta = 00
        
 

        self.angle  = float(self.theta) #- float(self.batdimx/213)

        self.rot = pygame.transform.rotate(self.image,self.angle)
        self.rect = self.rot.get_rect()
        self.rect.center = self.findPointOnCircle(self.theta)
        screen.blit(self.rot,self.rect)
        #print "self.rect =",self.rect
        #print "self.rect.center",self.rect.center


        
class FireBall(pygame.sprite.Sprite):
    def __init__(self,ballDimension,imageName):
        # Call the parent class (Sprite) constructor
        super(FireBall,self).__init__()
         
        # Create the image of the ball
        self.image = pygame.image.load(imageName)
         
        
         
        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()
        
        self.rect.centerx,self.rect.centery = (100,100)
         
        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
         
        # Speed in pixels per cycle
        self.speedx = 7
        
        self.speedy = 7
        # Floating point representation of where the ball is
        self.x = SCREEN_W/2
        self.y = SCREEN_H/2
         
        # Direction of ball in degrees
        self.angle = np.pi/4.0
        self.angle = random.uniform(0,2*math.pi)
        
         
        
        
        
        
    
    
    def reset(self):
        self.x = SCREEN_W/2
        self.y = SCREEN_H/2
        self.speedx=7
        self.speedy=7
        self.angle = random.uniform(0,2*math.pi)
        #self.angle = 0
 
        '''# Direction of ball (in degrees)
        self.direction = random.randrange(-45,45)
         
        # Flip a 'coin'
        if random.randrange(2) == 0 :
            # Reverse ball direction, let the other guy get it first
            self.direction += 180
            #self.y = 50'''
            
    # This function will bounce the ball off a horizontal surface (not a vertical one)
    '''def bounce(self,PaddleAngle):
        
        
        if(PaddleAngle > 120 and PaddleAngle < 240):            
            self.angle = -self.angle
            
        if(PaddleAngle >0 and PaddleAngle < 60):            
            self.angle = -self.angle
            
        if(PaddleAngle >300 and PaddleAngle < 360):            
            self.angle = -self.angle
            
        if(PaddleAngle > 90 and PaddleAngle <119):
            self.angle = math.pi - self.angle  
            
        if(PaddleAngle > 241 and PaddleAngle < 299):
             self.angle = math.pi - self.angle
            
            
            
        #self.speedx *= -1
        #self.speedy *= -1 '''
    
    def update(self):
        
        # Sine and Cosine work in degrees, so we have to convert them
        #direction_radians = math.radians(self.direction)
        
         
        # Change the position (x and y) according to the speed and direction
        self.x += math.cos(self.angle) * self.speedx
        self.y -= math.sin(self.angle) * self.speedy
        
        
        
        
        
        if self.y <= 0 or self.x <= 0:
            self.reset()
             
        if self.y >= SCREEN_H or self.x >= SCREEN_W:
            self.reset()
        
        
        
        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y
        
        screen.blit(self.image,self.rect)
        
        
 
def main():
    # basic start
    global SCREEN_H,SCREEN_W
    ignoreCollide = 0
    pygame.init()
    
    pygame.display.set_caption('Galactic Pong')
    running = True
    
    back = pygame.Surface((SCREEN_W,SCREEN_H))
    background = back.convert()
    color = Color()
    
    #class which calculates the collision and reflection
    calculate = refcol.CReflectCollid()
    
    #TODO: need to fix this function here
    backg = bg.CBackground((SCREEN_W/2, SCREEN_H/2),320,5,color.palegreen)
    
    # WolverPONG Call Function
    wolverpongimage = "./data/rWolverGamePONG.png"
    wolverPong = Pong((50,120),2,wolverpongimage) 
    WolverchangeDirection = 0
    
    if(MULTIPLAYER):
        # RayPONG Call Function
        rayPongimage = "./data/RayGamePONG.png"
        rayPong = Pong((50,120),2,rayPongimage) 
        RaychangeDirection = 0
        
    # FireBall Call Function
    ballimage = "./data/pongball.png"
    fireBall = FireBall((28,29), ballimage)
    balls = pygame.sprite.Group()
    balls.add(fireBall)
    
    movingsprites = pygame.sprite.Group()
    movingsprites.add(wolverPong)
    if(MULTIPLAYER):
        movingsprites.add(rayPong)
    movingsprites.add(fireBall)

    Collide = False
    clock = pygame.time.Clock()
    while running:
        
        # movement of ball (circle)
        time_passed = clock.tick(300)
        time_sec = time_passed / 1000.0
    
    
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                ''' WolverPONG MOVEMENTS - A,D'''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        WolverchangeDirection = 1
                        
                    elif event.key == pygame.K_d:
                        WolverchangeDirection = -1
                        
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        WolverchangeDirection = 0
                        
                    elif event.key == pygame.K_d:
                        WolverchangeDirection = 0
                        
                ''' RayPONG MOVEMENTS - LEFT,RIGHT'''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        RaychangeDirection = 1
                        
                    elif event.key == pygame.K_RIGHT:
                        RaychangeDirection = -1
                        
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        RaychangeDirection = 0
                        
                    elif event.key == pygame.K_RIGHT:
                        RaychangeDirection = 0
                        
        
        screen.blit(background,(0,0))
        screen.fill(Color.white)  
        backg.update(screen)  
        wolverPong.update(WolverchangeDirection)
        if(MULTIPLAYER):
            rayPong.update(RaychangeDirection)
        fireBall.update() 
        
        #TODO: update this background implementation
        
        
        #If collided, dont check for collision for next few iterations
        if (ignoreCollide==0):
            
            # See if the ball hits the player paddle
            
            #Collide = calculate.checkCollide(fireBall.rect.centerx,fireBall.rect.centery,wolverPong.rect.centerx,wolverPong.rect.centery,np.deg2rad(wolverPong.angle),wolverPong.rect[3])                 
            Collide = calculate.checkCollide(fireBall.rect.centerx,fireBall.rect.centery,wolverPong.rect.centerx,wolverPong.rect.centery,np.deg2rad(wolverPong.angle),120,fireBall.angle)
            if Collide:             
                     
                fireBall.angle = calculate.reflectAngle(fireBall.rect.centerx,fireBall.rect.centery,wolverPong.rect.centerx,wolverPong.rect.centery,np.deg2rad(wolverPong.angle),fireBall.angle)              
                ignoreCollide = 20    
                Collide = False
                        
            if(MULTIPLAYER):
                Collide = calculate.checkCollide(fireBall.rect.centerx,fireBall.rect.centery,rayPong.rect.centerx,rayPong.rect.centery,np.deg2rad(rayPong.angle),120,fireBall.angle)  
                
                   
                if Collide:
                   
                    fireBall.angle = calculate.reflectAngle(fireBall.rect.centerx,fireBall.rect.centery,rayPong.rect.centerx,rayPong.rect.centery,np.deg2rad(rayPong.angle),fireBall.angle)
                    ignoreCollide = 20 
                    Collide = False
                
                    
                    
            
           
            
            
            
        
        pygame.display.flip()
        clock.tick(100)
        if (ignoreCollide > 0):
            ignoreCollide -= 1
                
                    
        
        
        
        
 
if __name__ == '__main__': 
    
    
    
    main()
#    data = db.Data()