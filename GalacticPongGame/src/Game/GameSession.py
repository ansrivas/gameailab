import pygame
import time
import math, random
import numpy as np
from constants import *
from Reflection import reflectcollide as refcol
from Game import GameOver
from sympy.mpmath import ci

# Sound Initialization
pygame.mixer.pre_init(44100, -16, 2, 4096)

#  Playback song
sounds = []
sounds.append(pygame.mixer.Sound('./data/GameBackground.wav'))
sounds.append(pygame.mixer.Sound('./data/BallHit1.wav'))
sounds.append(pygame.mixer.Sound('./data/BallHit2.wav'))
sounds.append(pygame.mixer.Sound('./data/BallOut1.wav'))
sounds.append(pygame.mixer.Sound('./data/hitball.wav'))

# Set Screen Width and Screen Height 
screen = pygame.display.set_mode(RESOLUTION, 0, 32)

debug = False

radius = 320

class Pong(pygame.sprite.Sprite):
    """ Sprite Class for Pong bats - WolverPong, RayPong """

    def __init__(self, batImagePath, initialPlace, pongDimension=(50, 120), speed=2):
        super(Pong, self).__init__()
      
        self.color = RED
        #self.width = width
        self.x = self.y = 0
        self.angle = 1
        self.theta =  initialPlace 
        self.speed = speed
        self.batdimx, self.batdimy = pongDimension
        self.image = pygame.image.load(batImagePath)

        if(debug):
            self.originalrect = pygame.draw.rect(self.image, self.color, (self.x, self.y, self.batdimx, \
                                                                          self.batdimy), 1)
        
        self.rot = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rot.get_rect()
        self.rect.center = (266, 266)

        
    def findPointOnCircle(self, deg):
        """ Returns the x,y coordinates of the corresponding angle (in degrees) """

        rad = np.deg2rad(deg)
        x = (SCREEN_W/2) + 320 * math.cos(rad)
        y = (SCREEN_H/2) - 320 * math.sin(rad)

        return int(x),int(y)
    
    
    def update(self, changeDirection, screen):
        if(changeDirection == 1):
            self.theta += self.speed
        elif(changeDirection == -1):
            if(self.theta >= 0):
                self.theta -= self.speed
            else:
                self.theta = 360- self.speed
            
        if(self.theta >= 360):
            self.theta = 0
        
        self.angle  = float(self.theta) #- float(self.batdimx/213)
        self.rot = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rot.get_rect()
        self.rect.center = self.findPointOnCircle(self.theta)
        screen.blit(self.rot, self.rect)
 
    def resetbat(self, initialloc):
        self.x = self.y = 0
        self.angle = 1
        self.theta =  initialloc 
        self.speed = 2
        self.rect.center = (266,266)


class FireBall(pygame.sprite.Sprite):
    """ Sprite Class for pong ball - FireBall"""
    
    def __init__(self, ballDimension=(28,29), ballImage="./data/ball.png"):
        # Call the parent class (Sprite) constructor
        super(FireBall, self).__init__()
         
        self.image = pygame.image.load(ballImage)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = (100,100)

        # Speed in pixels per cycle
        self.speedx = self.speedy = 3.0

        # Floating point representation of where the ball is
        self.x, self.y = SCREEN_W/2, SCREEN_H/2
         
        # Direction of ball in degrees
        self.angle = random.uniform(0, 2*math.pi)
        
        self.offset = 70
        
        '''
        This is the case where rally has been increased to a 20, start increasing the speed 
        after this to make it harder
        '''
        self.rally = 0

        
    def resetBall(self, player, BallsLeft):
        self.x = SCREEN_W/2
        self.y = SCREEN_H/2
        self.speedx = self.speedy = 3.0
        self.angle = random.uniform(0, 2*math.pi)

        player *= -1 
        BallsLeft -= 1
        self.rally = 0
        
        return player, BallsLeft

    
    def update(self, screen, player, BallsLeft):
         
        # Change the position (x and y) according to the speed and direction
        self.x += math.cos(self.angle) * self.speedx
        self.y -= math.sin(self.angle) * self.speedy
  
        # Reset the ball position if it goes out of the circle (+ offset value)
        if math.sqrt((self.x - SCREEN_W/2)**2 + (self.y - SCREEN_H/2)**2) >= (radius + self.offset):
            player, BallsLeft = self.resetBall(player, BallsLeft)
             
        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y
        
        '''If the rally continued for more than 5 times, 
            start increasing the speed of the ball to make it harder
        '''
        if(self.rally > 0):
            if(self.rally%3 == 0):
                self.increasespeed()
            
        screen.blit(self.image, self.rect)

        return player, BallsLeft


    def increasespeed(self):
        '''just increase the speed a bit after a 
        successful rally, so as to increase hardness
        '''
        self.speedx += 0.005
        self.speedy += 0.005
        

