import pygame
import random


# Set Screen Width and Screen Height 
SCREEN_W, SCREEN_H = (1280, 720)
screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))

# Stars
N = 250

# Sound Initialization
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)

#  Playback song
sounds = []
sounds.append(pygame.mixer.Sound('./data/GameOver.wav'))

class Color():
    white=(255,255,255)
    black=(0,0,0)
    blue = (0,255,255)
    red = (255,0,0)
    snow = (205,201,201)
    palegreen= (152,251,152)

    def __init__(self):
        pass

class GameOverText(pygame.sprite.Sprite):
    def __init__(self):
        """ Constructor. Pass in the color of the block, 
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super(GameOverText,self).__init__() 
  
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('./data/GameOver.png').convert()
        
        
  
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
 
 
        # Instance variables for our current speed and direction
        self.change_x = 0
        self.change_y = 0
        
        # Instance variables that control the edges of where we bounce
        self.left_boundary = 0
        self.right_boundary = 0
        self.top_boundary = 0
        self.bottom_boundary = 0
        
        # Set ColorTone for the image
        self.colorTone = 1
        
 
 
    def update(self):
       
        if(self.rect.y > SCREEN_H/3-150):
            #self.rect.x -= self.change_x
            self.rect.y -= self.change_y
            
    def setAlpha(self,screen):
        
        self.image.set_alpha(self.colorTone)
        if(self.colorTone < 255):
            self.colorTone += .1
            
        
    def fadeIN(self,screen):
        screen.blit( self.image, ( SCREEN_W/3+10, SCREEN_H/3 ) )
        

        
class Stars():
    def __init__(self,screen, SCREEN_H,SCREEN_W,N):
        self.stars = None
        self.stars = [
        [random.randint(0, SCREEN_W),random.randint(0, SCREEN_H)]
        for x in range(N)
        ]      
        
    def renderStars(self,background):
        # Generate N Star Positions    
            
        background.fill(Color.black)     
        # Draw Stars (stars moving effect) 
        for star in self.stars:
            pygame.draw.line(background,(255, 255, 255), (star[0], star[1]), (star[0], star[1]))
            star[0] = star[0] - 1
            if star[0] < 0:
                star[0] = SCREEN_W
                star[1] = random.randint(0, SCREEN_H)
        
        screen.blit(background,(0,0)) 
 
 
        
class Winner():
    def __init__(self,winner):

        self.winner = winner
        
        if(self.winner == 1):
            self.winnerImage = pygame.image.load('./data/SuperHeroOne.png').convert()
            self.winnerTextImage = pygame.image.load('./data/WolverPong.png').convert()
            self.titleImage = pygame.image.load('./data/EmperorOfUniverse.png').convert()
        elif(self.winner == -1):
            self.winnerImage = pygame.image.load('./data/SuperHeroTwo.png').convert()
            self.winnerTextImage = pygame.image.load('./data/RayPong.png').convert()
            self.titleImage = pygame.image.load('./data/EmperorOfUniverse.png').convert()
        else:
            self.winnerImage = pygame.image.load('./data/DrawImage.png').convert()
            self.winnerTextImage = pygame.image.load('./data/Draw.png').convert()
            self.titleImage = pygame.image.load('./data/WarContinues.png').convert()
        
        #set ColorTones 
        self.winnerColorTone =1
        self.winnerTitleColorTone =1
        self.winnerImage.set_alpha(1)
        self.winnerTextImage.set_alpha(1)
        self.titleImage.set_alpha(1)
        
    def setAlpha(self,screen):
        
        self.winnerImage.set_alpha(self.winnerColorTone)
        self.winnerTextImage.set_alpha(self.winnerColorTone)
        if(self.winnerColorTone < 255):
            self.winnerColorTone += .5
            
        if(self.winnerColorTone > 127):
            self.titleImage.set_alpha(self.winnerTitleColorTone)
            if(self.winnerTitleColorTone < 255):
                self.winnerTitleColorTone += .5
            
        
    def fadeIN(self,screen):
        screen.blit( self.winnerImage, ( SCREEN_W/3, SCREEN_H/3 ) )
        screen.blit( self.winnerTextImage, ( SCREEN_W/2, SCREEN_H/3 ) )        
        screen.blit( self.titleImage, ( SCREEN_W/2 - 30, SCREEN_H/2-50 ) )
            



class MenuOption:
 
    hovered = False
    i = 0
    
    def __init__(self, text, pos,screen):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw(screen)
        
            
    def draw(self,screen):
        
        self.set_rend()
        screen.blit(self.rend, self.rect)
        
    def set_rend(self):
        menu_font = pygame.font.SysFont('Papyrus', 30)
        self.rend = menu_font.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered:
            return (255, 165, 0)
        else:
            return (self.increase_color(), self.increase_color(), self.increase_color())
        
    def increase_color(self):
        
        if(self.i < 100):
            
            self.i += 1
        
        return self.i
            
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
        
        
        
def gameOver(screen,SCREEN_H,SCREEN_W,playerWinner):
    
    
    running = True
    clock = pygame.time.Clock()
    
    pygame.init()
    sounds[0].play()
    
    ''' GAMEOVER TEXT SPRITE'''
    # This represents a block
    GameOverTextSprite = GameOverText()
      
    # Set a random location for the block
    GameOverTextSprite.rect.x = SCREEN_W/3+10
    GameOverTextSprite.rect.y = SCREEN_H/3 
    
    # Set movement speed
    GameOverTextSprite.change_x = 1
    GameOverTextSprite.change_y = 0.5
    
    # Set image boundaries
    GameOverTextSprite.left_boundary = 0
    GameOverTextSprite.top_boundary = 0
    GameOverTextSprite.right_boundary = SCREEN_W
    GameOverTextSprite.bottom_boundary = SCREEN_H
    
    # This is a list of every sprite. All blocks and the player block as well.
    sprites = pygame.sprite.Group()
    sprites.add(GameOverTextSprite)
    
    # create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    
        
    
    ''' STARS CREATION'''
    createStars = Stars(screen,SCREEN_H,SCREEN_W,N)
    
    '''Winner Image Render'''
    winner = Winner(playerWinner)
    
    '''Play Again Option '''
    # Create Options
    options = [MenuOption("BATTLE AGAIN", (SCREEN_W/1.4, SCREEN_H/1.2),screen)]
    # to detect mouse clicks
    handled = False
    
    
    
    while running:
        clock.tick(100) 
                                       
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
        background.fill((0,0,0))
        createStars.renderStars(background)
                    
        # GameOver Image fadeIN effect
        
        GameOverTextSprite.setAlpha(screen)
        GameOverTextSprite.fadeIN(screen)
        
        # Move image upwards
        if(GameOverTextSprite.colorTone >= 100):            
            screen.blit(background, (SCREEN_W/3+10,SCREEN_H/3))            
            sprites.update()                  
            sprites.draw(screen) 
            
            # Select Option           
            for option in options:
                               
                if option.rect.collidepoint(pygame.mouse.get_pos()):                    
                    option.hovered = True
                else:
                    option.hovered = False
                    
                # Click Option    
                if pygame.mouse.get_pressed()[0] and option.rect.collidepoint(pygame.mouse.get_pos()) and option.text == "BATTLE AGAIN" and not handled:                    
                    sounds[0].stop()                    
                    running = False                    
                    return True                
                    handled = pygame.mouse.get_pressed()[0]
                    
                if(running):                        
                    option.draw(screen)
        
        # Winner Image and Title Fade IN Effect
        if(GameOverTextSprite.rect.y <= SCREEN_H/3-150):
            winner.setAlpha(screen)
            winner.fadeIN(screen)
                    
        pygame.display.flip()

if __name__ == "__main__":
    gameOver(screen,SCREEN_H,SCREEN_W,0)