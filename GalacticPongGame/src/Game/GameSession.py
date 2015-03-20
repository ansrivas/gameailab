import pygame
import time
import math, random
from numpy import deg2rad, rad2deg
from constants import *
from Reflection import reflectcollide as refcol
from Game import GameOver
from logger.CLogger import Output

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


class Pong(pygame.sprite.Sprite):
    """ Sprite Class for Pong bats - WolverPong, RayPong """

    def __init__(self, batImagePath, initialTheta, pongDimension=(50, 120), speed=2):
        super(Pong, self).__init__()
      
        self.color = RED
        #self.width = width
        self.x = self.y = 0
        self.angle = 1
        self.theta = initialTheta 
        self.speed = speed
        self.batdimx, self.batdimy = pongDimension
        self.image = pygame.image.load(batImagePath)
        self.score = 0
        self.changeDirection = 0

        if debug:
            self.originalrect = pygame.draw.rect(self.image, self.color, (self.x, self.y, self.batdimx, \
                                                                          self.batdimy), 1)

        self.rot = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rot.get_rect()
        self.rect.center = (266, 266)
        
    def findPointOnCircle(self, deg):
        """ Returns the x,y coordinates of the corresponding angle (given in degrees) """

        rad = deg2rad(deg)
        x = (SCREEN_W/2) + 320 * math.cos(rad)
        y = (SCREEN_H/2) - 320 * math.sin(rad)

        return int(x),int(y)
    
    def update(self, changeDirection):
        if changeDirection == 1:
            self.theta += self.speed
        elif changeDirection == -1:
            if self.theta >= 0:
                self.theta -= self.speed
            else:
                self.theta = 360 - self.speed
            
        if self.theta >= 360:
            self.theta = 0
        
        self.angle  = float(self.theta) #- float(self.batdimx/213)
        self.rot = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rot.get_rect()
        self.rect.center = self.findPointOnCircle(self.theta)
        SCREEN.blit(self.rot, self.rect)
 
    def resetbat(self, initialTheta):
        """ Reset Bat's properties like Position, Speed etc. """

        self.x = self.y = 0
        self.angle = 1
        self.theta =  initialTheta 
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
        
    def resetBall(self):
        self.x = SCREEN_W/2
        self.y = SCREEN_H/2
        self.speedx = self.speedy = 3.0
        self.angle = random.uniform(0, 2*math.pi)
        self.rally = 0

    def update(self, player, ballsLeft):
        # Change the position (x and y) according to the speed and direction
        self.x += math.cos(self.angle) * self.speedx
        self.y -= math.sin(self.angle) * self.speedy
  
        # Reset the ball position if it goes out of the circle (+ offset value)
        if math.sqrt((self.x - SCREEN_W/2)**2 + (self.y - SCREEN_H/2)**2) >= (RADIUS + self.offset):
            self.resetBall()
            player *= -1
            ballsLeft -= 1
             
        # Move the image to where our x and y are
        self.rect.center = self.x, self.y
        
        '''If the rally continued for more than 5 times, 
            start increasing the speed of the ball to make it harder
        '''
        if self.rally > 0:
            if self.rally%3 == 0:
                self.increasespeed()
            
        SCREEN.blit(self.image, self.rect)

        return player, ballsLeft

    def increasespeed(self):
        """ Increase the bat speed after a successful rally, so as to increase difficulty """
        self.speedx += 0.005
        self.speedy += 0.005

class Game():

    def __init__(self):
        """ Initialize the main game state """
        # Sound Initialization
        pygame.mixer.pre_init(44100, -16, 2, 4096)

        pygame.init()
        pygame.display.set_caption('Galactic Pong')

        self.gamestate = RUNNING
        self.MULTIPLAYER = True
        self.highScore = 100
        self.stars = [
            [random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)]
            for _ in range(numStars)
        ]
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
                star[1] = random.randint(0, SCREEN_H)

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
        self.global_param_reset()
        self.gamestate = None
        self.MULTIPLAYER = True

        self.WolverPong.resetbat(180)
        if self.MULTIPLAYER:
            self.RayPong.resetbat(0)
        self.fireBall.resetBall()

    def render_pause_screen(self):
        renderPause = self.headingFont.render("Game Paused: press Space Bar to resume", True, (205,205,205))
        SCREEN.blit(renderPause,(380.,100.))

    def render_stop_screen(self):
        renderStop = self.headingFont.render("Game Stopped: press Space Bar to restart", True, (205,205,205))
        SCREEN.blit(renderStop,(380.,100.))

    def global_param_reset(self):
        """ Reset all parameters which are being used in main game loop """

        self.ballsLeft = TOTAL_BALLS
        self.Collide = False
        self.ignoreCollide = 0
        self.WolverPong.score = 0
        self.WolverPong.changeDirection = 0

        if self.MULTIPLAYER:
            self.RayPong.score = 0
            self.RayPong.changeDirection = 0

    def Run(self):
