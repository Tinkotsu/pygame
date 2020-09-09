import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

LIGHT_BLUE = (135, 206, 250)
WHITE = (255, 255, 255)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.img = pygame.image.load("jet.png").convert()
        self.surf = pygame.transform.scale(self.img, (50, 40))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.left > SCREEN_WIDTH:
            self.rect.left = 0
            self.rect.y = SCREEN_HEIGHT//2
            return 1
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super(Enemy, self).__init__()
        self.img = pygame.image.load("missile.png").convert()
        self.surf = pygame.transform.scale(self.img, (20, 20))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 12)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


def put_text(message, x, y):
    text = font.render(message, True, WHITE)
    place = text.get_rect(center=(x, y))
    screen.blit(text, place)


def game_over():
    global score
    screen.fill(LIGHT_BLUE)
    put_text("Game over! Final score: " + str(score), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                exit()
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    pygame.quit()
                    exit()


font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

score = 0

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()
    enemies.update()
    if player.update():
        for enemy in enemies:
            enemy.kill()
        score += 1

    screen.fill(LIGHT_BLUE)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if player.rect.right < SCREEN_WIDTH and pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        game_over()

    put_text(("score: " + str(score)), SCREEN_WIDTH - 100, 50)
    pygame.display.flip()

    clock.tick(30)
