import pygame
import time, random
import numpy as np
from math import atan2
from constants import *
from Reflection import reflectcollide as refcol
#from LineCircleIntersection import findIntersectPoints as PointsIntersect
#from BatAnglePrediction.predictAngle import Prediction
from Game import GameOver
from logger.CLogger import Output
from Game.GameSessionAI import ignoreCollide
from __builtin__ import True

SCREEN = pygame.display.set_mode(RESOLUTION, 0, 32)

'''just using a naive global logger
'''
log = Output()
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
    x = (SCREEN_W/2) + (RADIUS * np.cos(rad))
    y = (SCREEN_H/2) - (RADIUS * np.sin(rad))

    return int(x),int(y)

def findAngle(point):
    x1, y1 = RING_CENTER
    x2, y2 = point

    angle = -np.rad2deg(atan2(y2-y1, x2-x1))
    if angle < 0:
        angle += 360

    return int(np.round(angle))



class Pong(pygame.sprite.Sprite):
    """ Sprite Class for Pong bats - WolverPong, RayPong """

    def __init__(self, batImagePath, initialAngle, pongDimension=(50, 120)):
        super(Pong, self).__init__()

#        self.x = self.y = 0
#        self.angle = 0
        self.angle = initialAngle
        self.batdimx, self.batdimy = pongDimension
        self.image = pygame.image.load(batImagePath)
        self.score = 0
        self.changeDirection = 0
#        self.speed = DEFAULT_BAT_SPEED
#        self.speed_factor = 1.0
        self.rot = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rot.get_rect()
        self.rect.center = (266, 266)

    def update(self, changeDirection, smallDiff=None):
#        self.speed += 10
        if changeDirection > 0:
                if not smallDiff:
                    self.angle += DEFAULT_INCREASE_ANGLE
                else:
                    self.angle += smallDiff
        elif changeDirection < 0:
            if not smallDiff:
                self.angle -= DEFAULT_INCREASE_ANGLE
            else:
                self.angle -= smallDiff
        
        if self.angle < 0:
            self.angle += 360

        self.rot = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rot.get_rect()
        self.rect.center = findPointOnCircle(self.angle)

        SCREEN.blit(self.rot, self.rect)

    def resetbat(self, initialAngle):
        """ Reset Bat's properties like Position, Speed etc. """

#        self.x = self.y = 0
#        self.angle = 0
        self.angle = initialAngle
#        self.speed = DEFAULT_BAT_SPEED
        self.rect.center = (266,266)


class FireBall(pygame.sprite.Sprite):
    """ Sprite Class for pong ball - FireBall"""

    def __init__(self, ballDimension=(28,29), ballImage="./data/ball.png"):
        # Call the parent class (Sprite) constructor
        super(FireBall, self).__init__()

        self.image = pygame.image.load(ballImage)
        self.rect = self.image.get_rect()
#        self.rect.centerx, self.rect.centery = (100,100)
        self.center_offset = 20
        self.rect.center = (SCREEN_W/2 + np.random.randint(10, self.center_offset), \
                            SCREEN_H/2 - np.random.randint(10, self.center_offset))
        self.x, self.y = self.rect.center
        self.lastCollisonPoint = self.rect.center
        self.target = None
        self.smallestDifference = None
        # Speed in pixels per cycle
        self.speedx = self.speedy = DEFAULT_BALL_SPEED

        # Direction of ball in degrees
        self.angle = int(np.rad2deg(np.random.uniform(0, 2*np.pi)))

        # Ball gets reset if it crosses off this value outside the ring
        self.offset = 70
        '''
        This is the case where rally has been increased to a 20, start increasing the speed
        after this to make it harder
        '''
        self.rally = 0

    def resetBall(self):
        self.x, self.y = (SCREEN_W/2 + np.random.randint(10, self.center_offset), \
                          SCREEN_H/2 - np.random.randint(10, self.center_offset))
        self.speedx = self.speedy = DEFAULT_BALL_SPEED
        self.angle = int(np.rad2deg(np.random.uniform(0, 2*np.pi)))
        self.lastCollisonPoint = self.x, self.y
        self.target = None
        self.smallestDifference = None
        self.rally = 0

    def update(self, player, ballsLeft):
        rad = np.deg2rad(self.angle)
        # Change the position (x and y) according to the speed and direction
        self.x += np.cos(rad) * self.speedx
        self.y -= np.sin(rad) * self.speedy

        # Reset the ball position if it goes out of the circle (+ offset value)
        if np.sqrt((self.x - SCREEN_W/2)**2 + (self.y - SCREEN_H/2)**2) >= (RADIUS + self.offset):
            self.resetBall()
            player *= -1
            ballsLeft -= 1

        # Move the image to where our x and y are
        self.rect.center = self.x, self.y

        '''If the rally continued for more than 5 times,
            start increasing the speed of the ball to make it harder
        '''
        if self.rally > 0:
            if self.rally%2 == 0:
                self.increasespeed()

        SCREEN.blit(self.image, self.rect)

        return player, ballsLeft

    def increasespeed(self):
        """ Increase the bat speed after a successful rally, so as to increase difficulty """
        self.speedx += 0.05
        self.speedy += 0.05


