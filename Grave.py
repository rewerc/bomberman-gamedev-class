import pygame

class Grave:
    def __init__(self, x, y):
        self.img = pygame.image.load('assets/Player/grave.png')
        self.x = x
        self.y = y
    
    def show_grave(self, game):
        game.screen.blit(self.img, (self.x, self.y))
