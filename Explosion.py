import pygame
from math import *

class Explosion:
    def __init__(self, x, y, bomb):
        self.playerres = (64,64)
        self.img = pygame.image.load('assets/Creature/Creature_9.png')
        self.res = (64,64)
        self.x = x
        self.y = y
        self.change = 0.02
        self.timer = 0
        self.isRigid = False
        self.isTrigger = False
        self.bomb = bomb
    
    def isCollision(self, enemy, bullet):
        distance = sqrt((enemy.x - bullet.x)**2 + (enemy.y - bullet.y)**2)
        if distance < 27:
            return True
        else:
            return False

    def check_player(self, player):
        if player.type != self.bomb.owner.type:
            distance = sqrt((player.x - self.x)**2 + (player.y - self.y)**2)
            if distance < 50:
                print("He Dead")
                player.isDead = True
                del player

    def show_explosion(self, game):
        self.timer += self.change
        if self.timer < 1:
            game.screen.blit(self.img, (self.x, self.y))
        else:
            game.explosion.remove(self)
            del self