class CBombs(pygame.sprite.Sprite):
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
        if(self.playanimation == True):
            self.play_burning_animation()
        SCREEN.blit(self.image,self.rect)

    def play_burning_animation(self):
        maxlen = len(self.explosion_frame)

        bombexplosion.play()
        if(self.playanimation == True):
            if(self.frame_num >= maxlen):
                '''kill the sprites after animation is done playing'''
                self.frame_num =0
                self.playanimation = False
                self.kill()

            else:
                self.image = self.explosion_frame[self.frame_num]
                self.frame_num +=1
                SCREEN.blit(self.image,self.rect)


"""
This module is used to pull individual sprites from sprite sheets.
"""
class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
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


class Game():

    def __init__(self):
        """ Initialize the main game state """
        # Sound Initialization
        pygame.mixer.pre_init(44100, -16, 2, 4096)

        pygame.init()
        pygame.display.set_caption('Galactic Pong')

        self.mode = AUTO
        self.gamestate = RUNNING
        self.MULTIPLAYER = True
        self.highScore = 100
        self.stars = [
            [np.random.randint(0, SCREEN_W), np.random.randint(0, SCREEN_H)]
            for _ in range(numStars)
        ]

        self.openLock = False
        self.AI_turn = False

        Wolverpongimage = "./data/rWolverGamePONG.png"
        self.WolverPong = Pong(Wolverpongimage, 180)

        if self.MULTIPLAYER:
            RayPongimage = "./data/RayGamePONG.png"
            self.RayPong = Pong(RayPongimage, 0)

        """ AI Parameters """
        # To get points on the ball's trajectory
#        self.pointCount = 0

        # Self.ball contains (x1,y1, x2, y2)
        self.ball = np.zeros(4)
        # Predicted Bat points and angle
        self.ballAngle = self.batAngle = self.predictedBatAngle = 0.0
        # Self.predictedBatPoint contains (x1,y1, x2, y2)
#        self.predictedBatPoint = np.zeros(4)

        # Find the best fit among the the 2 points
#        self.predictedBatPointFinalX = self.predictedBatPointFinalY = 0.0

        self.background = pygame.Surface(SCREEN.get_size()).convert()

        self.scoreFont = pygame.font.SysFont("calibri",40)
        self.headingFont = pygame.font.SysFont("Papyrus",30)

        self.fireBall = FireBall()
        self.ballsLeft = TOTAL_BALLS
#        self.Collide = False
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

#        self.bomb_group = pygame.sprite.Group()
        self.numofBombs = 5
        self.points = None

        '''call ths just once so as to randomly initialize obstacles'''
#        self.generateNbombsinCircle(self.numofBombs)


    def resetBombLocation(self):
        '''reset all the bomb location after the game is reset '''
        np.random.shuffle(self.points)
        points = random.sample(self.points,self.numofBombs)

        self.bomb_group.empty()
        for p in points:
            bomb = CBombs(p)
            self.bomb_group.add(bomb)


    def generateNbombsinCircle(self,num=3):
        import pickle
        with open('points.txt', 'rb') as f:
            self.points = pickle.load(f)

        np.random.shuffle(self.points)
        points = random.sample(self.points, num)

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
        np.random.shuffle(listofpoints)
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
        """ Render Scores """

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
        self._global_param_reset()
        self.gamestate = None
        self.MULTIPLAYER = True

        self.WolverPong.resetbat(180)
        if self.MULTIPLAYER:
            self.RayPong.resetbat(0)
#        self.resetBombLocation()
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
#        self.Collide = False
        self.ignoreCollide = 0
        self.WolverPong.score = 0
        self.WolverPong.changeDirection = 0
#        self.pointCount = 0
        self.ball = np.zeros(4)
#        self.predictedBatPoint = np.zeros(4)
        self.ballAngle = self.batAngle = self.predictedBatAngle = 0.0
