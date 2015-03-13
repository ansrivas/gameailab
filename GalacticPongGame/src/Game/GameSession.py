import pygame
import random
import numpy as np
import math
from Reflection import reflectcollide as refcol


# Sound Initialization
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)

#  Playback song
sounds = []
sounds.append(pygame.mixer.Sound('./data/GameBackground.wav'))
sounds.append(pygame.mixer.Sound('./data/BallHit1.wav'))
sounds.append(pygame.mixer.Sound('./data/BallHit2.wav'))
sounds.append(pygame.mixer.Sound('./data/BallOut1.wav'))

# Set Screen Width and Screen Height 
SCREEN_W, SCREEN_H = (1280, 720)
screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))

# Number of Stars 
N = 500  

debug = False

class Color():
    white=(255,255,255)
    black=(0,0,0)
    blue = (0,255,255)
    red = (255,0,0)
    snow = (205,201,201)
    palegreen= (152,251,152)

    def __init__(self):
        pass
    

class Pong(pygame.sprite.Sprite):
    def __init__(self,pongdimension,speed,batimagepath,screen,SCREEN_H,SCREEN_W,initialPlace):
        pygame.sprite.Sprite.__init__(self)
      
        self.color = Color.red
        #self.width = width
        self.image = pygame.Surface(pongdimension).convert()
        self.image.fill((255,0,0))
        self.image.set_colorkey((255,0,0))
        
        self.x= 0
        self.y =0
        self.angle = 1
        self.theta =  initialPlace 
        self.speed = speed
        self.batdimx, self.batdimy = pongdimension
        
        self.image = pygame.image.load(batimagepath)
        if(debug):
            self.originalrect = pygame.draw.rect(self.image, self.color, (self.x,self.y,self.batdimx, self.batdimy ), 1)
        
        self.rot = pygame.transform.rotate(self.image,self.angle )
        
        self.rect = self.rot.get_rect()
        
        self.rect.center = (266,266)
        
        
        
    def findPointOnCircle(self,deg,screen,SCREEN_H,SCREEN_W):
        """
        Give an angle in degrees and we will get a corresponding point on circle w.r.t to this angle in clockwise.
        """
        rad = np.deg2rad(deg)
             
        y = (SCREEN_H/2) - 320 * math.sin(rad)
        x = (SCREEN_W/2) + 320 * math.cos(rad)
            
        return int(x),int(y)
    
    
    def update(self,changeDirection,screen,SCREEN_H,SCREEN_W):
        
        
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
        self.rect.center = self.findPointOnCircle(self.theta,screen,SCREEN_H,SCREEN_W)
        screen.blit(self.rot,self.rect)
 
    def resetbat(self):
        self.rect.center = (266,266)
       
class FireBall(pygame.sprite.Sprite):
    
    def __init__(self,ballDimension,imageName,screen,SCREEN_H,SCREEN_W):
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
        self.speedx = 2.5
        
        self.speedy = 2.5
        # Floating point representation of where the ball is
        self.x = SCREEN_W/2
        self.y = SCREEN_H/2
         
        # Direction of ball in degrees
        self.angle = np.pi/4.0
        self.angle = random.uniform(0,2*math.pi)
        
        '''This is the case where rally has been increased to a 20 , start increaing the speed after this to make it harder
        '''
        self.rally = 0
        
    def reset(self,SCREEN_H,SCREEN_W,player,BallsLeft):
        
        sounds[3].play()
        self.x = SCREEN_W/2
        self.y = SCREEN_H/2
        self.speedx=2.5
        self.speedy=2.5
        self.angle = random.uniform(0,2*math.pi)
        player *= -1 
        BallsLeft -= 1
        self.rally = 0
        return player,BallsLeft
    
    def update(self,screen,SCREEN_H,SCREEN_W,player,BallsLeft):
         
        # Change the position (x and y) according to the speed and direction
        self.x += math.cos(self.angle) * self.speedx
        self.y -= math.sin(self.angle) * self.speedy
  
        if self.y <= 0 or self.x <= 0:
            player,BallsLeft = self.reset(SCREEN_H,SCREEN_W,player,BallsLeft)
             
        if self.y >= SCREEN_H or self.x >= SCREEN_W:
            player,BallsLeft = self.reset(SCREEN_H,SCREEN_W,player,BallsLeft)
        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y
        
        '''If the rally continued for more than 5 times, 
            start increasing the speed of the ball to make it harder
        '''
        if(self.rally > 5):
            if(self.rally%5 == 0):
                self.increasespeed()
            
        screen.blit(self.image,self.rect)
        return player,BallsLeft

    def increasespeed(self):
        self.speedx += 0.005
        self.speedy += 0.005
        
        

class CGameState():
    RUNNING,STOPPED,PAUSED,RESET = 1,2,3,4
    def __init__(self):
        pass
    

gamestate = CGameState.STOPPED

