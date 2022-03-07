class Box:
    def __init__(self, wall, player):
        self.y = wall.y - player.res[1]
        self.x = wall.x - player.res[0]
        self.sizeX = wall.res[1] + player.res[1]
        self.sizeY = wall.res[0] + player.res[0]