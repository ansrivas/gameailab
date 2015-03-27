import pygame
import time, pickle
import math, random, numpy as np
from constants import *
from Reflection import reflectcollide as refcol
from LineCircleIntersection import findIntersectPoints as PointsIntersect
from FuzzyController import fuzzyControl as fuzzy
from Game import GameOver
from logger.CLogger import Output
from Networks import neuralnets as NN


SCREEN = pygame.display.set_mode(RESOLUTION, 0, 32)

'''just using a naive global logger
'''
log = None
debug = False

#  Playback sound
sounds = []
sounds.append(pygame.mixer.Sound('./data/GameBackground.wav'))
sounds.append(pygame.mixer.Sound('./data/BallHit1.wav'))
sounds.append(pygame.mixer.Sound('./data/BallHit2.wav'))
sounds.append(pygame.mixer.Sound('./data/BallOut1.wav'))
sounds.append(pygame.mixer.Sound('./data/hitball.wav'))

bombexplosion = pygame.mixer.Sound('./data/boom.wav')


def findPointOnCircle(deg):
    """ Returns the x,y coordinates of the corresponding angle (given in degrees) """

    rad = np.deg2rad(deg)
    x = (SCREEN_W/2) + RADIUS * math.cos(rad)
    y = (SCREEN_H/2) - RADIUS * math.sin(rad)

    return int(x),int(y)

def findAngle((x, y)):
    dy = y - SCREEN_H/2
    dx = x - SCREEN_W/2
    
    angle  = -np.rad2deg(np.arctan2(dy, dx))
    if(angle < 0):
        angle += 360
    
    return int(np.round(angle))
    


class Pong(pygame.sprite.Sprite):
    """ Sprite Class for Pong bats - WolverPong, RayPong """

    def __init__(self, batImagePath, initialAngle, pongDimension=(50, 120), speed=1):
        super(Pong, self).__init__()
      
        self.x = self.y = 0
        self.angle = initialAngle
        self.batdimx, self.batdimy = pongDimension
        self.image = pygame.image.load(batImagePath)
        self.score = 0
        self.changeDirection = 0
        self.speed = speed
        self.maxSpeed = 3
        self.speed_factor = 1.0
        self.rot = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rot.get_rect()
        
    def update(self, changeDirection=None):
        if changeDirection != None:
            if self.speed < self.maxSpeed:
                self.speed *= self.speed_factor
            else:
                self.speed = self.maxSpeed
            
            if changeDirection > 0:
                self.angle += self.speed
            elif changeDirection < 0:
                if self.angle > 0:
                    self.angle -= self.speed
                else:
                    self.angle = 360 - self.speed
                
            if self.angle >= 360:
                self.angle = 0
        
        self.rot = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rot.get_rect()
        self.rect.center = findPointOnCircle(self.angle)
        SCREEN.blit(self.rot, self.rect)
 
    def resetbat(self, initialAngle):
        """ Reset Bat's properties - give 'InitialAngle' in degrees """

        self.angle =  initialAngle
        self.speed = 1
        self.speed_factor = 1.0


