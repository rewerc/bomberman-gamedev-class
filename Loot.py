import pygame
import random
from Box import Box
from Item import Item

class Loot:
    def __init__(self, x, y):
        self.res = (64,64)
        self.x = x
        self.y = y
        self.isRigid = True
        self.isTrigger = False
        self.img = pygame.image.load('assets/Creature/Creature_5.png')
    
    def show_loot(self, game):        
        game.screen.blit(self.img, (self.x, self.y))
        for player in game.player:
            game.Collider_player(self, Box(self, player), player)
    
    def broken(self, game):
        k = random.randint(1,4)
        if k == 1:
            game.item.append(Item(self.x, self.y, "Speed"))
        elif k == 2:
            game.item.append(Item(self.x, self.y, "Strong"))
        elif k == 3:
            game.item.append(Item(self.x, self.y, "Long"))
        elif k == 4:
            game.item.append(Item(self.x, self.y, "Push"))

        game.loot.remove(self)
        del self
