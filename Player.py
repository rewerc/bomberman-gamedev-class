from Bullet import Bullet
from Bomb import Bomb
from pygame import mixer
import sys
import pygame
class Player:
    def __init__(self, x, y, resolution):
        self.img = pygame.image.load('assets/Player/Player_64.png')
        self.res = (64,64)
        self.x = x
        self.y = y
        self.speedX = 6
        self.speedY = 6
        self.changeX = 0
        self.changeY = 0
        self.score = 0
        self.num_of_bullet = 0
        self.num_of_bomb = 3
        self.pass1 = 0              #Stores var biar ada jeda waktu tembak
        self.bulleti = 0            #Index for bullet to be fired
        self.bombi = 0
        self.bullet = []
        self.pressed = []
        self.bomb = []
        self.effect = []
        self.isDead = False
        self.resolution = resolution
        self.type = 1
        for i in range(self.num_of_bullet):
            self.bullet.append(Bullet(self))
        for i in range(self.num_of_bomb):
            self.bomb.append(Bomb(self))
    
    #Border Player
    def Border(self):
        if self.x <= 0:
            self.x = 0
        if self.x >= self.resolution[0] - self.res[0]:
            self.x = self.resolution[0] - self.res[0]
        if self.y <= 0:
            self.y = 0
        if self.y >= self.resolution[1] - self.res[1]:
            self.y = self.resolution[1] - self.res[1]
    
    def show_player(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    #Apply Changes
    def applyChangePlayer(self):
        self.x += self.changeX
        self.y += self.changeY
    
    def show_score(self, screen):
        x, y = 10, 10
        font = pygame.font.Font('freesansbold.ttf', 32)
        score_show = font.render("Score : " + str(self.score), True, (255,255,255))
        screen.blit(score_show, (x, y))

    def add_score(self):
        self.score += 1
    
    #Bullet Movement
    def moveBullet(self):
        for i in range(self.num_of_bullet):
            if self.bullet[i].state == "fire":
                self.bullet[i].fire_bullet()
                self.bullet[i].y -= self.bullet[i].changeY
            if self.bullet[i].y < -50 and self.bullet[i].state == "fire":
                self.bullet[i].state = "ready"
                self.bullet[i].y = self.y
                self.bullet[i].x = self.x
    
    #Bomb Timer
    def bombTimer(self,game):
        for i in range(self.num_of_bomb):
            if self.bomb[i].state == "fire":
                self.bomb[i].timer += self.bomb[i].change
            if self.bomb[i].timer>1:
                self.bomb[i].explode(game, self)
                print('bomb ' +str(i)+' is ready')
    
    def check_location(self, x, y):
        for bom in self.bomb:
            if bom.x == x and bom.y == y:
                return False
        return True

    def handleEvent(self, game, event):
        if not self.isDead:
            if event.type == pygame.QUIT:
                game.running = False
                pygame.quit()
                sys.exit()
            
            #KeyDown
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
                if event.key == pygame.K_d:
                    self.changeX += self.speedX
                if event.key == pygame.K_a:
                    self.changeX -= self.speedX
                if event.key == pygame.K_s:
                    self.changeY += self.speedY
                if event.key == pygame.K_w:
                    self.changeY -= self.speedY
                if event.key == pygame.K_x:
                    if self.num_of_bomb != 0 :
                        self.bombi = self.bombi%self.num_of_bomb
                    if self.bomb[self.bombi].state == "ready":
                        newx = int((self.x+self.res[0]/2)/75)*75
                        newy = int((self.y+self.res[0]/2)/75)*75+12
                        if self.check_location(newx, newy):
                            self.bomb[self.bombi].x = newx
                            self.bomb[self.bombi].y = newy
                            self.bomb[self.bombi].drop_bomb()
                    self.bombi +=1
                
                    

            #KeyUp
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.changeX -= self.speedX
                if event.key == pygame.K_a:
                    self.changeX += self.speedX
                if event.key == pygame.K_s:                    
                    self.changeY -= self.speedY
                if event.key == pygame.K_w:
                    self.changeY += self.speedY
    