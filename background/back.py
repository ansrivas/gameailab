import pygame
class CBackground():
    def __init__(self,(x,y),size,width,color):

        self.size = size
        self.width = width
        self.color = color
        self.myimage = pygame.image.load("./data/back.png")
        self.imagerect = self.myimage.get_rect()
        self.imagerect.x,self.imagerect.y = (x,y)
        self.x,self.y = self.imagerect.center
        self.imagerect.center = (x,y)
        self.x, self.y = (x,y)
    def update(self,screen):
        screen.blit(self.myimage, self.imagerect)
        #use it to produce game-over effects for few seconds
        #self.color = self.colorobj.randomcolor()
        #pygame.draw.circle(screen, self.color, (self.x,self.y), self.size, self.width)
