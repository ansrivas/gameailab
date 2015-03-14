import pygame
import random
from Game import IntroScene, GameSession

# Set Screen Width and Screen Height 
SCREEN_W, SCREEN_H = (1280, 720)
screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))

# Number of Stars 
N = 500  


class GalacticText(pygame.sprite.Sprite):
    def __init__(self):
        """ Constructor. Pass in the color of the block, 
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super(GalacticText,self).__init__() 
  
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('./data/Galactic.png').convert()
        
        
  
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
 
        # Instance variables that control the edges of where we bounce
        self.left_boundary = 0
        self.right_boundary = 0
        self.top_boundary = 0
        self.bottom_boundary = 0
 
        # Instance variables for our current speed and direction
        self.change_x = 0
        self.change_y = 0
         
 
 
    def update(self):
        """ Called each frame. """
    
        if(self.rect.y > SCREEN_H/3-150):
            #self.rect.x -= self.change_x
            self.rect.y -= self.change_y
            
    def setAlpha(self,screen,ColorTone):
        
        self.image.set_alpha(ColorTone)
        
    def fadeIN(self,screen):
        screen.blit( self.image, ( SCREEN_W/3+10, SCREEN_H/3 ) )
        
        
        
        
class PongText(pygame.sprite.Sprite):
    def __init__(self):
        """ Constructor. Pass in the color of the block, 
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super(PongText,self).__init__() 
  
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('./data/Pong.png').convert()
        
        
  
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
 
        # Instance variables that control the edges of where we bounce
        self.left_boundary = 0
        self.right_boundary = 0
        self.top_boundary = 0
        self.bottom_boundary = 0
 
        # Instance variables for our current speed and direction
        self.change_x = 0
        self.change_y = 0
         
 
 
    def update(self):
        """ Called each frame. """
    
        if(self.rect.y > SCREEN_H/3-50):
            #self.rect.x -= self.change_x
            self.rect.y -= self.change_y
            
    def setAlpha(self,screen,ColorTone):
        
        self.image.set_alpha(ColorTone)
        
    def fadeIN(self,screen):
        screen.blit( self.image, ( SCREEN_W/3+220, SCREEN_H/3+100 ) )
            
            
    
