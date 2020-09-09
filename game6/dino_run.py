import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 200

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino run!')


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


font = pygame.font.Font(None, 36)


def put_text(message, x, y):
    text = font.render(message, True, BLACK)
    place = text.get_rect(center=(x, y))
    screen.blit(text, place)


def game_over():
    screen.fill(WHITE)
    put_text("Game over!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super(Dino, self).__init__()
        self.image = pygame.image.load('dino.png').convert()
        self.image = pygame.transform.scale(self.image, (44, 47))
        self.rect = self.image.get_rect()
        self.image1 = pygame.image.load('dino1.png').convert()
        self.image1 = pygame.transform.scale(self.image1, (44, 47))
        self.image2 = pygame.image.load('dino2.png').convert()
        self.image2 = pygame.transform.scale(self.image2, (44, 47))
        self.images = [self.image, self.image1, self.image2]
        self.rect.x = 10
        self.height = SCREEN_HEIGHT - 10 - self.rect.height
        self.rect.y = self.height
        self.isJumping = False
        self.jumpSpeed = 13
        self.run_counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if keys[pygame.K_SPACE] and self.rect.y == self.height:
            self.isJumping = True
        if self.isJumping:
            self.rect.y -= self.jumpSpeed
            self.jumpSpeed -= 1
            self.image = self.images[0]
            self.run_counter = 0
        else:
            if self.run_counter < 10:
                self.image = self.images[1]
            else:
                self.image = self.images[2]
            if self.run_counter > 20:
                self.run_counter = 0
            self.run_counter += 1
        if self.rect.y > self.height:
            self.rect.y = self.height
            self.isJumping = False
            self.jumpSpeed = 13


class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super(Cactus, self).__init__()
        self.image1 = pygame.image.load('cactus1.png').convert()
        self.image2 = pygame.image.load('cactus2.png').convert()
        self.image3 = pygame.image.load('cactus3.png').convert()
        self.image1 = pygame.transform.scale(self.image1, (30, 40))
        self.image2 = pygame.transform.scale(self.image2, (30, 40))
        self.image3 = pygame.transform.scale(self.image3, (30, 40))
        self.image = random.choice([self.image1, self.image2, self.image3])
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.rect.x = SCREEN_WIDTH + self.rect.width + random.randrange(10, 150)
        self.speed = 7

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()


class Ground:
    def __init__(self):
        self.image = pygame.image.load('ground.png').convert()
        self.image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT
        self.image1 = pygame.image.load('ground.png').convert()
        self.image1.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.rect1 = self.image1.get_rect()
        self.rect1.bottom = SCREEN_HEIGHT
        self.rect1.left = self.rect.right
        self.speed = 7

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.image1, self.rect1)

    def update(self):
        self.rect.x -= self.speed
        self.rect1.x -= self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right


clock = pygame.time.Clock()
running = True
score = 0
pause = False

ground = Ground()
dino = Dino()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(dino)

add_cactus = pygame.USEREVENT + 1
pygame.time.set_timer(add_cactus, 1500)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not pause:
                    pause = True
                else:
                    pause = False
        if event.type == add_cactus and len(enemies) < 3:
            cactus = Cactus()
            all_sprites.add(cactus)
            enemies.add(cactus)
    keys = pygame.key.get_pressed()
    if not pause:
        screen.fill(WHITE)
        score += 1
        ground.update()
        ground.draw()
        all_sprites.update()
        all_sprites.draw(screen)
    else:
        put_text("pause", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    put_text(("score: " + str(score // 5)), SCREEN_WIDTH - 80, 40)
    if pygame.sprite.spritecollideany(dino, enemies):
        game_over()
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
exit()