class CMain():
    def __init__(self,screen, SCREEN_H,SCREEN_W):
        self.gamestate = CGameState.PAUSED
        self.MULTIPLAYER= None
        self.screen = screen
        self.background = None
        self.InnerOrange = None
        self.OuterOrange= None
        self.OuterWhite= None
        self.InnerWhite = None
        self.OuterBigWhite = None
        self.InnerBigWhite = None
        self.wolverPong = None
        self.rayPong = None
        self.fireBall = None
        self.stars = None
        self.font1 = None
        self.font2 = None
        
    def initgame(self):
        self.MULTIPLAYER = True
        #global SCREEN_W,SCREEN_H        
        # basic start
        pygame.init()
     
        pygame.display.set_caption('Galactic Pong') 
        # create background
        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        # set transparency for the circles
        InnerColorTone = 20
        OuterColorTone = 40

        # create surfaces for transparent circles (Scores)
        self.InnerOrange = pygame.Surface((200,200))
        self.InnerOrange.fill(Color.black)
        self.InnerOrange.set_colorkey(Color.black)
        self.InnerOrange.set_alpha(InnerColorTone)
        pygame.draw.circle(self.InnerOrange, (255,165,0,255),(100,100), 50)
        
        self.OuterOrange = pygame.Surface((200,200))
        self.OuterOrange.fill(Color.black)
        self.OuterOrange.set_colorkey(Color.black)
        self.OuterOrange.set_alpha(OuterColorTone)
        pygame.draw.circle(self.OuterOrange, (255,165,0,100),(100,100), 50,3)
        
        self.InnerWhite = pygame.Surface((200,200))
        self.InnerWhite.fill(Color.black)
        self.InnerWhite.set_colorkey(Color.black)
        self.InnerWhite.set_alpha(InnerColorTone)
        pygame.draw.circle(self.InnerWhite, (200,200,200,100),(100,100), 50)
        
        self.OuterWhite = pygame.Surface((200,200))
        self.OuterWhite.fill(Color.black)
        self.OuterWhite.set_colorkey(Color.black)
        self.OuterWhite.set_alpha(OuterColorTone)
        pygame.draw.circle(self.OuterWhite, (200,200,200,100),(100,100), 50,3)
        
        
        # set transparency for Big circles
        InnerBigColorTone = 20
        OuterBigColorTone = 40
  
        # Create surface for transparent game circles 
        self.InnerBigOrange =  pygame.Surface((SCREEN_W,SCREEN_H))
        self.InnerBigOrange.fill(Color.black)
        self.InnerBigOrange.set_colorkey(Color.black)
        self.InnerBigOrange.set_alpha(InnerBigColorTone)
        pygame.draw.circle(self.InnerBigOrange, (255,165,0,255),(SCREEN_W/2,SCREEN_H/2), 300)
        
        
        self.OuterBigOrange =  pygame.Surface((SCREEN_W,SCREEN_H))
        self.OuterBigOrange.fill(Color.black)
        self.OuterBigOrange.set_colorkey(Color.black)
        self.OuterBigOrange.set_alpha(OuterBigColorTone)
        pygame.draw.circle(self.OuterBigOrange, (255,165,0,255),(SCREEN_W/2,SCREEN_H/2), 300,4)
        
        self.InnerBigWhite =  pygame.Surface((SCREEN_W,SCREEN_H))
        self.InnerBigWhite.fill(Color.black)
        self.InnerBigWhite.set_colorkey(Color.black)
        self.InnerBigWhite.set_alpha(InnerBigColorTone)
        pygame.draw.circle(self.InnerBigWhite, (200,200,200,255),(SCREEN_W/2,SCREEN_H/2), 300)
        
        self.OuterBigWhite =  pygame.Surface((SCREEN_W,SCREEN_H))
        self.OuterBigWhite.fill(Color.black)
        self.OuterBigWhite.set_colorkey(Color.black)
        self.OuterBigWhite.set_alpha(OuterBigColorTone)
        pygame.draw.circle(self.OuterBigWhite, (200,200,200,255),(SCREEN_W/2,SCREEN_H/2), 300,4)


        self.stars = [
        [random.randint(0, SCREEN_W),random.randint(0, SCREEN_H)]
        for x in range(250)
        ]        
        
        # Score Font 
        self.font1 = pygame.font.SysFont("calibri",40)
        # Side Headings Font
        self.font2 = pygame.font.SysFont("Papyrus",30)
 
           
        # WolverPONG Call Function
        wolverpongimage = "./data/rWolverGamePONG.png"
        self.wolverPong = Pong((50,120),2,wolverpongimage,self.screen,SCREEN_H,SCREEN_W,180)             
         
            
        if(self.MULTIPLAYER):
            # RayPONG Call Function
            rayPongimage = "./data/RayGamePONG.png"
            self.rayPong = Pong((50,120),2,rayPongimage,self.screen,SCREEN_H,SCREEN_W,0) 
            
            
        # FireBall Call Function
        ballimage = "./data/ball.png"
        self.fireBall = FireBall((28,29), ballimage,self.screen,SCREEN_H,SCREEN_W)
        
    
    def update(self):

        pass
    
    def blitstars(self): 
        # Generate N Star Positions    
            
        self.background.fill(Color.black)     
        # Draw Stars (stars moving effect) 
        for star in self.stars:
            pygame.draw.line(self.background,(255, 255, 255), (star[0], star[1]), (star[0], star[1]))
            star[0] = star[0] - 1
            if star[0] < 0:
                star[0] = SCREEN_W
                star[1] = random.randint(0, SCREEN_H)
        
        self.screen.blit(self.background,(0,0)) 
     
    def renderfonts(self,wolverScore,rayScore,ballsleft):
                # Render Scores        
        wolverScoreRender = self.font1.render(str(wolverScore), True,(205,205,205))
        rayScoreRender = self.font1.render(str(rayScore), True,(205,205,205)) 
        # Render Balls Left
        BallsLeftRender = self.font2.render("BALLS LEFT : "+str(ballsleft), True,(205,205,205))
        # Render HighScore
        HighScoreRender = self.font2.render("HIGHSCORE : ", True,(205,205,205))
        screen.blit(wolverScoreRender,(188.,185.))
        screen.blit(rayScoreRender,(1068.,185.)) 
        
        self.screen.blit(BallsLeftRender,(10.,10.)) 
        self.screen.blit(HighScoreRender,(1000.,10.)) 
          
       
    def render_score_circles(self):
                # Display Score Circles
        self.screen.blit(self.OuterOrange, (100,100,100,100))
        self.screen.blit(self.InnerOrange, (100,100,100,100))
        self.screen.blit(self.OuterWhite, (980,100,100,100))
        self.screen.blit(self.InnerWhite, (980,100,100,100))
        
 
    