#        self.predictedBatPointFinalX = self.predictedBatPointFinalY = 0.0

        if self.MULTIPLAYER:
            self.RayPong.score = 0
            self.RayPong.changeDirection = 0

    def check_bomb_ball_collide(self):
            collide_list = pygame.sprite.spritecollide(self.fireBall,self.bomb_group,False)

            for block in collide_list:
                block.playanimation = True

    def imposePenalty(self, player):
        """ Impose penalty on the player who resets the ball.
            Done by giving an extra point to the opponent
        """

        if self.MULTIPLAYER:
            if player == 1:
                self.RayPong.score += 1
            else:
                self.WolverPong.score += 1
        else:
            if self.WolverPong.score > 0:
                self.WolverPong.score -= 1


    def Run(self):
#        assert 0, self.WolverPong.changeDirection
        #class which calculates the collision and reflection
        calculate = refcol.CReflectCollide()

        #class for Line Circle Intersection
#        intersect = PointsIntersect.FindIntersection()
        #class to Predict the correct angle
#        predict = Prediction()

        # Play Background Music
        sounds[0].set_volume(MED_VOL)
        sounds[0].play()

        #Player turns
        player = -1
        if player == -1:
            AI_turn = True

        running = True
#        clock = pygame.time.Clock()
        SCREEN.blit(self.background,(0,0))
#        st = "Game starts in : "
#        self.delayGame(WolverScore=0, RayScore=0, ballsLeft=0, st=st)
#         FPS = 100                           # desired max. framerate in frames per second.
#         playtime = 0
#         milliseconds = 0
        clock = pygame.time.Clock()
        
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
                            self.WolverPong.changeDirection = 1
                            ''' increase the speed in case of continues pressing'''
#                            self.WolverPong.speed_factor += 0.01

                        elif keys[pygame.K_d]:
                            self.WolverPong.changeDirection = -1
                            ''' increase the speed in case of continues pressing'''
#                            self.WolverPong.speed_factor += 0.01

                        if self.MULTIPLAYER:
                            if self.mode == MANUAL:
                                if keys[pygame.K_LEFT]:
                                    self.RayPong.changeDirection = 1

                                elif keys[pygame.K_RIGHT]:
                                    self.RayPong.changeDirection = -1

                        if keys[pygame.K_SPACE]:
                            if self.gamestate == RUNNING:
                                self.gamestate = PAUSED
                            elif self.gamestate == PAUSED:
                                self.gamestate = RUNNING
                                st = "Resuming in: "
                                self.delayGame(self.WolverPong.score, self.RayPong.score, self.ballsLeft, st)
                            elif self.gamestate == STOPPED:
                                st = "Game restarts in: "
                                self.delayGame(self.WolverPong.score, self.RayPong.score, self.ballsLeft, st)
                                player = 1
                                self.gamestate = RUNNING

                        if keys[pygame.K_r] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                            if self.gamestate == RUNNING or self.gamestate == PAUSED:
                                self.fireBall.resetBall()
                                self.WolverPong.resetbat(180)
                                if self.MULTIPLAYER:
                                    self.RayPong.resetbat(0)

                                st = "Resetting in: "
                                self.delayGame(self.WolverPong.score, self.RayPong.score, self.ballsLeft, st)
                                self.gamestate = RUNNING

                                self.imposePenalty(player)

                        if keys[pygame.K_q] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                            if self.gamestate == RUNNING or self.gamestate == PAUSED:
                                self.resetGame()
                                self.gamestate = STOPPED

                    elif event.type == pygame.KEYUP:
                        if event.key in (pygame.K_a, pygame.K_d):
                            self.WolverPong.changeDirection = 0
                            ''' reset the speed back once the key is left'''
#                            self.WolverPong.speed = 1.0
#                            self.WolverPong.speed_factor = 1.0

                        if self.MULTIPLAYER:
                            if self.mode == MANUAL:
                                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                                    self.RayPong.changeDirection = 0
        #                            self.RayPong.speed = 1.0
        #                            self.RayPong.speed_factor = 1.0

            self.blitstars()

            if self.gamestate == STOPPED:
                self.render_stop_screen()

            if self.gamestate == PAUSED:
                self.render_pause_screen()

            if self.gamestate == RUNNING:
#                self.bomb_group.update()
#                self.check_bomb_ball_collide()

                self.WolverPong.update(self.WolverPong.changeDirection)
                # Change turn if player loses the ball
                player, self.ballsLeft = self.fireBall.update(player, self.ballsLeft)
                if self.ballsLeft > 0:
                    # WolverPong's Turn
                    if self.ignoreCollide == 0:
                        if player == 1:
                            SCREEN.blit(self.OuterBigOrange,(0,0))
                            SCREEN.blit(self.InnerBigOrange,(0,0))

                            collide = pygame.sprite.collide_rect(self.fireBall, self.WolverPong)
                            if collide:
#                                print "collision at {}".format(self.WolverPong.rect.center)
                                sounds[4].play()
                                self.WolverPong.score += 1
                                self.fireBall.angle, self.fireBall.target = calculate.reflectAngle(self.WolverPong.rect.center, \
                                                                             self.fireBall.lastCollisonPoint)
