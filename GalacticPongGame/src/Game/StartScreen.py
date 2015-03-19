import pygame
import random
from Game import IntroScene, GameSession
from constants import *
from abc import abstractmethod, ABCMeta


# Set Screen Width and Screen Height
screen = pygame.display.set_mode(RESOLUTION, 0,  32)


class TextSprites(pygame.sprite.Sprite):
    """ Abstract class of all other text sprite classes below """
    __metaclass__ = ABCMeta
    
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(TextSprites,self).__init__()

        # Instance variables that control the edges of where we bounce
        self.left_boundary = 0
        self.top_boundary = 0
        self.right_boundary = SCREEN_W
        self.bottom_boundary = SCREEN_W
 
        # Instance variables for our current speed and direction
        self.change_x = 5
        self.change_y = 5

    @abstractmethod
    def update(self, *args):
        pass

        
    def setAlpha(self, ColorTone):
        self.image.set_alpha(ColorTone)


    @abstractmethod
    def fadeIN(self, screen):
        pass


class GalacticText(TextSprites):
    def __init__(self):
        """ Constructor. Pass in the color of the block, 
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super(GalacticText,self).__init__() 
  
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('./data/Galactic.png').convert()
        # Get the rectangle enclosing this image
        self.rect = self.image.get_rect()
 

    def update(self):
        """ Called each frame. """    
        if(self.rect.y > SCREEN_H/3 -150):
            #self.rect.x -= self.change_x
            self.rect.y -= self.change_y


    def fadeIN(self, screen):
        screen.blit( self.image, ( SCREEN_W/3+10, SCREEN_H/3 ) )

        

class PongText(TextSprites):
    def __init__(self):
        """ Constructor. Pass in the color of the block, 
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super(PongText,self).__init__() 
  
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('./data/Pong.png').convert()
        # Get the rectangle enclosing this image
        self.rect = self.image.get_rect()
 

    def update(self):
        """ Called each frame. """
    
        if(self.rect.y > SCREEN_H/3-50):
            #self.rect.x -= self.change_x
            self.rect.y -= self.change_y


    def fadeIN(self, screen):
        screen.blit( self.image, ( SCREEN_W/3+220, SCREEN_H/3+100 ) )
            
            
    
