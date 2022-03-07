import pygame
import random

class Enemy:
    def __init__(self):
        self.img = pygame.image.load('assets/Enemy/Enemy_64.png')
        self.res = (64,64)
        self.x = random.randint(0, self.resolution[0] - self.res[0])
        self.y = random.randint(50, 150)
        self.changeX = -2
        self.changeY = 0
    
    #Border enemy + Game Over
    def BorderEnemy(self, game):
        # Game Over
        if self.y > 2000:
            self.game_over_text()
            return False

        if self.y > 500:
            for i in range(self.num_of_enemy):
                game.enemy[i].y = 6000
            self.game_over_text()
            return False

        if self.x <= 0:
            self.x = 0
            self.changeX *= -1
            self.y += 50
        if self.x >= self.resolution[0] - self.res[0]:
            self.x = self.resolution[0] - self.res[0]
            self.changeX *= -1
            self.y += 50
        if self.y <= 0:
            self.y = 0
            self.changeY *= -1
        if self.y >= self.resolution[1] - self.res[1]:
            self.y = self.resolution[1] - self.res[1]
            self.changeY *= -1
        return True
    
    def show_enemy(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def applyChangeEnemy(self):
        self.x += self.changeX
        self.y += self.changeY
