import sys, pygame

width = 1014
height = 500

speed = (0,0)

black= (0, 0, 0)

screen = pygame.display.set_mode((width, height))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('filler.png')
        self.rect = self.image.get_rect()
        self.movex = 0  # move along X
        self.movey = 0  # move along Y

    def update(self):
        if key[pygame.K_UP]:
            self.rect.move((0, -4))

        # BOTTOM
        if key[pygame.K_DOWN]:
            self.rect.move((0, 4))

        # RIGHT
        if key[pygame.K_RIGHT]:
            self.rect.move((4, 0))

        # LEFT
        if key[pygame.K_LEFT]:
            self.rect.move((-4, 0))


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([4, 10])
        self.image.fill(black)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    filler_rect = filler_rect.move(speed)
    key = pygame.key.get_pressed()
    #TOP
    if key[pygame.K_UP]:
        filler_rect = filler_rect.move((0,-4))

    #BOTTOM
    if key[pygame.K_DOWN]:
        filler_rect = filler_rect.move((0, 4))

    #RIGHT
    if key[pygame.K_RIGHT]:
        filler_rect = filler_rect.move((4,0))

    #LEFT
    if key[pygame.K_LEFT]:
        filler_rect = filler_rect.move((-4,0))


    screen.fill(black)
    screen.blit(Player, filler_rect)
    pygame.display.flip()