#        assert 0, self.WolverPong.changeDirection
        #class which calculates the collision and reflection
        calculate = refcol.CReflectCollid()
    
        # Play Background Music
        sounds[0].set_volume(MED_VOL)
        sounds[0].play()
    
        #Player turns
        player = 1
        running = True
        clock = pygame.time.Clock()
        SCREEN.blit(self.background,(0,0))
        st = "Game starts in : "
#        self.delayGame(WolverScore=0, RayScore=0, ballsLeft=0,st=st)
    
        while running:
            #clock.tick(100)
    #        time_passed = clock.tick(300)
    #        time_sec = time_passed / 1000.0
    
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
    
                        elif keys[pygame.K_d]:
                            self.WolverPong.changeDirection = -1
    
                        if self.MULTIPLAYER:
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
                                self.resetGame()
                                player = 1
                                st = "Game restarts in: "
                                self.delayGame(self.WolverPong.score, self.RayPong.score, self.ballsLeft, st)
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
    
                        if keys[pygame.K_q] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                            if self.gamestate == RUNNING or self.gamestate == PAUSED:
                                scores = self.WolverPong.score, self.RayPong.score
                                ballsLeft = self.ballsLeft
                                self.resetGame()
                                self.WolverPong.score, self.RayPong.score = scores
                                self.ballsLeft = ballsLeft
                                self.gamestate = STOPPED

                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            self.WolverPong.changeDirection = 0
    
                        elif event.key == pygame.K_d:
                            self.WolverPong.changeDirection = 0
    
                        if self.MULTIPLAYER:
                            if event.key == pygame.K_LEFT:
                                self.RayPong.changeDirection = 0
    
                            elif event.key == pygame.K_RIGHT:
                                self.RayPong.changeDirection = 0
    
    
    
            self.blitstars()
            if self.gamestate == STOPPED:
                self.render_stop_screen()
    
            if self.gamestate == PAUSED:
                self.render_pause_screen()
    
            if self.gamestate == RUNNING:
                self.WolverPong.update(self.WolverPong.changeDirection)
                if self.MULTIPLAYER:
                    self.RayPong.update(self.RayPong.changeDirection)
    
                # Change turn if player loses the ball
                player, self.ballsLeft = self.fireBall.update(player, self.ballsLeft)
    
                if self.ballsLeft > 0:
                    #If collided, dont check for collision for next few iterations
                    if self.ignoreCollide == 0:
                        # WolverPong's Turn
                        if player == 1:
                            # Draw Background Circle
                            SCREEN.blit(self.OuterBigOrange,(0,0))
                            SCREEN.blit(self.InnerBigOrange,(0,0))
    
                            # Check Collision
                            Collide = calculate.checkCollide(self.fireBall.rect.center, \
                                                             self.WolverPong.rect.center, \
                                                             deg2rad(self.WolverPong.angle),120,self.fireBall.angle)
    
                            if Collide:
                                # Increase Score by 1
                                self.WolverPong.score += 1
                                #sounds[1].play()
                                sounds[4].play()
                                self.fireBall.angle = calculate.reflectAngle(self.fireBall.rect.center, \
                                                                             self.WolverPong.rect.center, \
                                                                             deg2rad(self.WolverPong.angle), \
                                                                             self.fireBall.angle)
                                ignoreCollide = 20
                                Collide = False
                                player = -1
                                self.fireBall.rally +=1
    
                        # RayPong's Turn
                        if self.MULTIPLAYER:
                            if player == -1:
                                # Draw Background Circle
                                SCREEN.blit(self.OuterBigWhite,(0,0))
                                SCREEN.blit(self.InnerBigWhite,(0,0))
    
                                # Check Collision
                                Collide = calculate.checkCollide(self.fireBall.rect.center, \
                                                                 self.RayPong.rect.center, \
                                                                 deg2rad(self.RayPong.angle),120,self.fireBall.angle)
    
    
                                if Collide:
                                    # Increase Score by 1
                                    self.RayPong.score += 1
                                    #sounds[2].play()
                                    sounds[4].play()
                                    self.fireBall.angle = calculate.reflectAngle(self.fireBall.rect.center, \
                                                                                 self.RayPong.rect.center, \
                                                                                 deg2rad(self.RayPong.angle), \
                                                                                 self.fireBall.angle)
                                    ignoreCollide = 20
                                    Collide = False
                                    player = 1
                                    self.fireBall.rally +=1
    
    
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
                    sounds[0].play()
                    self.global_param_reset()
    
            self.render_score_circles()
            self.renderScores(self.ballsLeft, self.WolverPong.score, self.RayPong.score)

    
            pygame.display.flip()
            clock.tick(100)



if __name__ == "__main__":
    g = Game()
    g.Run()
