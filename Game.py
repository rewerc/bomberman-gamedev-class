import pygame
import random
from math import *
from pygame import mixer
from Box import Box
from Player import Player
from Enemy import Enemy
from Wall import Wall
from Bomb import Bomb
from Loot import Loot
from Opponent import Opponent
from Grave import Grave

class Game:
    def __init__(self):
        pygame.init()                   #Initialize the pygame
        self.num_of_enemy = 0
        self.num_of_loot = 30
        self.enemy = []
        self.walls = []
        self.explosion = []
        self.loot = []
        self.item = []
        self.border = []
        self.graves = []
        self.resolution = (975,687)
        self.screen = pygame.display.set_mode(self.resolution)#Creating Screen    
        self.running = False
        self.clock = pygame.time.Clock()
        self.current_time = pygame.time.get_ticks()
        self.timer = 60000 + pygame.time.get_ticks()
        self.font = pygame.font.SysFont(None, 50)
        self.spawnPoint1 = (370, 480)
        self.spawnPoint2 = (500, 600)
        self.run()

    # Game Over Text
    def game_over_text(self):
        font2 = pygame.font.Font('freesansbold.ttf', 80)
        gameover = font2.render("GAME OVER", True, (0,0,0))
        self.screen.blit(gameover, (250, 300))

    def setup(self):
        self.running = True
        self.player = [Player(self.spawnPoint1[0], self.spawnPoint1[1], self.resolution), Opponent(self.spawnPoint2[0], self.spawnPoint2[1], self.resolution)]
        pygame.display.set_caption("Something")     #Title and Icon
        self.icon = pygame.image.load("assets/Icon.png")
        pygame.display.set_icon(self.icon)
        # self.bgImg = pygame.image.load('Background3.jpg')   #Background Image
        # mixer.music.load("BG.mp3")      #Background Sound
        # mixer.music.play(-1)
    
    def build(self):
        #player2 = Player(400, 500)
        for i in range(self.num_of_enemy):
            self.enemy.append(Enemy())
        for i in range(1,8,2):
            for j in range(1,12,2):
        # for i in range(1,8,3):
            # for j in range(1,12,3):
                self.walls.append(Wall(j*75,i*75+12))
        # self.border.append(Border(225, 162, True, True))
        self.spawnLoot(self.num_of_loot)
    
    def isCollision(self, enemy, bullet):
        distance = sqrt((enemy.x - bullet.x)**2 + (enemy.y - bullet.y)**2)
        if distance < 27:
            return True
        else:
            return False
    
    #Collision
    def checkCollision(self, player):
        global score
        for i in range(self.num_of_enemy):
            for j in range(player.num_of_bullet):
                collision = self.isCollision(self.enemy[i], player.bullet[j])
                if player.bullet[j].state == "fire" and collision:
                    oof_sound = mixer.Sound("assets/audio/Oof.wav")
                    oof_sound.play()
                    player.bullet[j].y = player.y
                    player.bullet[j].x = player.x
                    player.bullet[j].state = "ready"
                    player.score += 10
                    self.enemy[i].x = random.randint(0, self.resolution[0] - self.enemy[i].res[0])
                    self.enemy[i].y = random.randint(50, 150)

    def isRender(self, player, box):
        if abs(player.x - box.x) < 150 and abs(player.y - box.y) < 150:
            return True
        return False

    #Solid Collider
    def Collider_player(self, wall, box, player):
        if self.isRender(player, box):
            isArea = player.y > box.y + 1 and player.y < box.y - 1 + box.sizeY and player.x > box.x +1 and player.x < box.x + box.sizeX -1
            isNear = player.y > box.y + player.speedY + 1 and player.y < box.y - player.speedY -1 + box.sizeY and player.x > box.x + player.speedX + 1 and player.x < box.x + box.sizeX - player.speedX - 1
            isStuck = sqrt((player.x - box.x - box.sizeX)**2 + (player.y - box.y - box.sizeY)**2) < 120
            #This is to stop player
            if wall.isRigid and type(wall) == Bomb and isStuck and isNear:
                player.x -= player.changeX
                player.y -= player.changeY
                return True

            isRightSide = abs(player.x - box.x - box.sizeX) < abs(player.x - box.x)
            isBottomSide = abs(player.y - box.y - box.sizeY) < abs(player.y - box.y)

            if wall.isRigid and isArea:
                #This is to Teleport player
                if player.changeY == 0:
                    if player.changeX < 0 or isRightSide:
                        player.x = box.x + box.sizeX
                    else:
                        player.x = box.x
                elif player.changeX == 0:
                    if player.changeY < 0 or isBottomSide:
                        player.y =box.y + box.sizeY
                    else:
                        player.y = box.y
                elif player.changeX != 0 and player.changeY != 0:
                    #If player di samping
                    if player.y < box.y + box.sizeY-player.speedY - 1 and player.y > box.y + player.speedY + 1:
                        #BorderX
                        if player.x >= box.x + box.sizeX/2:
                            player.x = box.x + box.sizeX
                        elif player.x < box.x + box.sizeX/2:
                            player.x = box.x

                    elif player.x < box.x + box.sizeX-player.speedX-1 and player.x > box.x + player.speedX + 1:
                        #BorderY
                        if player.y >= box.y + box.sizeY/2:
                            player.y = box.y + box.sizeY
                        elif player.y < box.y + box.sizeY/2:
                            player.y = box.y
            
            if wall.isTrigger and isArea:
                if wall.state == "Ready":
                    wall.state = "Equipped"
                    wall.effect(player, self)

            elif type(wall) == Wall and not(isArea):
                wall.isRigid = True

            elif type(wall) == Bomb and not(isArea) and self.hasBomb(player, wall.x, wall.y):
                wall.isRigid = True

            if isArea and wall.isRigid and type(wall) == Bomb and wall.get_effect("Push", player) != False:
                isWall = False
                isLoot = False
                isBomb = False
                newx = wall.x
                newy = wall.y

                for i in range(0,3):
                    if player.changeY == 0:
                        if player.changeX < 0:
                            newx -= 75
                        else:
                            newx += 75
                    elif player.changeX == 0:
                        if player.changeY < 0:
                            newy -= 75
                        else:
                            newy += 75
                    isWall = self.isWall(newx, newy)
                    isLoot = self.isLoot(newx, newy)
                    isBomb = self.isBomb(newx, newy)

                    if newx < 0:
                        newx = 0
                    if newy < 12:
                        newy = 12
                    if newx < self.resolution[0] and newy < self.resolution[1] and not isWall and isLoot == False and isBomb == False:
                        wall.x, wall.y = newx, newy
                    else:
                        break
        
    def show_screen(self):
        # self.screen.blit(self.bgImg, (0,0))
        self.screen.fill((50,50,50))
        for player in self.player:
            for bombs in player.bomb:
                bombs.show_bomb(self)
        for loots in self.loot:
            loots.show_loot(self)
        for player in self.player:
            if player.isDead:
                self.graves.append(Grave(player.x, player.y))
                if player.type == 1:
                    player.x = self.spawnPoint1[0]
                    player.y = self.spawnPoint1[1]
                if player.type == 2:
                    player.x = self.spawnPoint2[0]
                    player.y = self.spawnPoint2[1]
                player.isDead = False
        for grave in self.graves:
            grave.show_grave(self)
        for wall in self.walls:
            wall.show_wall(self.screen)
        # for bullet in self.player.bullet:
            # bullet.show_bullet(self.screen)
        for enem in self.enemy:
            enem.show_enemy(self.screen)
        for player in self.player:
            if not player.isDead:
                player.show_player(self.screen)
        for item in self.item:
            item.show_item(self)
        for ex in self.explosion:
            ex.show_explosion(self)
        for borders in self.border:
            borders.show_border(self)
        for player in self.player:
            player.show_score(self.screen)
        if len(self.player) == 1:
            if self.player[0].type == 1:
                self.draw_text("APPLE DEAD", self.font, (255,255,255), self.screen, 400, 500)
            else:
                self.draw_text("BANANA FAILURE", self.font, (255,255,255), self.screen, 500, 500)

    
    def update(self):
        for player in self.player:
            player.applyChangePlayer()
            player.Border()
            player.moveBullet()
            player.bombTimer(self)

        for wall in self.walls:
            for player in self.player:
                self.Collider_player(wall, Box(wall, player), player)
        for enem in self.enemy:
            if enem.BorderEnemy(self) == False:
                break
            enem.applyChangeEnemy()
        for player in self.player:
            for effect in player.effect:
                effect.item_timer(player, self)
        for borders in self.border:
            for player in self.player:
                if borders.isBottom:
                    borders.bottom(player)
                if borders.isRight:
                    borders.right(player)
                self.checkCollision(player)
        self.set_timer()
    
    def set_timer(self):
        self.current_time = pygame.time.get_ticks()
        if self.timer - self.current_time > 0:
            second = (int((self.timer - self.current_time)/1000)+1)%60
            minute = int((int((self.timer - self.current_time)/1000)+1)/60)
            time = f"{minute:02d}" + ":" + f"{second:02d}"
            self.draw_text(time, self.font, (255,255,255), self.screen, self.resolution[0] / 2, 50)
        else:
            if not self.player[0].isDead and not self.player[1].isDead:
                if self.player[0].score > self.player[1].score:
                    self.draw_text("BANANA WINS", self.font, (255,255,255), self.screen, 300, 400)
                elif self.player[0].score < self.player[1].score:
                    self.draw_text("APPLE WINS", self.font, (255,255,255), self.screen, 500, 400)
                else:
                    self.draw_text("DRAW!", self.font, (255,255,255), self.screen, self.resolution[0] / 2, 400)
            # self.running = False

    def isWall(self, x, y):
        for wall in self.walls:
            if wall.x == x and wall.y == y:
                return True
        return False
    
    def isBomb(self, x, y):
        for player in self.player:
            for bom in player.bomb:
                if bom.state == "fire" and bom.x == x and bom.y == y:
                    return bom
        return False
    
    def hasBomb(self, player, x, y):
        for bom in player.bomb:
            if bom.state == "fire" and bom.x == x and bom.y == y:
                return True
        return False
    
    def isLoot(self, x, y):
        for loots in self.loot:
            if loots.x == x and loots.y == y:
                return loots
        return False
    
    def isItem(self, x, y):
        for items in self.item:
            if items.state == "Ready" and items.x == x and items.y == y:
                self.item.remove(items)
                del items
                break
        return False
    
    def isBorder(self, x, y):
        for borders in self.border:
            if borders.x == x and borders.y == y:
                return borders
        return False
    
    def breakLoot(self):
        num = int(len(self.loot)/2)
        while len(self.loot) > num:
            for loot in self.loot:
                if random.randint(0,1) == 1:
                    loot.broken(self)
                if len(self.loot) <= num:
                    break
    
    def spawnLoot(self, quantity):
        num = len(self.loot)
        while(len(self.loot)<quantity + num):
            i, j = random.randint(0,8), random.randint(0,12)
            newx = j*75
            newy = i*75+12
            if self.nearPlayer(newx, newy):
                if not (self.isWall(newx,newy) or self.isLoot(newx, newy)):
                    self.loot.append(Loot(newx, newy))
    
    def nearPlayer(self, newx, newy):
        for player in self.player:
            if sqrt((newx - player.x)**2 + (newy - player.y)**2) < 150: 
                return False
        return True
    
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x,y)
        surface.blit(textobj, textrect)

    
    def run(self):
        self.setup()
        self.build()
        while self.running:
            self.show_screen()

            #Game receive input
            for player in self.player:
                player.handleEvent(self)

            #Game process input
            self.update()

            #Update frame
            pygame.display.update()
            self.clock.tick(60)













