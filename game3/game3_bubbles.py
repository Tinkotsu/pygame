import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 64)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)


def put_text(message, x, y):
    text = font.render(message, True, GREEN)
    place = text.get_rect(center=(x, y))
    screen.blit(text, place)


def victory():
    screen.fill(WHITE)
    put_text("VICTORY!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()


def game_over():
    screen.fill(WHITE)
    put_text("Game over!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()


class Bubble(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = (random.randrange(255), random.randrange(255), random.randrange(255))
        self.size = 80 - level * 5
        self.surf = pygame.Surface((self.size, self.size))
        self.rect = self.surf.get_rect()
        self.rect.x = random.randint(100, 600)
        self.rect.y = random.randint(SCREEN_HEIGHT + 40, SCREEN_HEIGHT + 300)
        self.vel_x = random.randint(-7, 7)
        self.vel_y = random.randrange(int(-level * 1.5), int(-level / 2))

    def draw(self):
        pygame.draw.circle(screen, self.color,
                           (self.rect.x + self.size//2, self.rect.y + self.size//2), self.size//2)

    def move(self):
        global lives
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        if b.rect.collidepoint(*mouse_pos) and mouse_clicked[0]:
            b.kill()
        if self.rect.left < 0:
            self.vel_x = abs(self.vel_x)
        if self.rect.right > SCREEN_WIDTH:
            self.vel_x = -abs(self.vel_x)
        self.rect.move_ip(self.vel_x, self.vel_y)
        if self.rect.bottom < 0:
            lives -= 1
            if lives < 0:
                game_over()
            self.kill()


level = 1
lives = 5
ready = False
running = True

all_bubbles = pygame.sprite.Group()


def generate_bubbles():
    for _ in range(10 + level * 2):
        all_bubbles.add(Bubble())


while running:
    if ready and len(all_bubbles) == 0:
        ready = 0
        level += 1
        if level == 7:
            victory()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not ready:
                    generate_bubbles()
                    ready = True
    screen.fill(WHITE)
    for b in all_bubbles:
        b.draw()
        b.move()
    if not ready:
        put_text("Press space to start next level", SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    put_text(("level: " + str(level)), SCREEN_WIDTH - 100, 50)
    put_text(("health: " + str(lives)), SCREEN_WIDTH - 100, 80)
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
exit()