class FireBall(pygame.sprite.Sprite):
    """ Sprite Class for pong ball - FireBall"""
    
    def __init__(self, ballDimension=(28,29), ballImage="./data/ball.png"):
        # Call the parent class (Sprite) constructor
        super(FireBall, self).__init__()
         
        self.image = pygame.image.load(ballImage)
        self.rect = self.image.get_rect()
        
        # Set an offset and start the ball around the center of the ring with given offset
        self.center_offset = 30
        self.rect.center = (SCREEN_W/2 + np.random.randint(20, self.center_offset), \
                            SCREEN_H/2 - np.random.randint(20, self.center_offset))
        self.x, self.y = self.rect.center

        # Speed in pixels per cycle
        self.speedx = self.speedy = DEFAULT_BALL_SPEED

        # Direction of ball in degress
        self.angle = np.rad2deg(np.random.uniform(0, 2*math.pi))
        
        # Offset values (in pixels) to reset the ball once it crosses this much outside the ring
        self.offset = 70
        '''
        This is the case where rally has been increased to a 20, start increasing the speed 
        after this to make it harder
        '''
        self.rally = 0
        # To get points on the ball's trajectory 
        self.pointCount = 0
        
    def resetBall(self):
        self.pointCount = 0
        self.speedx = self.speedy = DEFAULT_BALL_SPEED
        self.rect.center = (SCREEN_W/2 + np.random.randint(20, self.center_offset), \
                            SCREEN_H/2 - np.random.randint(20, self.center_offset))
        self.x, self.y = self.rect.center
        self.angle = np.rad2deg(np.random.uniform(0, 2*math.pi))
        self.rally = 0
   

    def update(self, player, ballsLeft):
        # Change the position (x and y) according to the speed and direction
        rad = np.deg2rad(self.angle)
        self.x += math.cos(rad) * self.speedx
        self.y -= math.sin(rad) * self.speedy

        # Reset the ball position if it goes out of the circle (+ offset value)
        if math.sqrt((self.x - SCREEN_W/2)**2 + (self.y - SCREEN_H/2)**2) >= (RADIUS + self.offset):
            self.resetBall()
            player *= -1
            ballsLeft -= 1
             
        # Move the image to where our x and y are
        self.rect.center = self.x, self.y
        
        '''If the rally continued for more than 3 times, 
            start increasing the speed of the ball to make it harder
        '''
        if self.rally > 0:
            if self.rally%3 == 0:
                self.increasespeed()
            
        SCREEN.blit(self.image, self.rect)

        return player, ballsLeft

    def increasespeed(self):
        """ Increase the ball speed after a successful rally, so as to increase difficulty """
        self.speedx += 0.005
        self.speedy += 0.005
        

class CBombs(pygame.sprite.Sprite):
    """ Class for generating  and managing Bombs """
    
    def __init__(self,loc):
        super(CBombs,self).__init__()
        self.image = pygame.image.load('./data/bomb.png').convert()
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = loc
        self.explosion_frame = []
        
        sprite_sheet = SpriteSheet("./data/explosion.png") 
        for y in range(1,6,1):
            for i in range(1,6,1):
                image = sprite_sheet.get_image(64*(i-1), 64*(y-1), 64, 64)
                self.explosion_frame.append(image)

        self.frame_num = 0 
        #self.image = self.explosion_frame[self.frame_num]
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = loc
        self.interval = 0.05
        self.playanimation = False
        
    def update(self):
        if self.playanimation:
            self.play_burning_animation()
        SCREEN.blit(self.image,self.rect)
     
    def play_burning_animation(self):
        maxlen = len(self.explosion_frame)
       
        bombexplosion.play()
        if self.playanimation:
            if self.frame_num >= maxlen:
                '''kill the sprites after animation is done playing'''
                self.frame_num =0
                self.playanimation = False
                self.kill()
            
            else:               
                self.image = self.explosion_frame[self.frame_num]
                self.frame_num +=1
                SCREEN.blit(self.image,self.rect)
            

