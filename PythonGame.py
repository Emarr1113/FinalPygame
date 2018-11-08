import sys, pygame, random, math

WIDTH = 1014
HEIGHT = 502

pygame.init()

speed = (0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

vec = pygame.math.Vector2
black = (0, 0, 0)
yellow = (255, 255, 0)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 25)

pygame.display.set_caption("Cosmic Defender")

class Background(pygame.sprite.Sprite):
    def __init__(self, image, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("map.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("platform.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.image = pygame.image.load("playerRight.png")
        self.image = pygame.image.load("playerLeft.png")
        self.rect = self.image.get_rect()
        self.movex = 0  # move along X
        self.movey = 0  # move along Y
        self.level = None
        self.direction = 1
        self.radius = 25
        # self.health = 30
        # check player circle
        # pygame.draw.circle(self.image, yellow, self.rect.center, self.radius)
    def getPosition(self):
        return (self.rect.left + 76, self.rect.top + 35)

    def updateDirection(self, direction):
        self.direction = direction

    def update(self):
        # Gravity
        self.calcGravity()
        self.rect.x += self.movex
        self.rect.y += self.movey
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for platform in platform_hit_list:
            if self.movey > 0:
                self.rect.bottom = platform.rect.top
                self.movey = 0
        if self.rect.left <0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullets(player.getPosition(), self.direction)
        active_sprites.add(bullet)
        bullets.add(bullet)

    def calcGravity(self):
        if self.movey == 0:
            self.movey = 1
        else:
            self.movey += 0.35
        if self.rect.y >= HEIGHT - self.rect.height and self.movey >= 0:
            self.movey = 0
            self.rect.y = HEIGHT - self.rect.height

    def jump(self):
        self.movey = -8

    def go_Left(self):
        self.direction = -1
        self.movex = -8
        self.image = pygame.image.load("playerLeft.png")

    def go_Right(self):
        self.direction = 1
        self.movex = 8
        self.image = pygame.image.load("playerRight.png")

    def go_Up(self):
        self.movey = -8

    def go_Down(self):
        self.movey = 8

    def stop(self):
        self.movex = 0


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image = pygame.image.load('enemy.png')
        self.rect = self.image.get_rect()
        self.radius = 35
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        # check enemy circle
        # pygame.draw.circle(self.image, yellow, self.rect.center, self.radius)
        self.speed = -9
        # self.damage = 10

    def move_towards_player(self, player):
        # find normalized direction vector (dx, dy) between enemy and player

        dx, dy = self.rect.x - player.rect.x, self.rect.y - player.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        # move along this normalized vector towards the player at current speeds
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

class Level(object):
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.background = None

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


class LevelOne(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        level = [[195, 36, 422, 171], [195, 36, 72, 358], [195, 36, 752, 358], ]

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

    def update(self):
        self.rect.x += (10 * self.direction)
        # Bullet dies off screen
        if self.rect.left < 0 or self.rect.right > 1014:
            self.kill()


Bg = Background("map.png", [0, 0])

pygame.init()

player = Player()
m = Mob()

levels = []
levels.append(LevelOne(player))
current_level = 0
current_level = levels[current_level]
active_sprites = pygame.sprite.Group()

bullets = pygame.sprite.Group()

player.level = current_level
player.rect.x = 450
player.rect.y = HEIGHT - player.rect.height
active_sprites.add(player)

mobs = pygame.sprite.Group()
for i in range(10):
    m = Mob()
    active_sprites.add(m)
    mobs.add(m)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 25)
frame_count = 0
frame_rate = 60
start_time = 90


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
                bullet = player.shoot()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.movex < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.movex > 0:
                player.stop()

    # check if bullet hits mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        active_sprites.add(m)
        mobs.add(m)

    # checks mob player collision
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        event.type = sys.exit()

    clock.tick(30)


    active_sprites.update()

    current_level.update()

    screen.blit(Bg.image, Bg.rect)
    m.move_towards_player(player)
    active_sprites.draw(screen)
    current_level.draw(screen)

    pygame.display.flip()