#                                print "reflected {}' and hitting at {}".format(self.fireBall.angle, self.fireBall.target)
                                self.fireBall.lastCollisonPoint = self.WolverPong.rect.center
#                                 self.fireBall.lastCollisonPoint = (self.WolverPong.rect.center[0] + self.WolverPong.batdimx/2, \
#                                                                    self.WolverPong.rect.center[1] + self.WolverPong.batdimy/2)
                                self.fireBall.rally += 1
                                if self.MULTIPLAYER:
                                    player = -1
                                    self.openLock = True
                                ignoreCollide = 20

                            self.WolverPong.update(self.WolverPong.changeDirection)
                        
                        # RayPong's Turn
                        if self.MULTIPLAYER:
                            SCREEN.blit(self.OuterBigWhite,(0,0))
                            SCREEN.blit(self.InnerBigWhite,(0,0))

                            if (AI_turn and not self.openLock):
                                AI_turn = True
                            else:
                                AI_turn = False

                            if self.mode == AUTO:
                                if self.openLock or AI_turn:
                                    self.batAngle = self.RayPong.angle
#                                    print "raypong currently at {}".format(self.batAngle)
                                    if self.openLock:
                                        print 'open Lock'
                                        self.predictedBatAngle = findAngle(self.fireBall.target)
                                    elif AI_turn:
                                        print "AI Turn"
                                        self.predictedBatAngle = self.fireBall.angle  # findAngle(findPointOnCircle(self.fireBall.angle))
#                                    print "predicted collison point {}".format(findPointOnCircle(self.predictedBatAngle))
                                    way1 = abs(self.batAngle - self.predictedBatAngle)
                                    way2 = 360 - way1
                                    
                                    if min(way1, way2) == way1:
                                        if self.predictedBatAngle < self.batAngle:
                                            self.RayPong.changeDirection = -1
                                        else:
                                            self.RayPong.changeDirection = 1
                                    else:
                                        if self.predictedBatAngle > self.batAngle:
                                            self.RayPong.changeDirection = -1
                                        else:
                                            self.RayPong.changeDirection = 1
                                    
                                    self.fireBall.smallestDifference = min(way1, way2)
#                                    print "Smallest Difference to move : {}".format(min(way1, way2))

                                    self.openLock = False
                                    AI_turn = False


#                            print "difference IN: {}, in {}".format(self.fireBall.smallestDifference, self.RayPong.changeDirection)
                            if self.fireBall.smallestDifference >= DEFAULT_INCREASE_ANGLE:
                                self.fireBall.smallestDifference -= DEFAULT_INCREASE_ANGLE
                                self.RayPong.update(self.RayPong.changeDirection)
                            elif self.fireBall.smallestDifference <= 0:
                                self.fireBall.smallestDifference = 0
                                self.RayPong.changeDirection = 0
                                self.RayPong.update(self.RayPong.changeDirection)
                            elif 0 < self.fireBall.smallestDifference < DEFAULT_INCREASE_ANGLE:
                                self.RayPong.update(self.RayPong.changeDirection, self.fireBall.smallestDifference)
                                self.fireBall.smallestDifference = 0

#                            print "difference OUT: {}, in {}".format(self.fireBall.smallestDifference, self.RayPong.changeDirection)

                                
#                            print "raypong's angle :  {}".format(self.RayPong.angle)

                            collide = pygame.sprite.collide_rect(self.fireBall, self.RayPong)
                            if collide:
                                sounds[4].play()
                                self.RayPong.score += 1
                                
                                self.fireBall.angle, self.fireBall.target = calculate.reflectAngle(self.RayPong.rect.center, \
                                                                             self.fireBall.lastCollisonPoint)
                                self.fireBall.lastCollisonPoint = self.RayPong.rect.center
#                                 self.fireBall.lastCollisonPoint = (self.RayPong.rect.center[0] + self.RayPong.batdimx/2, \
#                                                                    self.RayPong.rect.center[1] + self.RayPong.batdimy/2)
                                player = 1
                                self.fireBall.rally += 1
                                ignoreCollide = 20

                if self.ignoreCollide > 0:
                    ignoreCollide -= 1

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
                    self.gamestate = STOPPED
                    pygame.mixer.fadeout(2000)
                    sounds[0].play()
                    self._global_param_reset()

            self.render_score_circles()
            self.renderScores(self.ballsLeft, self.WolverPong.score, self.RayPong.score)


            pygame.display.flip()
#            clock.tick(50)  # milliseconds passed since last frame

if __name__ == "__main__":
    g = Game()
    g.Run()
