import pygame
from Box import Box
from Explosion import Explosion

class Bomb:
    def __init__(self, player):
        self.img = pygame.image.load('assets/Creature/Creature_1.png')
        self.res = (64,64)
        self.x = -500
        self.y = -500
        self.state = "ready"
        self.change = 0.005
        self.timer = 0
        self.isRigid = False
        self.level = 3
        self.isTrigger = False
        self.isBomb = True
        self.owner = player

    def drop_bomb(self):
        self.state = "fire"
        print('bomb has been planted')

    def show_bomb(self, game):
        if self.state == "fire":
            game.screen.blit(self.img, (self.x, self.y))
            for player in game.player:
                game.Collider_player(self, Box(self, player), player)
    
    def explode(self, game, player1):
        exp = Explosion(self.x, self.y, self)
        game.explosion.append(exp)
        for player in game.player:
            exp.check_player(player, game)
        self.state = "ready"
        for i in range(4):
            newx = self.x
            newy = self.y
            isBorder = False
            isBoda = game.isBorder(newx, newy)
            if isBoda != False:
                if i==0 and isBoda.isRight == True:
                    isBorder = True
                if i==2 and isBoda.isBottom == True:
                    isBorder = True
            for j in range(self.level):
                if isBorder:
                    break
                if i == 0:              #Right explosion
                    newx = self.x + 75*(j+1)
                if i == 1:              #Left explosion
                    newx = self.x - 75*(j+1)
                if i == 2:              #Bottom explosion
                    newy = self.y + 75*(j+1)
                if i == 3:              #Top explosion
                    newy = self.y - 75*(j+1)
                if game.isWall(newx, newy): #Logic to make explosion effect
                    break
                isBoda = game.isBorder(newx, newy)
                if isBoda != False:
                    if i==0 and isBoda.isRight == True:
                        isBorder = True
                    if i==1 and isBoda.isRight == True:
                        break
                    if i==2 and isBoda.isBottom == True:
                        isBorder = True
                    if i==3 and isBoda.isBottom == True:
                        break
                
                exp = Explosion(newx, newy, self)
                game.explosion.append(exp)
                for player in game.player:
                    exp.check_player(player, game)
                game.isItem(newx, newy)
                bom = game.isBomb(newx, newy)
                if bom != False:
                    bom.explode(game, player1)
                isLut = game.isLoot(newx, newy)
                if isLut != False:     #If isLOOT
                    isLut.broken(game)
                    if self.get_effect("Strong", player1) != False:
                        pass
                    else:
                        break

        self.timer = 0
        self.x = -500
        self.y = -500
        self.isRigid = False
    
    def get_effect(self, type, player):
        for eff in player.effect:
            if eff.type == type:
                return eff
        return False