class SpriteSheet(object):
    """ Class used to grab images (individual sprites) out of a sprite sheet. """

    # This points to our sprite sheet image
    sprite_sheet = None
 
    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """
 
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()
 
 
    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
 
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
 
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
 
        # Assuming black works as the transparent color
        image.set_colorkey(BLACK)
 
        # Return the image
        return image      
        

class Game:
    """ Main Class that contains Game related methods """
    
    def __init__(self, neuralNetPickle=None):
        """ Initialize the game state """
        # Sound Initialization
        pygame.mixer.pre_init(44100, -16, 2, 4096)

        pygame.init()
        pygame.display.set_caption('Galactic Pong')

        # Set it TRUE to enable multiplayer
        self.MULTIPLAYER = True

        # set it 'AUTO' to play with AI, or 'MANUAL' to play with another human player 
        self.mode = AUTO
        
        self.gamestate = RUNNING
        
        # Currently Random value is set... Can connect to DB...
        self.highScore = 100
        
        self.stars = [
            [np.random.randint(0, SCREEN_W), np.random.randint(0, SCREEN_H)]
            for _ in range(numStars)
        ]
 
        """ AI Parameters """

        # Self.ball contains (x1,y1, x2, y2)
        self.ball = np.zeros(4)
        
        # Predicted Bat points and angle
        self.ballAngle = self.batAngle = 0.0
        
        # Self.predictedBatPoint contains (x1,y1, x2, y2)
        self.predictedBatPoint = np.zeros(4)

        # Find the best fit among the the 2 points
        self.predictedBatAngle = self.predictedBatPointFinalX = self.predictedBatPointFinalY = 0.0
        
        # Move AI bat after opposite player's move
        self.aiMoveCount = 0
        self.aiMoveCountIncrease = 0
        
        # Predicted angle of AI bat, before AI player's turn
        self.beforePredictedBatPointAngle = 0.0
        
        self.background = pygame.Surface(SCREEN.get_size()).convert()

        self.scoreFont = pygame.font.SysFont("calibri",40)
        self.headingFont = pygame.font.SysFont("Papyrus",30)

        Wolverpongimage = "./data/rWolverGamePONG.png"
        self.WolverPong = Pong(Wolverpongimage, 180)

        if self.MULTIPLAYER:
            RayPongimage = "./data/RayGamePONG.png"
            self.RayPong = Pong(RayPongimage, 0)

        self.fireBall = FireBall()
        self.ballsLeft = TOTAL_BALLS
        self.Collide = False
        self.ignoreCollide = 0

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

        self.bomb_group = pygame.sprite.Group()
        self.numofBombs = 5
        self.points = None
            
                
        '''call this just once so as to randomly initialize obstacles'''
        self.generateNbombsinCircle(self.numofBombs)

        # Initializations for Neural Network
        self.inputData = self.outputData = None
        self.neuralNetPickle = neuralNetPickle
        
    def resetBombLocation(self):
        """ reset all the bomb location after the game is reset """

        np.random.shuffle(self.points)
        points = random.sample(self.points,self.numofBombs)
        
        self.bomb_group.empty()
        for p in points:
            bomb = CBombs(p)
            self.bomb_group.add(bomb) 
           
    def generateNbombsinCircle(self,num=3):

        with open('points.txt', 'rb') as f:
            self.points = pickle.load(f)
    
        np.random.shuffle(self.points)
        points = random.sample(self.points,num)
        
        for p in points:
            bomb = CBombs(p)
            self.bomb_group.add(bomb)
        
        #-----------------We need this code to generate N points inside the circle, current implementation is buggy------------
        '''
        listofpoints = []
        
        for x in range(SCREEN_W/2 - 280 ,SCREEN_W + 280) :
            
            for y in range(SCREEN_H/2 -280,SCREEN_H/2 + 280):

                if   abs((x-SCREEN_W/2)+(y-SCREEN_H/2)*1j) <= 280:
                    listofpoints.append((x,y))
           
        print len(listofpoints)    
        random.shuffle(listofpoints)     
        points = random.sample(listofpoints,num)
        
        for p in points:
            bomb = CBombs(p,colortone=120)
            self.bomb_group.add(bomb)            
        with open('points.txt', 'wb') as f:
            pickle.dump(listofpoints, f)
        '''        
        
    def setCircles(self, alpha, color=(255,165,0,255), width=0, radius=50, pos=(100, 100), \
                        surfacePos=(200, 200), fill=BLACK, colorkey=BLACK):
        """ Draw circles at a given position with given properties """
        obj = pygame.Surface(surfacePos)
        obj.fill(fill)
        obj.set_colorkey(colorkey)
        obj.set_alpha(alpha)
        pygame.draw.circle(obj, color, pos, radius, width)

        return obj

    def blitstars(self):
        """ Generate N Star Positions """

        self.background.fill(BLACK)
        # Draw Stars (stars moving effect)
        for star in self.stars:
            pygame.draw.line(self.background,(255, 255, 255), (star[0], star[1]), (star[0], star[1]))
            star[0] -= 1
            if star[0] < 0:
                star[0] = SCREEN_W
                star[1] = np.random.randint(0, SCREEN_H)

        SCREEN.blit(self.background,(0,0))

    def renderScores(self, ballsLeft, WolverScore, RayScore=None):
        """ Blit Scores in generated score circles """

        BallsLeftRender = self.headingFont.render("BALLS LEFT : " +str(ballsLeft), True, (205,205,205))
        HighScoreRender = self.headingFont.render("HIGHSCORE : " +str(self.highScore), True, (205,205,205))
        SCREEN.blit(BallsLeftRender,(10.,10.))
        SCREEN.blit(HighScoreRender,(1000.,10.))

        WolverScoreRender = self.scoreFont.render(str(WolverScore), True, (205,205,205))
        SCREEN.blit(WolverScoreRender,(188.,185.))
        if self.MULTIPLAYER:
            RayScoreRender = self.scoreFont.render(str(RayScore), True, (205,205,205))
            SCREEN.blit(RayScoreRender,(1068.,185.))

    def render_score_circles(self):
        """ Display Score Circles """

        SCREEN.blit(self.OuterOrange, (100,100,100,100))
        SCREEN.blit(self.InnerOrange, (100,100,100,100))

        if self.MULTIPLAYER:
            SCREEN.blit(self.OuterWhite, (980,100,100,100))
            SCREEN.blit(self.InnerWhite, (980,100,100,100))
     
    def delayGame(self, WolverScore, RayScore, ballsLeft, st, seconds=3):
        """ Delay the game (in seconds) for a certain given time (Default: 3) """
        
        while(seconds > 0):
            self.blitstars()
            self.render_score_circles()
            self.renderScores(ballsLeft, WolverScore, RayScore)
            renderSeconds = self.headingFont.render(st+str(seconds), True, (205,205,205))
            SCREEN.blit(renderSeconds,(525.,10.))

            pygame.display.flip()
            time.sleep(1.)
            seconds -=1

    def resetGame(self):
        """ Reset entire game state """

        self._global_param_reset()
        #self.gamestate = None
        self.MULTIPLAYER = True

        self.WolverPong.resetbat(180)
        if self.MULTIPLAYER:
            self.RayPong.resetbat(0)
        self.resetBombLocation()
        
        #call self.fireballreset in the end of this resetting sequence only
        self.fireBall.resetBall()
        
    def render_pause_screen(self):
        renderPause = self.headingFont.render("Game Paused: press Space Bar to resume", True, (205,205,205))
        SCREEN.blit(renderPause,(380.,100.))

    def render_stop_screen(self):
        renderStop = self.headingFont.render("Game Stopped: press Space Bar to restart", True, (205,205,205))
        SCREEN.blit(renderStop,(380.,100.))

    def _global_param_reset(self):
        """ Reset all parameters which are being used in main game loop """

        self.ballsLeft = TOTAL_BALLS
        self.Collide = False
        self.ignoreCollide = 0
        self.WolverPong.score = 0
        self.WolverPong.changeDirection = 0

        if self.MULTIPLAYER:
            self.RayPong.score = 0
            self.RayPong.changeDirection = 0

    def check_bomb_ball_collide(self):
        collide_list = pygame.sprite.spritecollide(self.fireBall, self.bomb_group, False)
         
        for block in collide_list:
            block.playanimation = True

    def directionToPredict(self, batAngle, predictedBatAngle):
   
        way1 = abs(batAngle - predictedBatAngle)
        way2 = 360 - way1
                                    
        if min(way1, way2) == way1:
            if predictedBatAngle < batAngle:
                direction = -1
            else:
                direction = 1
        else:
            if predictedBatAngle > batAngle:
                direction = -1
            else:
                direction = 1                   
            
        #the angle between batangle and predicted batangle became too small, so dont change the directions now
        if (min(way1, way2) < 1.5):
            direction = 0

        return direction
                
    def Run(self):
        """ Run the game """
        
        global log
        
        #class which calculates the collision and reflection
        calculate = refcol.CReflectCollid()
        
        #class for Line Circle Intersection
        intersect = PointsIntersect.FindIntersection()

        #class to predict acceleration - Fuzzy
        fuzzyAcceleration = fuzzy.Fuzzy()
        
        # Class object for Neural Network
        net = NN.CNeuralNet()
        if self.neuralNetPickle != None:
            net.mlpnetwork = net.loadTrainedModel(self.neuralNetPickle)
        
        # Play Background Music
        sounds[0].set_volume(MED_VOL)
        sounds[0].play()
    
        # Player turns - 1, -1 for WolverPong and RayPong respectively
        player = 1
        running = True
        clock = pygame.time.Clock()
        SCREEN.blit(self.background,(0,0))
        st = "Game starts in : "
        self.delayGame(WolverScore=0, RayScore=0, ballsLeft=0,st=st)

        while running:
            
            # Change value if single player
            if not self.MULTIPLAYER:
                player = 1
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                ''' WolverPONG MOVEMENTS - A,D'''
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_a]:
                        if player == 1:
                            self.aiMoveCountIncrease = 1
                        self.WolverPong.changeDirection = 1
                        ''' increase the speed in case of continues pressing'''
                        self.WolverPong.speed_factor = 1.01

                    elif keys[pygame.K_d]:
                        if player == 1:
                            self.aiMoveCountIncrease = 1
                        self.WolverPong.changeDirection = -1
                        ''' increase the speed in case of continues pressing'''
                        self.WolverPong.speed_factor = 1.01

                    if self.MULTIPLAYER:
                        if self.mode == MANUAL:
                            if keys[pygame.K_LEFT]:
                                self.RayPong.changeDirection = 1
                                self.RayPong.speed_factor = 1.01

                            elif keys[pygame.K_RIGHT]:
                                self.RayPong.changeDirection = -1
                                self.RayPong.speed_factor = 1.01

                    if keys[pygame.K_SPACE]:
                        if self.gamestate == RUNNING:
                            self.gamestate = PAUSED
                        elif self.gamestate == PAUSED:
                            self.gamestate = RUNNING
                            st = "Resuming in: "
                            self.delayGame(self.WolverPong.score, self.RayPong.score, self.ballsLeft, st)
                        elif self.gamestate == STOPPED:
                            self.resetGame()
                            player = 1
                            st = "Game restarts in: "
                            self.delayGame(self.WolverPong.score, self.RayPong.score, self.ballsLeft, st)
                            self.gamestate = RUNNING

                    if keys[pygame.K_r] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                        if (self.gamestate == RUNNING) or (self.gamestate == PAUSED):
                            self.resetGame()
                            st = "Resetting in: "
                            self.delayGame(self.WolverPong.score, self.RayPong.score, self.ballsLeft, st)
                            self.gamestate = RUNNING

                    if keys[pygame.K_q] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                        if (self.gamestate == RUNNING) or (self.gamestate == PAUSED):
                            self.resetGame()
                            self.gamestate = STOPPED

                elif event.type == pygame.KEYUP:
                    if (event.key == pygame.K_a) or (event.key == pygame.K_d):
                        if player == 1:
                            self.aiMoveCountIncrease = 0
                            self.aiMoveCount = 0
                        self.WolverPong.changeDirection = 0
                        ''' reset the speed back once the key is left'''
                        self.WolverPong.speed = 1.0
                        self.WolverPong.speed_factor = 1.0

                    if self.MULTIPLAYER:
                        if self.mode == MANUAL:
                            if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                                self.RayPong.changeDirection = 0
                                self.RayPong.speed = 1.0
                                self.RayPong.speed_factor = 1.0
            
            self.aiMoveCount += self.aiMoveCountIncrease
            self.blitstars()
            
            if self.gamestate == STOPPED:
                self.render_stop_screen()
    
            if self.gamestate == PAUSED:
                self.render_pause_screen()
    
            if self.gamestate == RUNNING:
                self.bomb_group.update()
                self.check_bomb_ball_collide()
                
                self.WolverPong.update(self.WolverPong.changeDirection)
                if self.MULTIPLAYER:
                    if self.mode == MANUAL:
                        self.RayPong.update(self.RayPong.changeDirection)
                    elif self.mode == AUTO:
                        self.RayPong.update()
    
                # Change turn if player loses the ball
                player, self.ballsLeft = self.fireBall.update(player, self.ballsLeft)
               
                if self.ballsLeft > 0:
                    #If collided, don't check for collision for next few iterations
                    if self.ignoreCollide == 0:

                        # WolverPong's Turn
                        if player == 1:
                            # Revert count after change in turn
                            self.fireBall.pointCount = 0
                            
                            # Draw Background Circle
                            SCREEN.blit(self.OuterBigOrange,(0,0))
                            SCREEN.blit(self.InnerBigOrange,(0,0))
    
                            # Check Collision
                            Collide = calculate.checkCollide(self.fireBall.rect.center, self.WolverPong.rect.center, \
                                                             np.deg2rad(self.WolverPong.angle),self.WolverPong.batdimy, \
                                                             np.deg2rad(self.fireBall.angle))
    
                            if Collide:
                                self.WolverPong.score += 1
                                sounds[4].play()
                                self.fireBall.angle = calculate.reflectAngle(self.fireBall.rect.center, \
                                                                             self.WolverPong.rect.center, \
                                                                             np.deg2rad(self.WolverPong.angle), \
                                                                             np.deg2rad(self.fireBall.angle))

                                self.fireBall.angle = np.rad2deg(self.fireBall.angle)
                                ignoreCollide = 20
                                Collide = False
                                player = -1
                                self.fireBall.rally +=1
                                self.aiMoveCount = 0

                        # RayPong's Turn
                        if self.MULTIPLAYER:
                            if player == -1:
                                # Draw Background Circle
                                SCREEN.blit(self.OuterBigWhite,(0,0))
                                SCREEN.blit(self.InnerBigWhite,(0,0))
                        
                                if self.mode == AUTO:
                                    if self.neuralNetPickle != None:
                                        self.inputData = [
                                                            self.fireBall.rect.center[0],
                                                            self.fireBall.rect.center[1],
                                                            self.fireBall.angle,
                                                            self.fireBall.speedx,
                                                            self.fireBall.speedy,
                                                         ]
                                        self.outputData = net.predict(self.inputData)
                            
                                        self.RayPong.angle = self.outputData[0]
                                        self.RayPong.speed = self.outputData[1]
                            
                                        self.RayPong.angle = int(np.round(self.RayPong.angle))
                                        print self.RayPong.angle,"angle is---------"
                                        self.RayPong.update()
                            
                                    else:  # If Fuzzy or something...
                            
                                        self.batAngle = self.RayPong.angle
                            
                                        # Get any point on ball's trajectory, In our case "3"
                                        if self.fireBall.pointCount == 3:
                                            self.ballAngle = self.fireBall.angle
                                            self.ball[:2] = self.fireBall.rect.center
                            
                                        # Get another point on ball's trajectory, In our case "6"
                                        if self.fireBall.pointCount == 6:
                                            self.ball[2:] = self.fireBall.rect.center
                            
                                            # Predict bat coordinates according to ball angle
                                            self.predictedBatPoint = intersect.lineCircleIntersect(self.ball, self.ballAngle)
                                            self.predictedBatAngle = findAngle(self.predictedBatPoint)
    
                                            # Get the acceleration by defuzzifying
                                            acceleration = fuzzyAcceleration.getFuzzyAcceleration(self.batAngle, self.predictedBatAngle)
                            
                                        # After getting the Best Fit , move Bat
                                        if self.fireBall.pointCount > 6:
                                            self.RayPong.changeDirection = self.directionToPredict(self.batAngle, self.predictedBatAngle)
                                            self.RayPong.speed_factor = self.RayPong.speed + acceleration
                            
                                            # If bat has reached it's target, reset speed and acceleration to avoid wobbling
                                            if self.RayPong.changeDirection == 0:
                                                self.RayPong.speed = 1
                                                self.RayPong.speed_factor = 1
                            
                                            self.RayPong.update(self.RayPong.changeDirection)
                            
                                            if debug:
                                                print "BAT POINTS PREDICTED : ",self.predictedBatPoint
                                                print "Current Bat Angle : ",self.batAngle,"Current Ball Angle : ",np.rad2deg(self.fireBall.angle),"Predicted Bat Angle : ",self.predictedBatAngle
                            
                                        self.fireBall.pointCount += 1
                            
    #                                 Check Collision
    #                                 Collide = pygame.sprite.collide_rect(self.fireBall, self.RayPong)
                                Collide = calculate.checkCollide(self.fireBall.rect.center, self.RayPong.rect.center, \
                                                                 np.deg2rad(self.RayPong.angle), self.RayPong.batdimy, \
                                                                 np.deg2rad(self.fireBall.angle))
                        
                                if Collide:
                                    self.RayPong.score += 1
                                    sounds[4].play()
                                    self.fireBall.angle = calculate.reflectAngle(self.fireBall.rect.center, \
                                                                                 self.RayPong.rect.center, \
                                                                                 np.deg2rad(self.RayPong.angle), \
                                                                                 np.deg2rad(self.fireBall.angle))
                                    self.fireBall.angle = np.rad2deg(self.fireBall.angle)
                                    ignoreCollide = 20
                                    Collide = False
                                    player = 1
                                    self.fireBall.rally +=1
                                    self.aiMoveCount = 0
    
                if self.ignoreCollide > 0:
                    ignoreCollide -= 1
                
                # When AI is idle, move to angle opposite to player bat (To play efficiently)  
                if self.MULTIPLAYER:
                    if self.mode == AUTO and not self.neuralNetPickle: 
                        if player != -1:
                            # We have a count to make it look smooth and human Like
                            if self.aiMoveCount > 6:
                                if self.WolverPong.angle >= 180:
                                    self.beforePredictedBatPointAngle = self.WolverPong.angle - 180
                                elif self.WolverPong.angle < 180:
                                    self.beforePredictedBatPointAngle = self.WolverPong.angle + 180
                                    
                                self.RayPong.speed_factor = 1.0
                                self.RayPong.changeDirection = self.directionToPredict(self.RayPong.angle, \
                                                                                       self.beforePredictedBatPointAngle)
                                if self.RayPong.changeDirection == 0:
                                        self.RayPong.speed = 1
                                        self.RayPong.speed_factor = 1

                                self.RayPong.update(self.RayPong.changeDirection)
                         
                # GameOver
                if self.ballsLeft == 0:
                    sounds[0].stop()
                    if self.WolverPong.score > self.RayPong.score:
                        winner = 1
                    elif self.RayPong.score > self.WolverPong.score:
                        winner = -1
                    else:
                        winner = 0
                        
                    GameOver.gameOver(SCREEN, SCREEN_H, SCREEN_W,winner)
                    '''Once the game is over, and gameover screen is closed: need to go back to game.stopped state
                    '''
                    sounds[0].play()
                    self.resetGame()
                    self.gamestate = STOPPED
                    
                
                #log everything only as long as game is running
                if self.gamestate == RUNNING:
                    logginstring = "{},{},{},{},{},{},{},{},{}".format(self.fireBall.rect.center[0], \
                                                                        self.fireBall.rect.center[1], \
                                                                        self.fireBall.angle , \
                                                                        self.fireBall.speedx , \
                                                                        self.fireBall.speedy , \
                                                                        self.WolverPong.rect.centerx, \
                                                                        self.WolverPong.rect.centery, \
                                                                        self.WolverPong.angle, \
                                                                        self.WolverPong.speed)

            
                    log.writeLog(logginstring)
                    
            self.render_score_circles()
            self.renderScores(self.ballsLeft, self.WolverPong.score, self.RayPong.score)
          

            pygame.display.flip()
            clock.tick(100)  # milliseconds passed since last frame

def prediction(inp,hidden,output, filename="./outdata/output_20_01_06.log"):
    
    net = NN.CNeuralNet(inputneurons=inp,hiddenneurons=hidden,outputneurons=output)
    net.createTrainingData(filename, inputdim=inp, outputdim=output)
    net.train(filename,trainepochs=10)
    
    return
 
if __name__ == "__main__":
    global log
    log = Output()

#     g = Game(neuralNetPickle="./outdata/output_21_11_57_learned.pickle")
    g = Game(neuralNetPickle=None)
    g.Run()

    #prediction(inp=5, hidden=15, output=2, filename="./outdata/output_21_11_57.log")
