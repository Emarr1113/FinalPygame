import sys, pygame, random

WIDTH = 1014
HEIGHT = 502

speed = (0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load("gameBackground.png")

vec = pygame.math.Vector2
black = (0,0,0)


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("mapFloor.png")
        self.image = pygame.transform.scale(self.image,(width,height))
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("filler.png")
        self.rect = self.image.get_rect()
        self.movex = 0  # move along X
        self.movey = 0  # move along Y
        self.level = None


    def update(self):
        # Gravity
        self.calcGravity()

        self.rect.x += self.movex

        player_hit_list = pygame.sprite.spritecollide(self,self.level.platform_list,False)
        for player in player_hit_list:
            if self.movex >0:
                self.rect.right = player.rect.left
            elif self.movex < 0:
                self.rect.left = player.rect.left
        self.rect.y += self.movey
        player_hit_list = pygame.sprite.spritecollide(self,self.level.platform_list,False)
        for player in player_hit_list:
            if self.movey >0:
                self.rect.bottom = player.rect.top
            elif self.movey < 0:
                self.rect.top = player.rect.bottom
            self.movey = 0

    def calcGravity(self):
        if self.movey == 0:
            self.movey = 1
        else:
            self.movey += 0.35
        if self.rect.y >= HEIGHT - self.rect.height and self.movey >= 0:
            self.movey = 0
            self.rect.y = HEIGHT - self.rect.height
    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self,self.level.platform_list, False)
        self.rect.y -=2
    def go_Left(self):
        self.movex = -6
    def go_Right(self):
        self.movex = 6
    def go_Up(self):
        self.movey = -6
    def go_Down(self):
        self.movey = 6
    def stop(self):
        self.movex = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([4, 10])
        self.image.fill(black)

        self.rect = self.image.get_rect()

        def update(self):

            """ Move the bullet. """
        self.rect.y -= 3
        self.rect.y = 3


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy_fill.png')
        self.imgae = pygame.transform.scale(self.image,(100,100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.move_ip(random.randint(0, screen.get_width()),
                          random.randint(0, screen.get_height()))
        self.movex = 0
        self.movey = 0

    def update(self):
        """Move Enemy"""

class Level(object):
    def __init__(self,player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        self.background = None

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()
    def draw(self,screen):
        screen.fill((255,255,255))
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

class LevelOne(Level):
    def __init__(self):
        Level.__init__(self,player)
        level = [[210,70,500,500], [210,70,200,400],[210,70,600,300]]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rext.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

pygame.init()

player = Player()

levels = []
levels.append(LevelOne(player))
current_level = 0
current_level = levels[current_level]
active_sprites = pygame.sprite.Group()
player.level = current_level
player.rect.x = 340
player.rect.y = HEIGHT - player.rect.height
active_sprites.add(player)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_Left()
            if event.type == pygame.K_RIGHT:
                player.go_Right()
            if event.type == pygame.K_UP:
                player.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.movex < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.movex > 0:
                player.stop()
    active_sprites.update()
    current_level.update()

    active_sprites.draw()
    current_level.draw()

    pygame.display.flip()
"""commit"""