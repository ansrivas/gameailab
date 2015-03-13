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
        self.speedx = 7
        
        self.speedy = 7
        # Floating point representation of where the ball is
        self.x = SCREEN_W/2
        self.y = SCREEN_H/2
         
        # Direction of ball in degrees
        self.angle = np.pi/4.0
        self.angle = random.uniform(0,2*math.pi)
        
         
        
        
        
        
    
    
    def reset(self,screen,SCREEN_H,SCREEN_W,player,BallsLeft):
        sounds[3].play()
        self.x = SCREEN_W/2
        self.y = SCREEN_H/2
        self.speedx=7
        self.speedy=7
        self.angle = random.uniform(0,2*math.pi)
        player *= -1 
        BallsLeft -= 1
        return player,BallsLeft
    
    def update(self,screen,SCREEN_H,SCREEN_W,player,BallsLeft):
        
        # Sine and Cosine work in degrees, so we have to convert them
        #direction_radians = math.radians(self.direction)
        
         
        # Change the position (x and y) according to the speed and direction
        self.x += math.cos(self.angle) * self.speedx
        self.y -= math.sin(self.angle) * self.speedy
        
        
        
        
        
        if self.y <= 0 or self.x <= 0:
            player,BallsLeft = self.reset(screen,SCREEN_H,SCREEN_W,player,BallsLeft)
             
        if self.y >= SCREEN_H or self.x >= SCREEN_W:
            player,BallsLeft = self.reset(screen,SCREEN_H,SCREEN_W,player,BallsLeft)
        
        
        
        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y
        
        screen.blit(self.image,self.rect)
        return player,BallsLeft