class CMain():

    def __init__(self, screen):
        pygame.init()
        pygame.display.set_caption('Galactic Pong') 

        self.gamestate = RUNNING
        self.MULTIPLAYER = True
        self.stars = [
            [random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)]
            for _ in range(numStars)
        ]
        self.screen = screen
        self.background = pygame.Surface(screen.get_size()).convert()

        self.scoreFont = pygame.font.SysFont("calibri",40)
        self.headingFont = pygame.font.SysFont("Papyrus",30)

        wolverpongimage = "./data/rWolverGamePONG.png"
        self.wolverPong = Pong(wolverpongimage, 180)  
         
        if self.MULTIPLAYER:
            rayPongimage = "./data/RayGamePONG.png"
            self.rayPong = Pong(rayPongimage, 0) 

        self.fireBall = FireBall()

        # set transparency for the circles
        self.InnerColorTone = self.InnerBigColorTone = 20
        self.OuterColorTone = self.OuterBigColorTone = 40
        
        self.InnerOrange = self.setCircles(self.InnerColorTone)
        self.OuterOrange = self.setCircles(self.OuterColorTone, (255,165,0,100), 3)
        self.InnerWhite = self.setCircles(self.InnerColorTone, (200,200,200,100))
        self.OuterWhite = self.setCircles(self.OuterColorTone,(200,200,200,100), 3)
        
        self.InnerBigOrange = self.setCircles(self.InnerBigColorTone, \
                                                   radius=300, pos=(SCREEN_W/2,SCREEN_H/2), surfacePos=RESOLUTION)
        self.OuterBigOrange = self.setCircles(self.OuterBigColorTone, width=4, \
                                                   radius=300, pos=(SCREEN_W/2,SCREEN_H/2), surfacePos=RESOLUTION)
        self.InnerBigWhite = self.setCircles(self.InnerBigColorTone, (200,200,200,255), \
                                                   radius=300, pos=(SCREEN_W/2,SCREEN_H/2), surfacePos=RESOLUTION)
        self.OuterBigWhite = self.setCircles(self.OuterBigColorTone, (200,200,200,255), 4, \
                                                   radius=300, pos=(SCREEN_W/2,SCREEN_H/2), surfacePos=RESOLUTION)

    
    def setCircles(self, alpha, color=(255,165,0,255), width=0, radius=50, pos=(100, 100), \
                        surfacePos=(200, 200), fill=BLACK, colorkey=BLACK):
        obj = pygame.Surface(surfacePos)
        obj.fill(fill)
        obj.set_colorkey(colorkey)
        obj.set_alpha(alpha)
        pygame.draw.circle(obj, color, pos, radius, width)
        
        return obj

    
    def blitstars(self): 
        # Generate N Star Positions
            
        self.background.fill(BLACK)     
        # Draw Stars (stars moving effect) 
        for star in self.stars:
            pygame.draw.line(self.background,(255, 255, 255), (star[0], star[1]), (star[0], star[1]))
            star[0] -= 1
            if star[0] < 0:
                star[0] = SCREEN_W
                star[1] = random.randint(0, SCREEN_H)
        
        self.screen.blit(self.background,(0,0)) 
     
    def renderfonts(self,wolverScore,rayScore,ballsleft):
                # Render Scores        
        wolverScoreRender = self.scoreFont.render(str(wolverScore), True,(205,205,205))
        rayScoreRender = self.scoreFont.render(str(rayScore), True,(205,205,205)) 
        # Render Balls Left
        BallsLeftRender = self.headingFont.render("BALLS LEFT : "+str(ballsleft), True,(205,205,205))
        # Render HighScore
        HighScoreRender = self.headingFont.render("HIGHSCORE : ", True,(205,205,205))
        self.screen.blit(wolverScoreRender,(188.,185.))
        self.screen.blit(rayScoreRender,(1068.,185.)) 
        
        self.screen.blit(BallsLeftRender,(10.,10.)) 
        self.screen.blit(HighScoreRender,(1000.,10.)) 
          
       
    def render_score_circles(self):
                # Display Score Circles
        self.screen.blit(self.OuterOrange, (100,100,100,100))
        self.screen.blit(self.InnerOrange, (100,100,100,100))
        self.screen.blit(self.OuterWhite, (980,100,100,100))
        self.screen.blit(self.InnerWhite, (980,100,100,100))
        
 
    def delay3seconds(self,wolverScore,rayScore,ballsleft,st):
        i = 3
        while(i > 0):
            self.blitstars()
            self.render_score_circles()
            self.renderfonts(wolverScore, rayScore, ballsleft)
            secondsRender = self.headingFont.render(st+str(i), True,(205,205,205))
            self.screen.blit(secondsRender,(525.,10.)) 
            
            pygame.display.flip()
            time.sleep(1.)
            i -=1
    
    def reset_entire_gamestate(self):
        pass
            
    def render_pause_screen(self):
        pauseRender = self.headingFont.render("Game Paused: press Space Bar to resume", True,(205,205,205))
        self.screen.blit(pauseRender,(380.,100.)) 

    def render_stop_screen(self):
        stopRender = self.headingFont.render("Game Stopped: press Space Bar to restart", True,(205,205,205))
        self.screen.blit(stopRender,(380.,100.)) 
 
 
 
