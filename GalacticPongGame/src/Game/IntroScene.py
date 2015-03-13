import time
from random import randint
import pygame
from pygame.locals import *

from Game import FadeIN
from Game import FadeOUT



 

def introScene(SCREEN_W,SCREEN_H,screen,sounds,warSounds,background):
    
   
    
    # Images for Introduction Scene
    images = []
    
    
    # FRAME 1
    OneUniverseImage = pygame.image.load('./data/OneUniverse.png').convert()
    CommaImage = pygame.image.load('./data/Comma.png').convert()
    OneEmperorImage = pygame.image.load('./data/OneEmperor.png').convert()
    
    images.append(OneUniverseImage)
    images.append(CommaImage)
    images.append(OneEmperorImage)
    
    
    # FRAME 2
    OnceUponTimeImage = pygame.image.load('./data/OnceUponTime.png').convert()
    OnceUponTimeTextImage = pygame.image.load('./data/OnceUponTimeText.png').convert()
    ThereLivedImage = pygame.image.load('./data/ThereLived.png').convert()
    
    
    images.append(OnceUponTimeTextImage)
    images.append(OnceUponTimeImage)
    images.append(ThereLivedImage)
    
    
    # FRAME 3
    SuperHeroOneImage = pygame.image.load('./data/SuperHeroOne.png').convert()
    SuperHeroTwoImage = pygame.image.load('./data/SuperHeroTwo.png').convert()
    WolverPongImage = pygame.image.load('./data/WolverPong.png').convert()
    RayPongImage = pygame.image.load('./data/RayPong.png').convert()
    RulerWesternHemisphereImage = pygame.image.load('./data/RulerWesternHemisphere.png').convert()
    RulerEasternHemisphereImage = pygame.image.load('./data/RulerEasternHemisphere.png').convert()
    RivalTextImage = pygame.image.load('./data/RivalText.png').convert()
    
    images.append(SuperHeroOneImage)
    images.append(SuperHeroTwoImage)
    images.append(WolverPongImage)
    images.append(RayPongImage)
    images.append(RulerWesternHemisphereImage)
    images.append(RulerEasternHemisphereImage)
    images.append(RivalTextImage)
    
    
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
    
    images.append(SpaceWar1Image)
    images.append(SpaceWar2Image)
    images.append(SpaceWar3Image)
    images.append(SpaceWar4Image)
    images.append(SpaceWar5Image)
    images.append(SpaceWar6Image)
    images.append(SoldiersFallenImage)
    images.append(AndNowImage)
    images.append(FinalTextImage)
    
    
    
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
    
    
    
   
    
    # Loops for IntoScene
    FirstFrame = True
    SecondFrame = True
    ThirdFrame = True
    FourthFrame = True
    
    
    
    while FirstFrame:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                FirstFrame = False
                SecondFrame = False
                ThirdFrame = False
                FourthFrame = False
                sounds[0].stop()
                for sound in warSounds:
                    sound.stop()
                sounds[1].play()
                return True
                
                
        # Set Background Color    
        background.fill((0,0,0))
        screen.blit(background, (0,0))
        
        # ONE UNIVERSE Call FadeIN Function
        OneUniverseImage,OneUniverseImageColorTone = FadeIN.fadeIN(OneUniverseImage,OneUniverseImageColorTone,images)
        screen.blit (OneUniverseImage, (SCREEN_W/2 - OneUniverseSize[2]/1, SCREEN_H/2 - OneUniverseSize[3]/2))
        
        if(OneUniverseImageColorTone >= 255):
            OneUniverseImageColorTone = 255
            
            # Comma Call FadeIN Function
            CommaImage,CommaImageColorTone = FadeIN.fadeIN(CommaImage,CommaImageColorTone,images)
            screen.blit (CommaImage, (SCREEN_W/2, SCREEN_H/2 - CommaSize[3]/3))
            
            # ONE EMPEROR Call FadeIN Function
            OneEmperorImage,OneEmperorImageColorTone = FadeIN.fadeIN(OneEmperorImage,OneEmperorImageColorTone,images)
            screen.blit (OneEmperorImage, (SCREEN_W/2 + 15, SCREEN_H/2 - OneEmperorSize[3]/2))
            
            if(OneEmperorImageColorTone >= 255):
                OneEmperorImageColorToneOne = 255
        
            if(CommaImageColorTone >= 255):
                CommaImageColorToneOne = 255
                FirstFrame = False
                
        pygame.display.flip()
        
    
    sounds[0].play()
    while SecondFrame:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:                
                SecondFrame = False
                ThirdFrame = False
                FourthFrame = False
                sounds[0].stop()
                for sound in warSounds:
                    sound.stop()
                sounds[1].play()
                return True
            
            
        # Set Background Color    
        background.fill((3,3,3))
        screen.blit(background, (0,0))
        
        # ONCE UPON A TIME TEXT Call FadeIN Function
        OnceUponTimeTextImage, OnceUponTimeTextImageColorTone = FadeIN.fadeIN(OnceUponTimeTextImage, OnceUponTimeTextImageColorTone,images)
        screen.blit (OnceUponTimeTextImage, (SCREEN_W/2 - OnceUponTimeTextSize[2]*2, SCREEN_H/5))
        
        if(OnceUponTimeTextImageColorTone >= 255):
            OnceUponTimeTextImageColorTone = 255
            
            # Comma Call FadeIN Function
            CommaImage,CommaImageColorTone = FadeIN.fadeIN(CommaImage,CommaImageColorTone,images)
            screen.blit (CommaImage, ((SCREEN_W/2 - OnceUponTimeTextSize[2]*2)+OnceUponTimeTextSize[2], SCREEN_H/5 + CommaSize[3]/2))
            
            if(CommaImageColorTone >= 255):
                CommaImageColorToneOne = 255
        
            # ONCE UPON A TIME Call FadeIN Function
            OnceUponTimeImage, OnceUponTimeImageColorTone = FadeIN.fadeIN(OnceUponTimeImage, OnceUponTimeImageColorTone,images)
            screen.blit (OnceUponTimeImage, (SCREEN_W/2 - OnceUponTimeSize[2]/2, SCREEN_H/2 - OnceUponTimeSize[3]/2))
            
            if(OnceUponTimeImageColorTone >= 255):
                OnceUponTimeImageColorTone = 255
                
                # THERE LIVED Call FadeIN Function
                ThereLivedImage, ThereLivedImageColorTone = FadeIN.fadeIN(ThereLivedImage, ThereLivedImageColorTone,images)
                screen.blit (ThereLivedImage,(SCREEN_W/1.25 - ThereLivedSize[2], SCREEN_H/1.25 - ThereLivedSize[3]))
                
                if(ThereLivedImageColorTone >= 255):
                    ThereLivedImageColorTone = 255
                    SecondFrame = False
                                
        pygame.display.flip()
        
    sounds[0].set_volume(0.8)
   
    while(ThirdFrame):
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                ThirdFrame = False
                FourthFrame = False
                sounds[0].stop()
                for sound in warSounds:
                    sound.stop()
                sounds[1].play()
                return True
            
        # Set Background Color    
        background.fill((0,0,0))
        screen.blit(background, (0,0))
        
        # SUPERHERO ONE Call FadeIN Function
        SuperHeroOneImage, SuperHeroOneImageColorTone = FadeIN.fadeIN(SuperHeroOneImage, SuperHeroOneImageColorTone,images)
        screen.blit (SuperHeroOneImage, (SuperHeroOneSize[0] + 20 ,SuperHeroOneSize[1] + 20))
        
        if(SuperHeroOneImageColorTone >= 255):
            SuperHeroOneImageColorTone = 255
        
        # WOLVERPONG NAME Call FadeIN Function        
        if(SuperHeroOneImageColorTone >= 127):
            WolverPongImage, WolverPongImageColorTone = FadeIN.fadeIN(WolverPongImage, WolverPongImageColorTone,images)
            screen.blit (WolverPongImage, ((SuperHeroOneSize[0] + 20)+WolverPongSize[2], (SuperHeroOneSize[1] + 20)+WolverPongSize[3]))
                         
            if(WolverPongImageColorTone >= 255):
                WolverPongImageColorTone = 255
            
            # WOLVERPONG DESIGNATION Call FadeIN Function       
            if(WolverPongImageColorTone >= 127):
                RulerWesternHemisphereImage, RulerWesternHemisphereColorTone = FadeIN.fadeIN(RulerWesternHemisphereImage, RulerWesternHemisphereColorTone,images)
                screen.blit (RulerWesternHemisphereImage, ((SuperHeroOneSize[0] + 20)+WolverPongSize[2], (SuperHeroOneSize[1] + 20)+WolverPongSize[3]*2))
                
                if(RulerWesternHemisphereColorTone >= 255):
                    RulerWesternHemisphereColorTone = 255
                    
                # SUPERHERO TWO Call FadeIN Function
                if(RulerWesternHemisphereColorTone >= 127):
                    SuperHeroTwoImage, SuperHeroTwoImageColorTone = FadeIN.fadeIN(SuperHeroTwoImage, SuperHeroTwoImageColorTone,images)
                    screen.blit (SuperHeroTwoImage, (SCREEN_W - 150, SCREEN_H - 200))
                        
                    if(SuperHeroTwoImageColorTone >= 255):
                        SuperHeroTwoImageColorTone = 255
                        
                    # RAYPONG NAME Call FadeIN Function        
                    if(SuperHeroTwoImageColorTone >= 127):
                        RayPongImage, RayPongImageColorTone = FadeIN.fadeIN(RayPongImage, RayPongImageColorTone,images)
                        screen.blit (RayPongImage, (SCREEN_W - (SuperHeroTwoSize[2] + 350), SCREEN_H -(SuperHeroTwoSize[1] + 150)))
                        
                        if(RayPongImageColorTone >= 255):
                            RayPongImageColorTone = 255
                            
                        # WOLVERPONG DESIGNATION Call FadeIN Function       
                        if(RayPongImageColorTone >= 127):
                            RulerEasternHemisphereImage, RulerEasternHemisphereColorTone = FadeIN.fadeIN(RulerEasternHemisphereImage, RulerEasternHemisphereColorTone,images)
                            screen.blit (RulerEasternHemisphereImage, (SCREEN_W - (SuperHeroTwoSize[2] + 350), SCREEN_H -(SuperHeroTwoSize[1] + 100)))
                            
                            if(RulerEasternHemisphereColorTone >= 255):
                                RulerEasternHemisphereColorTone = 255
                                
                            # RIVAL TEXT Call FadeIN Function       
                            if(RulerEasternHemisphereColorTone >= 127):
                                RivalTextImage, RivalTextColorTone = FadeIN.fadeIN(RivalTextImage, RivalTextColorTone,images)
                                screen.blit (RivalTextImage, (SCREEN_W/3, SCREEN_H/2 - 40))
                                
                                if(RivalTextColorTone >= 255):
                                    RivalTextColorTone = 255
                                    ThirdFrame = False  
                                    for sound in warSounds:
                                        sound.set_volume(0.5)
                                        sound.play()
                                                                                                                                                                                        
                                                
        pygame.display.flip()
        
    sounds[0].set_volume(0.6)
    
    while FourthFrame:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                FourthFrame = False
                sounds[0].stop()
                for sound in warSounds:
                    sound.stop()
                sounds[1].play()
                return True
            
        # Set Background Color    
        background.fill((0,0,0))
        screen.blit(background, (0,0))
        
        
        
        # SPACE WAR 1 Call FadeIN Function    
        SpaceWar1Image, SpaceWar1ImageColorTone = FadeIN.fadeIN(SpaceWar1Image, SpaceWar1ImageColorTone,images)
        
        if(SpaceWar1ImageColorToneOUT > 254):
            screen.blit (SpaceWar1Image, (100, 40))
        
        # SPACE WAR 2 Call FadeIN Function    
        if(SpaceWar1ImageColorTone >= 255):
            SpaceWar1ImageColorTone = 255
            
        if(SpaceWar1ImageColorTone >= 127):
            SpaceWar2Image, SpaceWar2ImageColorTone = FadeIN.fadeIN(SpaceWar2Image, SpaceWar2ImageColorTone,images)
            if(SpaceWar2ImageColorToneOUT > 254):
                screen.blit (SpaceWar2Image, (SCREEN_W - 700, 40))
            
            if(SpaceWar2ImageColorTone >= 255):
                warSounds[2].play()
                SpaceWar2ImageColorTone = 255
            
            # SPACE WAR 3 Call FadeIN Function        
            if(SpaceWar2ImageColorTone >= 127):
                SpaceWar3Image, SpaceWar3ImageColorTone = FadeIN.fadeIN(SpaceWar3Image, SpaceWar3ImageColorTone,images)
                if(SpaceWar3ImageColorToneOUT > 254):
                    screen.blit (SpaceWar3Image, (SCREEN_W - 400, 60))
            
                if(SpaceWar3ImageColorTone >= 255):
                    warSounds[3].play()
                    SpaceWar3ImageColorTone = 255
                
                # SPACE WAR 4 Call FadeIN Function        
                if(SpaceWar3ImageColorTone >= 127):
                    
                    SoldiersFallenImage, SoldiersFallenImageColorTone = FadeIN.fadeIN(SoldiersFallenImage, SoldiersFallenImageColorTone,images)
                    if(SoldiersFallenImageColorToneOUT > 254):
                        screen.blit (SoldiersFallenImage, (SCREEN_W/3, SCREEN_H/2 - 40))
                    
                    if(SoldiersFallenImageColorTone >= 255):
                            SoldiersFallenImageColorTone = 255
                    
                    SpaceWar4Image, SpaceWar4ImageColorTone = FadeIN.fadeIN(SpaceWar4Image, SpaceWar4ImageColorTone,images)
                    if(SpaceWar4ImageColorToneOUT > 254):
                        screen.blit (SpaceWar4Image, (SCREEN_W - 400, SCREEN_H-300))
            
                    if(SpaceWar4ImageColorTone >= 255):
                        warSounds[4].play()
                        SpaceWar4ImageColorTone = 255
                    
                    # SPACE WAR 5 Call FadeIN Function        
                    if(SpaceWar4ImageColorTone >= 127):
                        SpaceWar5Image, SpaceWar5ImageColorTone = FadeIN.fadeIN(SpaceWar5Image, SpaceWar5ImageColorTone,images)
                        if(SpaceWar5ImageColorToneOUT > 254):
                            screen.blit (SpaceWar5Image, (SCREEN_W - 800, SCREEN_H-200))
            
                        if(SpaceWar5ImageColorTone >= 255):
                            warSounds[5].play()
                            SpaceWar5ImageColorTone = 255
                        
                        # SPACE WAR 6 Call FadeIN Function        
                        if(SpaceWar5ImageColorTone >= 127):
                            SpaceWar6Image, SpaceWar6ImageColorTone = FadeIN.fadeIN(SpaceWar6Image, SpaceWar6ImageColorTone,images)
                            if(SpaceWar6ImageColorToneOUT > 254):
                                screen.blit (SpaceWar6Image, (75, SCREEN_H-400))
                
                            if(SpaceWar6ImageColorTone >= 255):
                                warSounds[8].play()
                                SpaceWar6ImageColorTone = 255
                            
                            # SOLDIERFALLEN TEXT Fade OUT Call Function    
                            if(SpaceWar6ImageColorTone >= 127):
                                SoldiersFallenImage, SoldiersFallenImageColorToneOUT = FadeOUT.fadeOUT(SoldiersFallenImage, SoldiersFallenImageColorToneOUT)
                                screen.blit (SoldiersFallenImage, (SCREEN_W/3, SCREEN_H/2 - 40))
                                                  
                                if(SoldiersFallenImageColorToneOUT <= 0):
                                    SoldiersFallenImageColorToneOUT = 0
                               
                                if(SoldiersFallenImageColorToneOUT <= 27):
                                    AndNowImage, AndNowImageColorTone = FadeIN.fadeIN(AndNowImage, AndNowImageColorTone, images)
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
                                                FinalTextImage, FinalTextImageColorTone = FadeIN.fadeIN(FinalTextImage, FinalTextImageColorTone,images)
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
                                                            for sound in warSounds:
                                                                sound.set_volume(0.2)
                                                            return True
                                                            
                                                                                                                                                                                                                                              
        
        pygame.display.flip()
        
    

    
    
            
    
    
