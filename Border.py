import pygame

class Border:
    def __init__(self, x, y, isBottom, isRight):
        self.x = x
        self.y = y
        self.img = pygame.image.load('assets/Creature/Creature_2.png')
        self.sizeX = 64
        self.sizeY = 64
        self.res = (64,64)
        self.isBottom = isBottom
        self.isRight = isRight
    
    #DONT TRY TO UNDERSTAND THIS BASED ON THE VARIABLES
    #IM TOO LAZY TO CHANGE THEM VARS

    def bottom(self, player):
        isArea = abs(player.y - self.y)< 65
        isNear = abs(player.y - self.y)< player.speedY + 2
        isTop = player.x < self.x + self.sizeX - (player.speedY + 2)
        isBottom = player.x + player.res[0]> self.x + (player.speedY + 2)
        if isArea and isTop and isBottom:
            if player.changeY < 0 and player.y > self.y + (player.speedY + 2):
                player.y = self.y + 64
            
        if isNear and isTop and isBottom and player.changeY > 0 and player.y < self.y + self.sizeY - (player.speedY + 2):
            player.y = self.y + 1
    
    def show_border(self, game):
        game.screen.blit(self.img, (self.x, self.y))

    def right(self, player):
        isArea = abs(player.x - self.x)< 65
        isNear = abs(player.x - self.x)< player.speedX + 2
        isTop = player.y < self.y + self.sizeY - 1
        isBottom = player.y + player.res[1]> self.y + 1
        if isArea and isTop and isBottom:
            if player.changeX < 0 and player.x > self.x + 1:
                player.x = self.x + 64
            
        if isNear and isTop and isBottom and player.changeX > 0 and player.x < self.x + self.sizeX - 1:
            player.x = self.x + 1