class Planet(pygame.sprite.Sprite):
    def __init__(self):
        """ Constructor. Pass in the color of the block, 
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super(Planet,self).__init__() 
  
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('./data/Planet.jpg').convert()
        
        
  
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
 
        # Instance variables that control the edges of where we bounce
        self.left_boundary = 0
        self.right_boundary = 0
        self.top_boundary = 0
        self.bottom_boundary = 0
 
        # Instance variables for our current speed and direction
        self.change_x = 0
        self.change_y = 0
         
 
 
    def update(self):
        """ Called each frame. """
    
        if(self.rect.y > SCREEN_H/3-150):
            #self.rect.x -= self.change_x
            self.rect.y -= self.change_y
            
    def setAlpha(self,screen,ColorTone):
        
        self.image.set_alpha(ColorTone)
        
    def fadeIN(self,screen):
        screen.blit( self.image, ( SCREEN_W/3-220, SCREEN_H/3 ) )
        
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
        menu_font = pygame.font.SysFont('Bizarre-Ass Font Sans Serif', 60)
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
        
        
def main():
    
    # Sound Initialization
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    
    # basic game start
    pygame.init()
    
   
    
    pygame.display.set_caption('Galactic Pong Introduction')
    
    # create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    
    
    #  Playback song
    sounds = []
    warSounds = []
    sounds.append(pygame.mixer.Sound('./data/IntroTheme.ogg'))
    sounds.append(pygame.mixer.Sound('./data/MainTheme.wav'))
    warSounds.append(pygame.mixer.Sound('./data/WarSound1.wav'))
    warSounds.append(pygame.mixer.Sound('./data/WarSound2.wav'))
    warSounds.append(pygame.mixer.Sound('./data/WarSound3.wav'))
    warSounds.append(pygame.mixer.Sound('./data/WarSound4.wav'))
    warSounds.append(pygame.mixer.Sound('./data/WarSound5.wav'))
    warSounds.append(pygame.mixer.Sound('./data/WarSound6.wav'))
    warSounds.append(pygame.mixer.Sound('./data/WarSound7.wav'))
    warSounds.append(pygame.mixer.Sound('./data/WarSound8.wav'))
    warSounds.append(pygame.mixer.Sound('./data/WarSound9.wav'))
    
    
    
    
    sounds[0].set_volume(0.8)
   
    
    # This is a list of every sprite. All blocks and the player block as well.
    all_sprites_list = pygame.sprite.Group()
      
    ''' GALACTIC TEXT SPRITE'''
    # This represents a block
    GalacticTextSprite = GalacticText()
      
    # Set a random location for the block
    GalacticTextSprite.rect.x = SCREEN_W/3+10
    GalacticTextSprite.rect.y = SCREEN_H/3 
    
    # Set movement speed
    GalacticTextSprite.change_x = 1
    GalacticTextSprite.change_y = 1
    
    # Set image boundaries
    GalacticTextSprite.left_boundary = 0
    GalacticTextSprite.top_boundary = 0
    GalacticTextSprite.right_boundary = SCREEN_W
    GalacticTextSprite.bottom_boundary = SCREEN_W
    
    ''' PONG TEXT SPRITE'''
    # This represents a block
    PongTextSprite = PongText()
      
    # Set a random location for the block
    PongTextSprite.rect.x = SCREEN_W/3+220
    PongTextSprite.rect.y = SCREEN_H/3+100
    
    # Set movement speed
    PongTextSprite.change_x = 1
    PongTextSprite.change_y = 1
    
    # Set image boundaries
    PongTextSprite.left_boundary = 0
    PongTextSprite.top_boundary = 0
    PongTextSprite.right_boundary = SCREEN_W
    PongTextSprite.bottom_boundary = SCREEN_W
    
    ''' FIRE PLANET SPRITE '''
    
    # This represents a block
    PlanetTextSprite = Planet()
      
    # Set a random location for the block
    PlanetTextSprite.rect.x = SCREEN_W/3-220
    PlanetTextSprite.rect.y = SCREEN_H/3
    
    # Set movement speed
    PlanetTextSprite.change_x = 1
    PlanetTextSprite.change_y = 1
    
    # Set image boundaries
    PlanetTextSprite.left_boundary = 0
    PlanetTextSprite.top_boundary = 0
    PlanetTextSprite.right_boundary = SCREEN_W
    PlanetTextSprite.bottom_boundary = SCREEN_W
    
    ''' add all sprites'''
    
    all_sprites_list.add(PlanetTextSprite)
    all_sprites_list.add(GalacticTextSprite)
    all_sprites_list.add(PongTextSprite)
    
    

    
    # create background
    ImageBackground = pygame.Surface((720,220))
    ImageBackground = ImageBackground.convert()
    
    # Generate N Star Positions    
    stars = [
    [random.randint(0, SCREEN_W),random.randint(0, SCREEN_H)]
    for x in range(N)
    ]
    
    Total_Stars_shown = 1
    
    #Color Tone increase in image
    ColorTone = 1
    
    # Create Menu Options
    options = [MenuOption("NEW GAME", (SCREEN_W/3+50, SCREEN_H/2),screen), MenuOption("CONTROLS", (SCREEN_W/3+50, SCREEN_H/2+100),screen)]
    
   
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    StartFrame = False
    StartFrame = IntroScene.introScene(SCREEN_W,SCREEN_H,screen,sounds,warSounds,background)
    
    # to detect mouse clicks
    handled = False
    
    while(StartFrame):
        
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        
        
        background.fill((0,0,0))
        
        # Draw Stars by decreasing the position coordinate each time (stars moving effect)   
        for star in range(0,Total_Stars_shown):
            
            pygame.draw.line(background,(255, 255, 255), (stars[star][0], stars[star][1]), (stars[star][0], stars[star][1]))
            stars[star][0] = stars[star][0] - 1
            if stars[star][0] < 0:
                stars[star][0] = SCREEN_W
                stars[star][1] = random.randint(0, SCREEN_H)
        
        # Draw Stars one by one (for stars increasing effect)
        if(Total_Stars_shown < N):        
            Total_Stars_shown += 1
        else:
            Total_Stars_shown = N
            
        screen.blit(background, (0,0))
        
        # Start Title FadeIn Effect when Total stars > N/3 
        if(Total_Stars_shown > N/3):
            # Image fadeIN effect
            if(ColorTone<=255):
                GalacticTextSprite.setAlpha(screen, ColorTone)
                PongTextSprite.setAlpha(screen, ColorTone)
                PlanetTextSprite.setAlpha(screen, ColorTone)
                ColorTone += 1
            PlanetTextSprite.fadeIN(screen)
            GalacticTextSprite.fadeIN(screen)
            PongTextSprite.fadeIN(screen)
        
        # Start moving the Title upwards when all stars are shown and ColorTone of Title is 255
        if(ColorTone >= 255 and Total_Stars_shown > N/1.3):
            
            ImageBackground.fill((0,0,0))
            screen.blit(background, (208,242))
                                    
            all_sprites_list.update()
                  
            # Draw all the spites
            all_sprites_list.draw(screen)
        
        
        if(GalacticTextSprite.rect.y <= SCREEN_H/3-150):
            for option in options:
                
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    
                    option.hovered = True
                else:
                    option.hovered = False
                    
                if pygame.mouse.get_pressed()[0] and option.rect.collidepoint(pygame.mouse.get_pos()) and option.text == "NEW GAME" and not handled:
                    sounds[1].stop()
                    StartFrame = False
                    GameSession.game(screen,SCREEN_H,SCREEN_W)
                    handled = pygame.mouse.get_pressed()[0]
                    
                    
                if(StartFrame):    
                    option.draw(screen)
                
                
                                                                            
        pygame.display.flip()
        
if __name__ == "__main__":
    main()
    
    