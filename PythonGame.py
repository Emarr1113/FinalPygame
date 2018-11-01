import sys, pygame, random

WIDTH = 1014
HEIGHT = 502

speed = (0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))


vec = pygame.math.Vector2
black = (0,0,0)


class Background(pygame.sprite.Sprite):
    def __init__(self,image,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("gameBackground.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

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
        # print("rect.x = %d " % self.rect.x)
        # print("move x = %d " % self.movex)
        # player_hit_list = pygame.sprite.spritecollide(self,self.level.platform_list, False)
        # for player in player_hit_list:
        #     if self.movey > 0:
        #         self.rect.right = player.rect.left
        #     elif self.movey < 0:
        #         self.rect.left = player.rect.left
        self.rect.y += self.movey
        platform_hit_list = pygame.sprite.spritecollide(self,self.level.platform_list, False)
        for platform in platform_hit_list:
            if self.movey > 0:
                self.rect.bottom = platform.rect.top
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
        # self.rect.y += 2
    #         # self.rect.y -=2
    #         # player_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.movey= -10
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
        self.image = pygame.transform.scale(self.image,(100,100))
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

        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

class LevelOne(Level):
    def __init__(self, player):
        Level.__init__(self,player)
        level = [[195,36,422,171], [195,36,61,358], [195,36,762,358], [1014,29,0,471]]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Bullets(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)



Bg = Background("gameBackground.png", [0,0])

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
            #print("key down")
            if event.key == pygame.K_LEFT:
                player.go_Left()
                #print("key left")
            if event.key == pygame.K_RIGHT:
                #print("key right")
                player.go_Right()

            if event.key == pygame.K_SPACE:
                player.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.movex < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.movex > 0:
                player.stop()
    active_sprites.update()
    current_level.update()

    screen.blit(Bg.image, Bg.rect)

    active_sprites.draw(screen)
    current_level.draw(screen)





    pygame.display.flip()
