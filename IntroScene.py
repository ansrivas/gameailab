'''
Created on Mar 6, 2015

@author: Sridev
'''

import os,sys,random
import pygame
from pygame.locals import *
from Crypto.Random.random import randint
from Game import FadeIN
from Game import FadeOUT
import time
 
# Set Screen Width and Screen Height 
SCREEN_W, SCREEN_H = (1280, 720)

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
    # basic start
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W,SCREEN_H), pygame.FULLSCREEN)
    pygame.display.set_caption('Galactic Pong Introduction')
    
    # create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    
    # Images for Introduction Scene
    
    # FRAME 1
    OneUniverseImage = pygame.image.load('./data/OneUniverse.png').convert()
    CommaImage = pygame.image.load('./data/Comma.png').convert()
    OneEmperorImage = pygame.image.load('./data/OneEmperor.png').convert()
    
    # FRAME 2
    OnceUponTimeImage = pygame.image.load('./data/OnceUponTime.png').convert()
    OnceUponTimeTextImage = pygame.image.load('./data/OnceUponTimeText.png').convert()
    ThereLivedImage = pygame.image.load('./data/ThereLived.png').convert()
    
    # FRAME 3
    SuperHeroOneImage = pygame.image.load('./data/SuperHeroOne.png').convert()
    SuperHeroTwoImage = pygame.image.load('./data/SuperHeroTwo.png').convert()
    WolverPongImage = pygame.image.load('./data/WolverPong.png').convert()
    RayPongImage = pygame.image.load('./data/RayPong.png').convert()
    RulerWesternHemisphereImage = pygame.image.load('./data/RulerWesternHemisphere.png').convert()
    RulerEasternHemisphereImage = pygame.image.load('./data/RulerEasternHemisphere.png').convert()
    RivalTextImage = pygame.image.load('./data/RivalText.png').convert()
    
    # FRAME 4
    SpaceWar1Image = pygame.image.load('./data/SpaceWar1.jpg').convert()
    SpaceWar2Image = pygame.image.load('./data/SpaceWar2.jpg').convert()
    SpaceWar3Image = pygame.image.load('./data/SpaceWar3.jpg').convert()
    SpaceWar4Image = pygame.image.load('./data/SpaceWar4.jpg').convert()
    SpaceWar5Image = pygame.image.load('./data/SpaceWar5.jpg').convert()
    SpaceWar6Image = pygame.image.load('./data/SpaceWar6.jpg').convert()
    SoldiersFallenImage = pygame.image.load('./data/SoldiersFallen.png').convert()
    AndNowImage = pygame.image.load('./data/AndNow.png').convert()
    FinalTextImage =  pygame.image.load('./data/FinalText.png').convert()
    
    # Get Image Positions
    
    # FRAME 1
    OneUniverseSize = OneUniverseImage.get_rect()
    CommaSize = CommaImage.get_rect()
    OneEmperorSize = OneEmperorImage.get_rect()
    
    
    # FRAME 2
    OnceUponTimeSize = OnceUponTimeImage.get_rect()
    OnceUponTimeTextSize = OnceUponTimeTextImage.get_rect()
    ThereLivedSize = ThereLivedImage.get_rect()
    
    # FRAME 3
    SuperHeroOneSize = SuperHeroOneImage.get_rect()
    SuperHeroTwoSize = SuperHeroTwoImage.get_rect()
    WolverPongSize = WolverPongImage.get_rect()
    RayPongSize = RayPongImage.get_rect()
    RulerWesternHemisphereSize = RulerWesternHemisphereImage.get_rect()
    RulerEasternHemisphereSize = RulerEasternHemisphereImage.get_rect()
    
    
    
    # Color Tones for all Images
    
    # FRAME 1    
    OneUniverseImageColorTone =1 
    CommaImageColorTone =1 
    OneEmperorImageColorTone =1
    
    # FRAME 2
    OnceUponTimeImageColorTone = 1
    OnceUponTimeTextImageColorTone = 1
    ThereLivedImageColorTone = 1
    
    # FRAME 3
    SuperHeroOneImageColorTone = 1
    SuperHeroTwoImageColorTone = 1
    WolverPongImageColorTone = 1
    RayPongImageColorTone = 1
    RulerWesternHemisphereColorTone = 1
    RulerEasternHemisphereColorTone = 1
    RivalTextColorTone = 1
    
    # FRAME 4
    SpaceWar1ImageColorTone = 1
    SpaceWar1ImageColorToneOUT = 255
    SpaceWar2ImageColorTone = 1
    SpaceWar2ImageColorToneOUT = 255
    SpaceWar3ImageColorTone = 1
    SpaceWar3ImageColorToneOUT = 255
    SpaceWar4ImageColorTone = 1
    SpaceWar4ImageColorToneOUT = 255
    SpaceWar5ImageColorTone = 1
    SpaceWar5ImageColorToneOUT = 255
    SpaceWar6ImageColorTone = 1
    SpaceWar6ImageColorToneOUT = 255
    SoldiersFallenImageColorTone = 1
    SoldiersFallenImageColorToneOUT = 255
    AndNowImageColorTone = 1
    AndNowImageColorToneOUT = 255
    FinalTextImageColorTone = 1
    FinalTextImageColorToneOUT = 255
    
    
     
    
    
    # main loop
    clock = pygame.time.Clock()
    
    time.sleep(5)
    
   
    
    # Loops for IntoScene
    FirstFrame = True
    SecondFrame = True
    ThirdFrame = True
    FourthFrame = True
    FifthFrame = True
    
    
    while FirstFrame:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                FirstFrame = False
                SecondFrame = False
                ThirdFrame = False
                FourthFrame = False
                
                
        # Set Background Color    
        background.fill((0,0,0))
        screen.blit(background, (0,0))
        
        # ONE UNIVERSE Call FadeIN Function
        OneUniverseImage,OneUniverseImageColorTone = FadeIN.fadeIN(OneUniverseImage,OneUniverseImageColorTone)
        screen.blit (OneUniverseImage, (SCREEN_W/2 - OneUniverseSize[2]/1, SCREEN_H/2 - OneUniverseSize[3]/2))
        
        if(OneUniverseImageColorTone >= 255):
            OneUniverseImageColorTone = 255
            
            # Comma Call FadeIN Function
            CommaImage,CommaImageColorTone = FadeIN.fadeIN(CommaImage,CommaImageColorTone)
            screen.blit (CommaImage, (SCREEN_W/2, SCREEN_H/2 - CommaSize[3]/3))
            
            # ONE EMPEROR Call FadeIN Function
            OneEmperorImage,OneEmperorImageColorTone = FadeIN.fadeIN(OneEmperorImage,OneEmperorImageColorTone)
            screen.blit (OneEmperorImage, (SCREEN_W/2 + 15, SCREEN_H/2 - OneEmperorSize[3]/2))
            
            if(OneEmperorImageColorTone >= 255):
                OneEmperorImageColorToneOne = 255
        
            if(CommaImageColorTone >= 255):
                CommaImageColorToneOne = 255
                FirstFrame = False
                
        pygame.display.flip()
        
    
    
    while SecondFrame:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:                
                SecondFrame = False
                ThirdFrame = False
                FourthFrame = False
        # Set Background Color    
        background.fill((3,3,3))
        screen.blit(background, (0,0))
        
        # ONCE UPON A TIME TEXT Call FadeIN Function
        OnceUponTimeTextImage, OnceUponTimeTextImageColorTone = FadeIN.fadeIN(OnceUponTimeTextImage, OnceUponTimeTextImageColorTone)
        screen.blit (OnceUponTimeTextImage, (SCREEN_W/2 - OnceUponTimeTextSize[2]*2, SCREEN_H/5))
        
        if(OnceUponTimeTextImageColorTone >= 255):
            OnceUponTimeTextImageColorTone = 255
            
            # Comma Call FadeIN Function
            CommaImage,CommaImageColorTone = FadeIN.fadeIN(CommaImage,CommaImageColorTone)
            screen.blit (CommaImage, ((SCREEN_W/2 - OnceUponTimeTextSize[2]*2)+OnceUponTimeTextSize[2], SCREEN_H/5 + CommaSize[3]/2))
            
            if(CommaImageColorTone >= 255):
                CommaImageColorToneOne = 255
        
            # ONCE UPON A TIME Call FadeIN Function
            OnceUponTimeImage, OnceUponTimeImageColorTone = FadeIN.fadeIN(OnceUponTimeImage, OnceUponTimeImageColorTone)
            screen.blit (OnceUponTimeImage, (SCREEN_W/2 - OnceUponTimeSize[2]/2, SCREEN_H/2 - OnceUponTimeSize[3]/2))
            
            if(OnceUponTimeImageColorTone >= 255):
                OnceUponTimeImageColorTone = 255
                
                # THERE LIVED Call FadeIN Function
                ThereLivedImage, ThereLivedImageColorTone = FadeIN.fadeIN(ThereLivedImage, ThereLivedImageColorTone)
                screen.blit (ThereLivedImage,(SCREEN_W/1.25 - ThereLivedSize[2], SCREEN_H/1.25 - ThereLivedSize[3]))
                
                if(ThereLivedImageColorTone >= 255):
                    ThereLivedImageColorTone = 255
                    SecondFrame = False
                                
        pygame.display.flip()
        
    
   
    while(ThirdFrame):
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                ThirdFrame = False
                FourthFrame = False
            
        # Set Background Color    
        background.fill((0,0,0))
        screen.blit(background, (0,0))
        
        # SUPERHERO ONE Call FadeIN Function
        SuperHeroOneImage, SuperHeroOneImageColorTone = FadeIN.fadeIN(SuperHeroOneImage, SuperHeroOneImageColorTone)
        screen.blit (SuperHeroOneImage, (SuperHeroOneSize[0] + 20 ,SuperHeroOneSize[1] + 20))
        
        if(SuperHeroOneImageColorTone >= 255):
            SuperHeroOneImageColorTone = 255
        
        # WOLVERPONG NAME Call FadeIN Function        
        if(SuperHeroOneImageColorTone >= 127):
            WolverPongImage, WolverPongImageColorTone = FadeIN.fadeIN(WolverPongImage, WolverPongImageColorTone)
            screen.blit (WolverPongImage, ((SuperHeroOneSize[0] + 20)+WolverPongSize[2], (SuperHeroOneSize[1] + 20)+WolverPongSize[3]))
                         
            if(WolverPongImageColorTone >= 255):
                WolverPongImageColorTone = 255
            
            # WOLVERPONG DESIGNATION Call FadeIN Function       
            if(WolverPongImageColorTone >= 127):
                RulerWesternHemisphereImage, RulerWesternHemisphereColorTone = FadeIN.fadeIN(RulerWesternHemisphereImage, RulerWesternHemisphereColorTone)
                screen.blit (RulerWesternHemisphereImage, ((SuperHeroOneSize[0] + 20)+WolverPongSize[2], (SuperHeroOneSize[1] + 20)+WolverPongSize[3]*2))
                
                if(RulerWesternHemisphereColorTone >= 255):
                    RulerWesternHemisphereColorTone = 255
                    
                # SUPERHERO TWO Call FadeIN Function
                if(RulerWesternHemisphereColorTone >= 127):
                    SuperHeroTwoImage, SuperHeroTwoImageColorTone = FadeIN.fadeIN(SuperHeroTwoImage, SuperHeroTwoImageColorTone)
                    screen.blit (SuperHeroTwoImage, (SCREEN_W - 150, SCREEN_H - 200))
                        
                    if(SuperHeroTwoImageColorTone >= 255):
                        SuperHeroTwoImageColorTone = 255
                        
                    # RAYPONG NAME Call FadeIN Function        
                    if(SuperHeroTwoImageColorTone >= 127):
                        RayPongImage, RayPongImageColorTone = FadeIN.fadeIN(RayPongImage, RayPongImageColorTone)
                        screen.blit (RayPongImage, (SCREEN_W - (SuperHeroTwoSize[2] + 350), SCREEN_H -(SuperHeroTwoSize[1] + 150)))
                        
                        if(RayPongImageColorTone >= 255):
                            RayPongImageColorTone = 255
                            
                        # WOLVERPONG DESIGNATION Call FadeIN Function       
                        if(RayPongImageColorTone >= 127):
                            RulerEasternHemisphereImage, RulerEasternHemisphereColorTone = FadeIN.fadeIN(RulerEasternHemisphereImage, RulerEasternHemisphereColorTone)
                            screen.blit (RulerEasternHemisphereImage, (SCREEN_W - (SuperHeroTwoSize[2] + 350), SCREEN_H -(SuperHeroTwoSize[1] + 100)))
                            
                            if(RulerEasternHemisphereColorTone >= 255):
                                RulerEasternHemisphereColorTone = 255
                                
                            # RIVAL TEXT Call FadeIN Function       
                            if(RulerEasternHemisphereColorTone >= 127):
                                RivalTextImage, RivalTextColorTone = FadeIN.fadeIN(RivalTextImage, RivalTextColorTone)
                                screen.blit (RivalTextImage, (SCREEN_W/3, SCREEN_H/2 - 40))
                                
                                if(RivalTextColorTone >= 255):
                                    RivalTextColorTone = 255
                                    ThirdFrame = False                                                                                                                                                        
                                                
        pygame.display.flip()
        
    
    while FourthFrame:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                FourthFrame = False
            
        # Set Background Color    
        background.fill((0,0,0))
        screen.blit(background, (0,0))
        
        # SPACE WAR 1 Call FadeIN Function    
        SpaceWar1Image, SpaceWar1ImageColorTone = FadeIN.fadeIN(SpaceWar1Image, SpaceWar1ImageColorTone)
        if(SpaceWar1ImageColorToneOUT > 254):
            screen.blit (SpaceWar1Image, (100, 40))
        
        # SPACE WAR 2 Call FadeIN Function    
        if(SpaceWar1ImageColorTone >= 255):
            SpaceWar1ImageColorTone = 255
            
        if(SpaceWar1ImageColorTone >= 127):
            SpaceWar2Image, SpaceWar2ImageColorTone = FadeIN.fadeIN(SpaceWar2Image, SpaceWar2ImageColorTone)
            if(SpaceWar2ImageColorToneOUT > 254):
                screen.blit (SpaceWar2Image, (SCREEN_W - 700, 40))
            
            if(SpaceWar2ImageColorTone >= 255):
                SpaceWar2ImageColorTone = 255
            
            # SPACE WAR 3 Call FadeIN Function        
            if(SpaceWar2ImageColorTone >= 127):
                SpaceWar3Image, SpaceWar3ImageColorTone = FadeIN.fadeIN(SpaceWar3Image, SpaceWar3ImageColorTone)
                if(SpaceWar3ImageColorToneOUT > 254):
                    screen.blit (SpaceWar3Image, (SCREEN_W - 400, 60))
            
                if(SpaceWar3ImageColorTone >= 255):
                    SpaceWar3ImageColorTone = 255
                
                # SPACE WAR 4 Call FadeIN Function        
                if(SpaceWar3ImageColorTone >= 127):
                    
                    SoldiersFallenImage, SoldiersFallenImageColorTone = FadeIN.fadeIN(SoldiersFallenImage, SoldiersFallenImageColorTone)
                    if(SoldiersFallenImageColorToneOUT > 254):
                        screen.blit (SoldiersFallenImage, (SCREEN_W/3, SCREEN_H/2 - 40))
                    
                    if(SoldiersFallenImageColorTone >= 255):
                            SoldiersFallenImageColorTone = 255
                    
                    SpaceWar4Image, SpaceWar4ImageColorTone = FadeIN.fadeIN(SpaceWar4Image, SpaceWar4ImageColorTone)
                    if(SpaceWar4ImageColorToneOUT > 254):
                        screen.blit (SpaceWar4Image, (SCREEN_W - 400, SCREEN_H-300))
            
                    if(SpaceWar4ImageColorTone >= 255):
                        SpaceWar4ImageColorTone = 255
                    
                    # SPACE WAR 5 Call FadeIN Function        
                    if(SpaceWar4ImageColorTone >= 127):
                        SpaceWar5Image, SpaceWar5ImageColorTone = FadeIN.fadeIN(SpaceWar5Image, SpaceWar5ImageColorTone)
                        if(SpaceWar5ImageColorToneOUT > 254):
                            screen.blit (SpaceWar5Image, (SCREEN_W - 800, SCREEN_H-200))
            
                        if(SpaceWar5ImageColorTone >= 255):
                            SpaceWar5ImageColorTone = 255
                        
                        # SPACE WAR 6 Call FadeIN Function        
                        if(SpaceWar5ImageColorTone >= 127):
                            SpaceWar6Image, SpaceWar6ImageColorTone = FadeIN.fadeIN(SpaceWar6Image, SpaceWar6ImageColorTone)
                            if(SpaceWar6ImageColorToneOUT > 254):
                                screen.blit (SpaceWar6Image, (75, SCREEN_H-400))
                
                            if(SpaceWar6ImageColorTone >= 255):
                                SpaceWar6ImageColorTone = 255
                            
                            # SOLDIERFALLEN TEXT Fade OUT Call Function    
                            if(SpaceWar6ImageColorTone >= 127):
                                SoldiersFallenImage, SoldiersFallenImageColorToneOUT = FadeOUT.fadeOUT(SoldiersFallenImage, SoldiersFallenImageColorToneOUT)
                                screen.blit (SoldiersFallenImage, (SCREEN_W/3, SCREEN_H/2 - 40))
                                                  
                                if(SoldiersFallenImageColorToneOUT <= 0):
                                    SoldiersFallenImageColorToneOUT = 0
                               
                                if(SoldiersFallenImageColorToneOUT <= 127):
                                    AndNowImage, AndNowImageColorTone = FadeIN.fadeIN(AndNowImage, AndNowImageColorTone)
                                    if(AndNowImageColorToneOUT > 254):
                                        screen.blit (AndNowImage, (SCREEN_W/3, SCREEN_H/2 - 40))
                                    
                                    if(AndNowImageColorTone >= 255):
                                        AndNowImageColorTone = 255
                                        
                                        # All Space Images Fade OUT Call Function
                                        if(AndNowImageColorTone == 255):
                                            
                                            SpaceWar1Image, SpaceWar1ImageColorToneOUT = FadeOUT.fadeOUT(SpaceWar1Image, SpaceWar1ImageColorToneOUT)
                                            screen.blit (SpaceWar1Image, (100, 40))
                                            
                                            if(SpaceWar1ImageColorToneOUT <= 0):
                                                SpaceWar1ImageColorToneOUT = 0
                                            
                                            SpaceWar2Image, SpaceWar2ImageColorToneOUT = FadeOUT.fadeOUT(SpaceWar2Image, SpaceWar2ImageColorToneOUT)
                                            screen.blit (SpaceWar2Image, (SCREEN_W - 700, 40))
                                            
                                            if(SpaceWar2ImageColorToneOUT <= 0):
                                                SpaceWar2ImageColorToneOUT = 0
                                            
                                            SpaceWar3Image, SpaceWar3ImageColorToneOUT = FadeOUT.fadeOUT(SpaceWar3Image, SpaceWar3ImageColorToneOUT)
                                            screen.blit (SpaceWar3Image, (SCREEN_W - 400, 60))
                                            
                                            if(SpaceWar3ImageColorToneOUT <= 0):
                                                SpaceWar3ImageColorToneOUT = 0
                                            
                                            SpaceWar4Image, SpaceWar4ImageColorToneOUT = FadeOUT.fadeOUT(SpaceWar4Image, SpaceWar4ImageColorToneOUT)
                                            screen.blit (SpaceWar4Image, (SCREEN_W - 400, SCREEN_H-300))
                                            
                                            if(SpaceWar4ImageColorToneOUT <= 0):
                                                SpaceWar4ImageColorToneOUT = 0
                                            
                                            SpaceWar5Image, SpaceWar5ImageColorToneOUT = FadeOUT.fadeOUT(SpaceWar5Image, SpaceWar5ImageColorToneOUT)
                                            screen.blit (SpaceWar5Image, (SCREEN_W - 800, SCREEN_H-200))
                                            
                                            if(SpaceWar5ImageColorToneOUT <= 0):
                                                SpaceWar5ImageColorToneOUT = 0
                                            
                                            SpaceWar6Image, SpaceWar6ImageColorToneOUT = FadeOUT.fadeOUT(SpaceWar6Image, SpaceWar6ImageColorToneOUT)
                                            screen.blit (SpaceWar6Image, (75, SCREEN_H-400))
                                            
                                            if(SpaceWar6ImageColorToneOUT <= 0):
                                                SpaceWar6ImageColorToneOUT = 0
                                            
                                            AndNowImage, AndNowImageColorToneOUT = FadeOUT.fadeOUT(AndNowImage, AndNowImageColorToneOUT)
                                            screen.blit (AndNowImage, (SCREEN_W/3, SCREEN_H/2 - 40))
                                            
                                            if(AndNowImageColorToneOUT <= 0):
                                                AndNowImageColorToneOUT = 0
                                                
                                            if(SpaceWar1ImageColorToneOUT==0 and SpaceWar2ImageColorToneOUT==0 and SpaceWar3ImageColorToneOUT==0 and SpaceWar4ImageColorToneOUT==0 and SpaceWar5ImageColorToneOUT==0 and SpaceWar6ImageColorToneOUT==0 and AndNowImageColorToneOUT == 0):
                                                FinalTextImage, FinalTextImageColorTone = FadeIN.fadeIN(FinalTextImage, FinalTextImageColorTone)
                                                if(FinalTextImageColorToneOUT > 254):
                                                    screen.blit (FinalTextImage, (SCREEN_W/4, SCREEN_H/2 - 40))
                                                
                                                if(FinalTextImageColorTone >= 255):
                                                    FinalTextImageColorTone = 255
                                                    
                                                    if(FinalTextImageColorTone == 255):
                                                        time.sleep(0.10)
                                                        FinalTextImage, FinalTextImageColorToneOUT = FadeOUT.fadeOUT(FinalTextImage, FinalTextImageColorToneOUT)
                                                        screen.blit (FinalTextImage, (SCREEN_W/4, SCREEN_H/2 - 40))
                                                        
                                                        if(FinalTextImageColorToneOUT <= 0):
                                                            FinalTextImageColorToneOUT = 0
                                                            FourthFrame = False                                                                                                                                                                                                                                                    
        
        pygame.display.flip()
    
    # Number of Stars 
    N = 500  
    
   
    
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
    
    
    
    while(FifthFrame):
        
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == QUIT:
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
        if(ColorTone == 256 and Total_Stars_shown == N):
            
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
                    
                option.draw(screen)
                
                                                                            
        pygame.display.flip()
    
    
            
    
    
if __name__ == '__main__': main()