def game(screen,SCREEN_H,SCREEN_W,N):
    
              
    MULTIPLAYER = True
    #global SCREEN_W,SCREEN_H
    
    # If collided once, dont check for the next n iterations
    ignoreCollide = 0
    
    # basic start
    pygame.init()
    
       
    pygame.display.set_caption('Galactic Pong')
    running = True
    
    
    # create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    
    # create surfaces for transparent circles (Scores)
    InnerOrange = pygame.Surface((200,200))
    InnerOrange.fill(Color.black)
    InnerOrange.set_colorkey(Color.black)
    pygame.draw.circle(InnerOrange, (255,165,0,255),(100,100), 50)
    
    OuterOrange = pygame.Surface((200,200))
    OuterOrange.fill(Color.black)
    OuterOrange.set_colorkey(Color.black)
    pygame.draw.circle(OuterOrange, (255,165,0,100),(100,100), 50,3)
    
    InnerWhite = pygame.Surface((200,200))
    InnerWhite.fill(Color.black)
    InnerWhite.set_colorkey(Color.black)
    pygame.draw.circle(InnerWhite, (200,200,200,100),(100,100), 50)
    
    OuterWhite = pygame.Surface((200,200))
    OuterWhite.fill(Color.black)
    OuterWhite.set_colorkey(Color.black)
    pygame.draw.circle(OuterWhite, (200,200,200,100),(100,100), 50,3)
    
    # set transparency for the circles
    InnerColorTone = 20
    OuterColorTone = 40
    OuterOrange.set_alpha(OuterColorTone)
    InnerOrange.set_alpha(InnerColorTone)
    OuterWhite.set_alpha(OuterColorTone)
    InnerWhite.set_alpha(InnerColorTone)
    
    # Create surface for transparent game circles 
    InnerBigOrange =  pygame.Surface((SCREEN_W,SCREEN_H))
    InnerBigOrange.fill(Color.black)
    InnerBigOrange.set_colorkey(Color.black)
    pygame.draw.circle(InnerBigOrange, (255,165,0,255),(SCREEN_W/2,SCREEN_H/2), 300)
    
    
    OuterBigOrange =  pygame.Surface((SCREEN_W,SCREEN_H))
    OuterBigOrange.fill(Color.black)
    OuterBigOrange.set_colorkey(Color.black)
    pygame.draw.circle(OuterBigOrange, (255,165,0,255),(SCREEN_W/2,SCREEN_H/2), 300,4)
    
    InnerBigWhite =  pygame.Surface((SCREEN_W,SCREEN_H))
    InnerBigWhite.fill(Color.black)
    InnerBigWhite.set_colorkey(Color.black)
    pygame.draw.circle(InnerBigWhite, (200,200,200,255),(SCREEN_W/2,SCREEN_H/2), 300)
    
    OuterBigWhite =  pygame.Surface((SCREEN_W,SCREEN_H))
    OuterBigWhite.fill(Color.black)
    OuterBigWhite.set_colorkey(Color.black)
    pygame.draw.circle(OuterBigWhite, (200,200,200,255),(SCREEN_W/2,SCREEN_H/2), 300,4)
    
    # set transparency for Big circles
    InnerBigColorTone = 20
    OuterBigColorTone = 40
    OuterBigOrange.set_alpha(OuterBigColorTone)
    InnerBigOrange.set_alpha(InnerBigColorTone)
    OuterBigWhite.set_alpha(OuterBigColorTone)
    InnerBigWhite.set_alpha(InnerBigColorTone)
       
    
    # Score Font 
    font = pygame.font.SysFont("calibri",40)
    # Side Headings Font
    Sfont = pygame.font.SysFont("Papyrus",30)
    
    
    # Generate N Star Positions    
    stars = [
    [random.randint(0, SCREEN_W),random.randint(0, SCREEN_H)]
    for x in range(250)
    ]
    
    
    #class which calculates the collision and reflection
    calculate = refcol.CReflectCollid()
    
    #TODO: need to fix this function here
    #backg = bg.CBackground((SCREEN_W/2, SCREEN_H/2),320,5,Color.palegreen)
    
    # WolverPONG Call Function
    wolverpongimage = "./data/rWolverGamePONG.png"
    wolverPong = Pong((50,120),2,wolverpongimage,screen,SCREEN_H,SCREEN_W,180) 
    WolverchangeDirection = 0
    
    if(MULTIPLAYER):
        # RayPONG Call Function
        rayPongimage = "./data/RayGamePONG.png"
        rayPong = Pong((50,120),2,rayPongimage,screen,SCREEN_H,SCREEN_W,0) 
        RaychangeDirection = 0
        
    # FireBall Call Function
    ballimage = "./data/ball.png"
    fireBall = FireBall((28,29), ballimage,screen,SCREEN_H,SCREEN_W)
    balls = pygame.sprite.Group()
    balls.add(fireBall)
    
    movingsprites = pygame.sprite.Group()
    movingsprites.add(wolverPong)
    if(MULTIPLAYER):
        movingsprites.add(rayPong)
    movingsprites.add(fireBall)

    Collide = False
    clock = pygame.time.Clock()
    
    screen.blit(background,(0,0))
    
    wolverScore = 0
    rayScore = 0
    
    #Player turns
    player = 1
    
    # Play Background Music
    sounds[0].play()
    sounds[0].set_volume(0.3)
    
    # Number of Balls Left
    BallsLeft = 10
    
    while running:
        clock.tick(100) 
        # Change value if single player
        if not MULTIPLAYER:
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
                        
        background.fill(Color.black) 
        
        
                 
        # Draw Stars (stars moving effect) 
        for star in stars:
            pygame.draw.line(background,(255, 255, 255), (star[0], star[1]), (star[0], star[1]))
            star[0] = star[0] - 1
            if star[0] < 0:
                star[0] = SCREEN_W
                star[1] = random.randint(0, SCREEN_H)
        
        screen.blit(background,(0,0)) 
         
        
        wolverPong.update(WolverchangeDirection,screen,SCREEN_H,SCREEN_W)
        if(MULTIPLAYER):
            rayPong.update(RaychangeDirection,screen,SCREEN_H,SCREEN_W)
            
        # Change turn if player loses the ball
        player,BallsLeft = fireBall.update(screen,SCREEN_H,SCREEN_W,player,BallsLeft) 
        
             
        if(BallsLeft > 0):
            
            #If collided, dont check for collision for next few iterations
            if (ignoreCollide==0):
                
                # WolverPong's Turn               
                if(player == 1):
                    # Draw Background Circle
                    screen.blit(OuterBigOrange,(0,0))
                    screen.blit(InnerBigOrange,(0,0))
                    
                    # Check Collision
                    Collide = calculate.checkCollide(fireBall.rect.centerx,fireBall.rect.centery,wolverPong.rect.centerx,wolverPong.rect.centery,np.deg2rad(wolverPong.angle),120,fireBall.angle)
                    
                    if Collide: 
                        # Increase Score by 1            
                        wolverScore += 1
                        sounds[1].play()     
                        fireBall.angle = calculate.reflectAngle(fireBall.rect.centerx,fireBall.rect.centery,wolverPong.rect.centerx,wolverPong.rect.centery,np.deg2rad(wolverPong.angle),fireBall.angle)              
                        ignoreCollide = 20    
                        Collide = False
                        player = -1
                        
                # RayPong's Turn            
                if(MULTIPLAYER):
                    if(player == -1):
                        # Draw Background Circle
                        screen.blit(OuterBigWhite,(0,0))
                        screen.blit(InnerBigWhite,(0,0))
                        
                        # Check Collision
                        Collide = calculate.checkCollide(fireBall.rect.centerx,fireBall.rect.centery,rayPong.rect.centerx,rayPong.rect.centery,np.deg2rad(rayPong.angle),120,fireBall.angle)  
                        
                           
                        if Collide:
                            # Increase Score by 1
                            rayScore += 1  
                            sounds[2].play()
                            fireBall.angle = calculate.reflectAngle(fireBall.rect.centerx,fireBall.rect.centery,rayPong.rect.centerx,rayPong.rect.centery,np.deg2rad(rayPong.angle),fireBall.angle)
                            ignoreCollide = 20 
                            Collide = False
                            player = 1
        # Render Scores        
        wolverScoreRender = font.render(str(wolverScore), True,(205,205,205))
        rayScoreRender = font.render(str(rayScore), True,(205,205,205)) 
        # Render Balls Left
        BallsLeftRender = Sfont.render("BALLS LEFT : "+str(BallsLeft), True,(205,205,205))
        # Render HighScore
        HighScoreRender = Sfont.render("HIGHSCORE : ", True,(205,205,205))
        
        # Display Score Circles
        screen.blit(OuterOrange, (100,100,100,100))
        screen.blit(InnerOrange, (100,100,100,100))
        screen.blit(OuterWhite, (980,100,100,100))
        screen.blit(InnerWhite, (980,100,100,100))
        
        screen.blit(wolverScoreRender,(188.,185.))
        screen.blit(rayScoreRender,(1068.,185.)) 
        
        screen.blit(BallsLeftRender,(10.,10.)) 
        screen.blit(HighScoreRender,(1000.,10.)) 
           
        pygame.display.flip()
        
        if (ignoreCollide > 0):
            ignoreCollide -= 1
        # GameOver    
        if(BallsLeft == 0):
            running = False
            
            

'''if __name__ == "__main__":
    main()'''