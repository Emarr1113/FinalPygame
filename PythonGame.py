import sys, pygame, random, math

WIDTH = 1014
HEIGHT = 502

speed = (0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))


vec = pygame.math.Vector2
black = (0,0,0)


class Background(pygame.sprite.Sprite):
    def __init__(self,image,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("map.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("platform.png")
        self.image = pygame.transform.scale(self.image,(width,height))
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.movex = 0  # move along X
        self.movey = 0  # move along Y
        self.level = None
        self.direction = 1

    def getPosition(self):
        return (self.rect.left + 76, self.rect.top + 35)

    def updateDirection(self, direction):
        self.direction = direction

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
        self.movey= -8
    def go_Left(self):
        self.direction = -1
        self.movex = -6
    def go_Right(self):
        self.direction = 1
        self.movex = 6
    def go_Up(self):
        self.movey = -6
    def go_Down(self):
        self.movey = 6
    def stop(self):
        self.movex = 0

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.image = pygame.image.load('enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,8)
        self.speed = 0

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top >HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def move_towards_player(self, Player):
        dx, dy = self.rect.x - Player.rect.x, self.rect.y - Player.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed


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
        level = [[195,36,422,171], [195,36,72,358], [195,36,752,358],]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Bullets(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.direction = direction
        #self.vel = dir * self.bullet_speed()
        #self.spawn_time = pygame.time.get_ticks()

    # def bullet_speed(self):
    #     self.speed = 500
    # def bullet_lifetime(self):
    #     self.bulletsLife = 1000
    # def bullet_rate(self):
    #     self.last_shot > self.bullet_rate
    #     self.bullet_rate = 150
    def update(self):
        self.rect.x += (10 * self.direction)
        # if self.rect.bottom > 30:
        #     self.kill()

    # def delete_bullet(self):
    #     if Bullets() <= HEIGHT


Bg = Background("map.png", [0,0])

pygame.init()

player = Player()
m = Mob()
bullet = Bullets()

levels = []
levels.append(LevelOne(player))
current_level = 0
current_level = levels[current_level]
active_sprites = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
bullet_list.add(bullet)
player.level = current_level
player.rect.x = 360
player.rect.y = HEIGHT - player.rect.height
active_sprites.add(player)
mobs = pygame.sprite.Group()
for i in range(8):
    m = Mob()
    active_sprites.add(m)
    mobs.add(m)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_Left()
            if event.key == pygame.K_RIGHT:
                player.go_Right()
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_s:
                bullet = Bullets(player.getPosition(), player.direction)
                active_sprites.add(bullet)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.movex < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.movex > 0:
                player.stop()

    active_sprites.update()

    #check if bullet hits mob
    hits = pygame.sprite.groupcollide(mobs, bullet_list, True, True)
    for hit in hits:
        m = Mob()
        active_sprites.add(m)
        mobs.add(m)

    # checks mob player collision
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
         event.type = sys.exit()
    current_level.update()


    screen.blit(Bg.image, Bg.rect)
    m.move_towards_player(player)
    active_sprites.draw(screen)
    current_level.draw(screen)





    pygame.display.flip()
