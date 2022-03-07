import pygame
from pygame import mixer

class Bullet:
    def __init__(self, player):
        self.img = pygame.image.load('assets/bullet.png')
        self.res = (16,40)
        self.x = 0
        self.y = player.y
        self.state = "ready"
        self.changeY = 4
        self.player = player
    
    def fireAgain(self):
        if self.player.pass1 >= 20:
            bullet_sound = mixer.Sound("assets/audio/Shot.wav")
            bullet_sound.set_volume(0.2)
            bullet_sound.play()
            if self.state == "ready":
                self.x = self.player.x
                self.y = self.player.y
                self.fire_bullet()
            self.player.bulleti += 1
            self.player.pass1 = 0
        else:
            self.player.pass1 += 1
    
    def fire_bullet(self):
        self.state = "fire"
    
    def show_bullet(self, screen):
        if self.state == "fire":
            screen.blit(self.img, (self.x + 8, self.y + 20))