def game(screen,SCREEN_H,SCREEN_W):
    global gamestate
              
    main = CMain(screen, SCREEN_H,SCREEN_W)
    main.initgame()
    #class which calculates the collision and reflection
    calculate = refcol.CReflectCollid()

    # Play Background Music
    sounds[0].play()
    sounds[0].set_volume(0.3)
    
    # Number of Balls Left
    BallsLeft = 10
        
    # If collided once, dont check for the next n iterations
    ignoreCollide = 0
        
    wolverScore = 0
    rayScore = 0
    WolverchangeDirection = 0
    RaychangeDirection = 0

    Collide = False
 
    #Player turns
    player = 1      
    running = True
    clock = pygame.time.Clock()
    screen.blit(main.background,(0,0))

    
    while running:
        clock.tick(100) 
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
    
        main.blitstars()
        
        main.wolverPong.update(WolverchangeDirection,screen,SCREEN_H,SCREEN_W)
        if(main.MULTIPLAYER):
            main.rayPong.update(RaychangeDirection,screen,SCREEN_H,SCREEN_W)
            
        # Change turn if player loses the ball
        player,BallsLeft = main.fireBall.update(screen,SCREEN_H,SCREEN_W,player,BallsLeft) 
        '''
        Should we reset the location of bat also here???????????????????
        '''     
        if(BallsLeft > 0):
            
            #If collided, dont check for collision for next few iterations
            if (ignoreCollide==0):
                
                # WolverPong's Turn               
                if(player == 1):
                    # Draw Background Circle
                    screen.blit(main.OuterBigOrange,(0,0))
                    screen.blit(main.InnerBigOrange,(0,0))
                    
                    # Check Collision
                    Collide = calculate.checkCollide(main.fireBall.rect.centerx,main.fireBall.rect.centery,main.wolverPong.rect.centerx,main.wolverPong.rect.centery,np.deg2rad(main.wolverPong.angle),120,main.fireBall.angle)
                    
                    if Collide: 
                        # Increase Score by 1            
                        wolverScore += 1
                        sounds[1].play()     
                        main.fireBall.angle = calculate.reflectAngle(main.fireBall.rect.centerx,main.fireBall.rect.centery,main.wolverPong.rect.centerx,main.wolverPong.rect.centery,np.deg2rad(main.wolverPong.angle),main.fireBall.angle)              
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
                        Collide = calculate.checkCollide(main.fireBall.rect.centerx,main.fireBall.rect.centery,main.rayPong.rect.centerx,main.rayPong.rect.centery,np.deg2rad(main.rayPong.angle),120,main.fireBall.angle)  
                        
                           
                        if Collide:
                            # Increase Score by 1
                            rayScore += 1  
                            sounds[2].play()
                            main.fireBall.angle = calculate.reflectAngle(main.fireBall.rect.centerx,main.fireBall.rect.centery,main.rayPong.rect.centerx,main.rayPong.rect.centery,np.deg2rad(main.rayPong.angle),main.fireBall.angle)
                            ignoreCollide = 20 
                            Collide = False
                            player = 1
                            main.fireBall.rally +=1
                            
        
        main.render_score_circles()
        main.renderfonts(wolverScore,rayScore,BallsLeft) 
        pygame.display.flip()
        
        if (ignoreCollide > 0):
            ignoreCollide -= 1
        # GameOver    
        if(BallsLeft == 0):
            running = False
            
            

if __name__ == "__main__":
    game(screen,SCREEN_H,SCREEN_W)