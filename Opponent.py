import pygame
from Player import Player

class Opponent(Player):
    def __init__(self,x,y,resolution):
        super().__init__(x, y, resolution)
        self.resolution = (975,687)
        self.type = 2
        self.img = pygame.image.load('assets/Player/Player2-64.png')

    def show_score(self, screen):
        x, y = self.resolution[0] - 150, 10
        font = pygame.font.Font('freesansbold.ttf', 32)
        score_show = font.render("Score : " + str(self.score), True, (255,255,255))
        screen.blit(score_show, (x, y))
    
    def handleEvent(self, game, event):
        if not self.isDead:
            if event.type == pygame.QUIT:
                game.running = False
            
            #KeyDown
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
                if event.key == pygame.K_RIGHT:
                    self.changeX += self.speedX
                if event.key == pygame.K_LEFT:
                    self.changeX -= self.speedX
                if event.key == pygame.K_DOWN:
                    self.changeY += self.speedY
                if event.key == pygame.K_UP:
                    self.changeY -= self.speedY
                if event.key == pygame.K_m:
                    if self.num_of_bomb != 0 :
                        self.bombi = self.bombi % self.num_of_bomb
                    if self.bomb[self.bombi].state == "ready":
                        newx = int((self.x+self.res[0]/2)/75)*75
                        newy = int((self.y+self.res[0]/2)/75)*75+12
                        if self.check_location(newx, newy):
                            self.bomb[self.bombi].x = newx
                            self.bomb[self.bombi].y = newy
                            self.bomb[self.bombi].drop_bomb()

            #KeyUp
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.changeX -= self.speedX
                if event.key == pygame.K_LEFT:
                    self.changeX += self.speedX
                if event.key == pygame.K_DOWN:                    
                    self.changeY -= self.speedY
                if event.key == pygame.K_UP:
                    self.changeY += self.speedY