BallsLeft = 10
ignoreCollide = 0
wolverScore = 0
rayScore = 0
WolverchangeDirection = 0
RaychangeDirection = 0
Collide = False  

def global_param_reset(): 
    '''
    this function will reset all the parameters which are being used in main game loop
    '''
    global BallsLeft,ignoreCollide,wolverScore,rayScore,WolverchangeDirection ,RaychangeDirection,Collide
    BallsLeft = 10
    ignoreCollide = 0
    wolverScore = 0
    rayScore = 0
    WolverchangeDirection = 0
    RaychangeDirection = 0
    Collide = False  
        
def game(screen):
 
    global BallsLeft,ignoreCollide,wolverScore,rayScore,WolverchangeDirection ,RaychangeDirection,Collide
     
    main = CMain(screen)
    #class which calculates the collision and reflection
    calculate = refcol.CReflectCollid()

    # Play Background Music
    sounds[0].set_volume(0.3)
    sounds[0].play()
    
    # Number of Balls Left
    BallsLeft = 10
        
    # If collided once, dont check for the next n iterations
    ignoreCollide = 0
        
    wolverScore = rayScore = 0
    WolverchangeDirection = RaychangeDirection = 0

    Collide = False
 
    #Player turns
    player = 1      
    running = True
    clock = pygame.time.Clock()
    screen.blit(main.background,(0,0))
    st = "Game starts in : "
    main.delay3seconds( wolverScore=0, rayScore=0, ballsleft=0,st=st)

    while running:
        #clock.tick(100)
        time_passed = clock.tick(300)
        time_sec = time_passed / 1000.0
     
        # Change value if single player
        if not main.MULTIPLAYER:
            player = 1    
                               
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                ''' WolverPONG MOVEMENTS - A,D'''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        WolverchangeDirection = 1
                        
                    elif event.key == pygame.K_d:
                        WolverchangeDirection = -1
                    
                    if event.key == pygame.K_LEFT:
                        RaychangeDirection = 1
                    
                    elif event.key == pygame.K_RIGHT:
                        RaychangeDirection = -1
                    
                    if event.key == pygame.K_SPACE: 
                        if(main.gamestate == RUNNING):
                            main.gamestate = PAUSED  
                        elif(main.gamestate == PAUSED):
                            main.gamestate = RUNNING 
                            st = "Resuming in: "
                            #just passed the current wolverscore, etc to resume from current state
                            main.delay3seconds(wolverScore,rayScore,BallsLeft,st)
                        elif(main.gamestate == STOPPED):
                            st = "Game starts in: "
                            main.delay3seconds(wolverScore,rayScore,BallsLeft,st)
                            main.gamestate = RUNNING
                     
                    if event.key == pygame.K_r:
                        if(main.gamestate == RUNNING or main.gamestate == PAUSED):   
                            main.gamestate = RESET 

                            global_param_reset()
                            main.wolverPong.resetbat(180)
                            main.wolverPong.update(WolverchangeDirection,screen)
                            if(main.MULTIPLAYER):
                                main.rayPong.resetbat(0)
                                main.rayPong.update(RaychangeDirection,screen)
                
                            # Change turn if player loses the ball
                            player,BallsLeft = main.fireBall.update(screen, player, BallsLeft) 
              
                            st = "Resetting in: "
                            main.delay3seconds(wolverScore,rayScore,BallsLeft,st)
                            main.gamestate = RUNNING
 
                    if event.key == pygame.K_s:
                        if(main.gamestate == RUNNING or main.gamestate == PAUSED ):
                            main.gamestate = STOPPED

                            global_param_reset()
                            main.wolverPong.resetbat(180)
                            main.wolverPong.update(WolverchangeDirection, screen)
                            if(main.MULTIPLAYER):
                                main.rayPong.resetbat(0)
                                main.rayPong.update(RaychangeDirection, screen)
                
                            # Change turn if player loses the ball
                            player,BallsLeft = main.fireBall.update(screen, player, BallsLeft) 
              
                              
                              
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        WolverchangeDirection = 0
                        
                    elif event.key == pygame.K_d:
                        WolverchangeDirection = 0

                    if event.key == pygame.K_LEFT:
                        RaychangeDirection = 0
                        
                    elif event.key == pygame.K_RIGHT:
                        RaychangeDirection = 0
        
        

        main.blitstars()
        if(main.gamestate == STOPPED):
            main.render_stop_screen()
            
        if(main.gamestate == PAUSED):
            main.render_pause_screen()
            
        if(main.gamestate == RUNNING): 
            main.wolverPong.update(WolverchangeDirection,screen)
            if(main.MULTIPLAYER):
                main.rayPong.update(RaychangeDirection,screen)
                
            # Change turn if player loses the ball
            player,BallsLeft = main.fireBall.update(screen, player, BallsLeft) 

            if(BallsLeft > 0):
                
                #If collided, dont check for collision for next few iterations
                if (ignoreCollide==0):
                    
                    # WolverPong's Turn               
                    if(player == 1):
                        # Draw Background Circle
                        screen.blit(main.OuterBigOrange,(0,0))
                        screen.blit(main.InnerBigOrange,(0,0))
                        
                        # Check Collision
                        Collide = calculate.checkCollide(main.fireBall.rect.centerx,main.fireBall.rect.centery, \
                                                         main.wolverPong.rect.centerx,main.wolverPong.rect.centery, \
                                                         np.deg2rad(main.wolverPong.angle),120,main.fireBall.angle)
                        
                        if Collide: 
                            # Increase Score by 1            
                            wolverScore += 1
                            #sounds[1].play()  
                            sounds[4].play()   
                            main.fireBall.angle = calculate.reflectAngle(main.fireBall.rect.centerx, \
                                                                         main.fireBall.rect.centery, \
                                                                         main.wolverPong.rect.centerx, \
                                                                         main.wolverPong.rect.centery, \
                                                                         np.deg2rad(main.wolverPong.angle), \
                                                                         main.fireBall.angle)              
                            ignoreCollide = 20    
                            Collide = False
                            player = -1
                            main.fireBall.rally +=1
                            
                    # RayPong's Turn            
                    if(main.MULTIPLAYER):
                        if(player == -1):
                            # Draw Background Circle
                            screen.blit(main.OuterBigWhite,(0,0))
                            screen.blit(main.InnerBigWhite,(0,0))
                            
                            # Check Collision
                            Collide = calculate.checkCollide(main.fireBall.rect.centerx,main.fireBall.rect.centery, \
                                                             main.rayPong.rect.centerx,main.rayPong.rect.centery, \
                                                             np.deg2rad(main.rayPong.angle),120,main.fireBall.angle)  
                            
                               
                            if Collide:
                                # Increase Score by 1
                                rayScore += 1  
                                #sounds[2].play()
                                sounds[4].play()
                                main.fireBall.angle = calculate.reflectAngle(main.fireBall.rect.centerx, \
                                                                             main.fireBall.rect.centery, \
                                                                             main.rayPong.rect.centerx, \
                                                                             main.rayPong.rect.centery, \
                                                                             np.deg2rad(main.rayPong.angle), \
                                                                             main.fireBall.angle)
                                ignoreCollide = 20 
                                Collide = False
                                player = 1
                                main.fireBall.rally +=1
                                
                    
            if (ignoreCollide > 0):
                ignoreCollide -= 1
            # GameOver    
            if(BallsLeft == 0):
                sounds[0].stop()
                if(wolverScore > rayScore):
                    winner = 1
                elif(rayScore > wolverScore):
                    winner = -1
                else:
                    winner = 0 
                GameOver.gameOver(screen, SCREEN_H, SCREEN_W,winner)
                '''Once the game is over, and gameover screen is closed: need to go back to game.stopped state
                '''
                main.gamestate = STOPPED
                sounds[0].play()
                global_param_reset()         
        
        main.render_score_circles()
        main.renderfonts(wolverScore,rayScore,BallsLeft) 
  
        pygame.display.flip()
        clock.tick(100)
            

if __name__ == "__main__":
    game(screen, SCREEN_H, SCREEN_W)
