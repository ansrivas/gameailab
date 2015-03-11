import pygame
class CBackground():
    def __init__(self,(x,y),size,width,color):

        self.size = size
        self.width = width
        self.color = color
        self.myimage = pygame.image.load("./data/bg4.png")
        self.imagerect = self.myimage.get_rect()
        self.imagerect.x,self.imagerect.y = (360,640)
        self.x,self.y = self.imagerect.center
         
        self.x, self.y = (x,y)
    def update(self,screen):
        #screen.blit(self.myimage, self.imagerect)
        #use it to produce game-over effects for few seconds
        #self.color = self.colorobj.randomcolor()
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.size, self.width)
