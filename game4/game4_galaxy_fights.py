import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)


def put_text(message, x, y):
    text = font.render(message, True, WHITE)
    place = text.get_rect(center=(x, y))
    screen.blit(text, place)


def victory():
    screen.fill(BLACK)
    put_text("VICTORY!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()


def game_over():
    screen.fill(BLACK)
    put_text("Game over!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.surf = pygame.Surface((width, 20))
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self):
        if self.rect.bottom > SCREEN_HEIGHT:
            game_over()
        bul = pygame.sprite.spritecollideany(self, bullets)
        if bul:
            self.kill()
            bul.kill()
        if freeze != 1:
            self.rect.move_ip(0, 1)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((2, 6))
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self):
        if self.rect.bottom < 0:
            self.kill()
        self.rect.y -= 10

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-30))

    def update(self):
        if pressed_keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)

    def draw(self):
        pygame.draw.polygon(screen, WHITE, [[self.rect.x+15, self.rect.y],
                                            [self.rect.x, self.rect.y+30],
                                            [self.rect.x+30, self.rect.y+30]])


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

level = 1
ready = False
running = True
freeze = 0
fr_count = 0


def gen_enemies():
    line_amount = 1 + level * 2
    enemy_w = (SCREEN_WIDTH - 40) // line_amount - 20
    y = -30 * level * 2
    for _ in range(level * 2 + 1):
        x = 30 + enemy_w // 2
        for _ in range(line_amount):
            enemy = Enemy(x, y, enemy_w)
            all_sprites.add(enemy)
            enemies.add(enemy)
            x += enemy_w + 20
        y += 30


while running:
    if len(enemies) == 0 and len(bullets) == 0 and ready:
        if level == 5:
            victory()
        ready = False
        level += 1
        freeze = 0
        fr_count = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if freeze == 0 and event.key == pygame.K_LSHIFT:
                freeze = 1
            if event.key == pygame.K_SPACE:
                if freeze == 1:
                    fr_count += 1
                if fr_count >= level * 2 + 2:
                    freeze = 2
                bullet = Bullet(player.rect.x + 15, player.rect.y)
                all_sprites.add(bullet)
                bullets.add(bullet)
            if event.key == pygame.K_RETURN:
                if not ready:
                    gen_enemies()
                    ready = True

    pressed_keys = pygame.key.get_pressed()

    all_sprites.update()

    screen.fill(BLACK)
    for entity in all_sprites:
        entity.draw()

    if not ready:
        put_text("Press enter to start next level", SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        put_text("You have 1 freeze ability. Activate on LSHIFT", SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 + 50)
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
exit()
