import pygame
from Box import Box

class Item:
    def __init__(self, x, y, type):
        self.res = (64,64)
        self.x = x
        self.y = y
        self.isRigid = False
        self.isTrigger = True
        self.state = "Ready"
        self.timer = 0
        self.change = 0.001
        self.type = type
        if type == "Speed":
            self.img = pygame.image.load('assets/Enemy/Enemy_64.png')
        elif type == "Strong":
            self.img = pygame.image.load('assets/Creature/Creature_4.png')
        elif type == "Long":
            self.img = pygame.image.load('assets/Creature/Creature_7.png')
        elif type == "Push":
            self.img = pygame.image.load('assets/Creature/Creature_8.png')
    
    def item_timer(self, player, game):
        if self.state == "Equipped":
            self.timer += self.change
            if self.timer > 1:
                print(player.effect)
                print(type(player))
                player.effect.remove(self)
                if self.get_effect(self.type, player) == False:
                    self.removeEffect(player)
                game.item.remove(self)
                print("Effect disabled")
                del self
            
    
    def effect(self, player, game):
        eff = self.get_effect(self.type, player)
        player.effect.append(self)
        player.add_score()
        if eff == False:
            self.applyEffect(player)
        else:
            print("Renewed")
            player.effect.remove(eff)
            game.item.remove(eff)
            del eff

    def get_effect(self, type, player):
        for eff in player.effect:
            if eff.type == type:
                return eff
        return False

    def show_item(self, game):
        if self.state == "Ready":
            game.screen.blit(self.img, (self.x, self.y))
            for player in game.player:
                game.Collider_player(self, Box(self, player), player)
    
    def applyEffect(self, player):
        if self.type == "Speed":
            if player.changeX !=0:
                player.changeX *= 3
                player.changeX /= 2
            if player.changeY !=0:
                player.changeY *= 3
                player.changeY /= 2
            player.speedX *= 3
            player.speedX /= 2
            player.speedY *= 3
            player.speedY /= 2
        
        if self.type == "Long":
            for bom in player.bomb:
                bom.level = 5

    def removeEffect(self, player):
        if self.type == "Speed":
            if player.changeX !=0:
                player.changeX /= 3
                player.changeX *= 2
            if player.changeY !=0:
                player.changeY /= 3
                player.changeY *= 2
            player.speedX /= 3
            player.speedX *= 2
            player.speedY /= 3
            player.speedY *= 2
        
        if self.type == "Long":
            for bom in player.bomb:
                bom.level = 3