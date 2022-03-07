import pygame
class Wall:
    def __init__(self, x, y):
        self.res = (64,64)
        self.x = x
        self.y = y
        self.img = pygame.image.load('assets/Wall.png')
        self.isRigid = False
        self.isTrigger = False
    
    def show_wall(self,screen):
        screen.blit(self.img, (self.x, self.y))