class Planet(TextSprites):
    def __init__(self):
        """ Constructor. Pass in the color of the block, 
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super(Planet,self).__init__() 
  
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('./data/Planet.jpg').convert()
        # Get the rectangle enclosing this image
        self.rect = self.image.get_rect()
 
 
    def update(self):
        """ Called each frame. """
    
        if(self.rect.y > SCREEN_H/3-150):
            #self.rect.x -= self.change_x
            self.rect.y -= self.change_y

            
    def fadeIN(self, screen):
        screen.blit( self.image, ( SCREEN_W/3-220, SCREEN_H/3 ) )

        
class MenuOption:
 
    hovered = False
    i = 0
    
    def __init__(self, text, pos, screen):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw(screen)
        
            
    def draw(self, screen):
        self.set_rend()
        screen.blit(self.rend, self.rect)

        
    def set_rend(self):
        menu_font = pygame.font.SysFont('Bizarre-Ass Font Sans Serif', 60)
        self.rend = menu_font.render(self.text, True, self.get_color())

        
    def get_color(self):
        if self.hovered:
            return (255, 165, 0)
        else:
            return (self.increase_color(), self.increase_color(), self.increase_color())

        
    def increase_color(self):
        if(self.i < 100):
            self.i += 5
        
        return self.i
            
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

        
def main():
    
    # Sound Initialization
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    
    # Initialize all modules
    pygame.init()
    pygame.display.set_caption('Galactic Pong Introduction')
    
    # create background
    global screen
    background = pygame.Surface(screen.get_size()).convert()
    
    #  Playback song
    sounds = []
    sounds.append(pygame.mixer.Sound('./data/IntroTheme.ogg'))
    sounds.append(pygame.mixer.Sound('./data/MainTheme.wav'))
    sounds[0].set_volume(0.3)
    sounds[1].set_volume(0.3)
    
    warSounds = []
    import glob
    war_sounds = glob.glob("./data/WarSound*.wav")
    for war_sound in war_sounds:
        warSounds.append(pygame.mixer.Sound(war_sound))
        
    ''' GALACTIC TEXT SPRITE'''
    # This represents a block
    GalacticTextSprite = GalacticText()
      
    # Set a random location for the block
    GalacticTextSprite.rect.x = SCREEN_W/3+10
    GalacticTextSprite.rect.y = SCREEN_H/3 
    
    ''' PONG TEXT SPRITE '''
    # This represents a block
    PongTextSprite = PongText()
      
    # Set a random location for the block
    PongTextSprite.rect.x = SCREEN_W/3+220
    PongTextSprite.rect.y = SCREEN_H/3+100
    
    ''' FIRE PLANET SPRITE '''
    
    # This represents a block
    PlanetTextSprite = Planet()
      
    # Set a random location for the block
    PlanetTextSprite.rect.x = SCREEN_W/3-220
    PlanetTextSprite.rect.y = SCREEN_H/3
    
    ''' add all sprites '''

    # This is a list of every sprite. All blocks and the player block as well.
    all_sprites_list = pygame.sprite.Group(PlanetTextSprite, GalacticTextSprite, PongTextSprite)
    
    # create background
    ImageBackground = pygame.Surface((720,220)).convert()
    
    # Generate N Star Positions    
    stars = [
    [random.randint(0, SCREEN_W),random.randint(0, SCREEN_H)]
    for _ in range(numStars)
    ]
    
    # Create Menu Options
    options = [MenuOption("NEW GAME", (SCREEN_W/3+50, SCREEN_H/2), screen), \
               MenuOption("CONTROLS", (SCREEN_W/3+50, SCREEN_H/2+100), screen)]
    
    Total_Stars_shown = 1

    #Color Tone increase in image
    ColorTone = 1
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
#    StartFrame = False
    StartFrame = IntroScene.introScene(SCREEN_W,SCREEN_H,screen,sounds,warSounds,background)
    
    # to detect mouse clicks
    handled = False
    fullscreen = False

    while(StartFrame):
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_ESCAPE]:
                    if fullscreen:
                        screen = pygame.display.set_mode(RESOLUTION, 0, 32)
                    fullscreen = not fullscreen

                if keys[pygame.K_f] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN, 32)
                    else:
                        screen = pygame.display.set_mode(RESOLUTION, 0, 32)
                
        
        background.fill((0,0,0))
        
        # Draw Stars by decreasing the position coordinate each time (stars moving effect)   
        for star in range(0,Total_Stars_shown):
            pygame.draw.line(background,(255, 255, 255), stars[star], stars[star])
            stars[star][0] -= 1
            if stars[star][0] < 0:
                stars[star][0] = SCREEN_W
                stars[star][1] = random.randint(0, SCREEN_H)
        
        # Draw Stars one by one (for stars increasing effect)
        if(Total_Stars_shown < numStars):        
            Total_Stars_shown += 1
        else:
            Total_Stars_shown = numStars
            
        screen.blit(background, (0,0))
        
        # Start Title FadeIn Effect when Total stars > N/3 
        # *** INCREASE 'ColorTone' value to speed up the fading ***
        
        if(Total_Stars_shown > numStars/3):
            # Image fadeIN effect
            if(ColorTone<=255):
                GalacticTextSprite.setAlpha(ColorTone)
                PongTextSprite.setAlpha(ColorTone)
                PlanetTextSprite.setAlpha(ColorTone)
                ColorTone += 5
            PlanetTextSprite.fadeIN(screen)
            GalacticTextSprite.fadeIN(screen)
            PongTextSprite.fadeIN(screen)
        
        # Start moving the Title upwards when all stars are shown and ColorTone of Title is 255
        if(ColorTone >= 255 and Total_Stars_shown > numStars/1.3):
            ImageBackground.fill((0,0,0))
            screen.blit(background, (208,242))
            all_sprites_list.clear(screen, background)
            all_sprites_list.update()
            all_sprites_list.draw(screen)


        if(GalacticTextSprite.rect.y <= SCREEN_H/3-150):
            for option in options:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    option.hovered = True
                else:
                    option.hovered = False

                if pygame.mouse.get_pressed()[0] and option.rect.collidepoint(pygame.mouse.get_pos()) \
                    and option.text == "NEW GAME" and not handled:
                    #Fades out the current sound and smoothly enters into the game
                    pygame.mixer.fadeout(2000)
                    StartFrame = False
                    GameSession.game(screen)
                    handled = pygame.mouse.get_pressed()[0]
                    
                if(StartFrame):    
                    option.draw(screen)
                                                                            
        pygame.display.flip()
        
if __name__ == "__main__":

    main()
    
    