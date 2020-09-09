import pygame
import random
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pygame.image.load("background.jpg").convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)

enemy_images = []

item_images = []
item_images_names = ('apple', 'cake', 'cherry', 'pear', 'ruby')

for name in item_images_names:
    img = pygame.image.load(name + '.png').convert()
    if name == 'ruby' or name == 'cake' or name == 'apple':
        img.set_colorkey((0, 0, 0), pygame.RLEACCEL)
    else:
        img.set_colorkey((255, 255, 255), pygame.RLEACCEL)
    img = pygame.transform.scale(img, (40, 40))
    item_images.append(img)

for i in range(1, 3):
    img = pygame.image.load('monster' + str(i) + '.png').convert()
    if i == 1:
        img.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        img = pygame.transform.scale(img, (50, 50))
    else:
        img.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        img = pygame.transform.scale(img, (60, 60))
    enemy_images.append(img)


def put_text(message, x, y, color=WHITE):
    text = font.render(message, True, color)
    place = text.get_rect(center=(x, y))
    screen.blit(text, place)


def game_over():
    screen.blit(bg, [0, 0])
    put_text('Game over!', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120)
    put_text('Final score: ' + str(score), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160)
    pygame.display.flip()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bird.png").convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.image_left = self.image
        self.image_right = pygame.transform.flip(self.image, 1, 0)
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.rect.x = SCREEN_WIDTH // 2
        self.speed = 6

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if keys[pygame.K_SPACE]:
            self.speed = 20
        else:
            self.speed = 6
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
            self.image = self.image_left
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
            self.image = self.image_right
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(item_images)
        self.rect = self.image.get_rect()
        self.speed = random.randrange(3, 7)
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, 0)

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        global hp
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            hp -= 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(enemy_images)
        self.rect = self.image.get_rect()
        self.speed = random.randrange(4, 8)
        self.rect.y = random.randrange(-100, 0)
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


clock = pygame.time.Clock()
score = 0
hp = 5

running = True

player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
items = pygame.sprite.Group()
enemies = pygame.sprite.Group()

add_item = pygame.USEREVENT + 1
pygame.time.set_timer(add_item, 2000)

add_enemy = pygame.USEREVENT + 2
pygame.time.set_timer(add_enemy, 7000)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == add_item and len(all_sprites) < 6:
            item = Item()
            all_sprites.add(item)
            items.add(item)
        if event.type == add_enemy and len(all_sprites) < 6:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

    keys = pygame.key.get_pressed()

    screen.blit(bg, [0, 0])
    all_sprites.update()
    all_sprites.draw(screen)

    if hp == 0:
        game_over()
    if pygame.sprite.spritecollide(player, enemies, True):
        game_over()
    if pygame.sprite.spritecollide(player, items, True):
        score += 1

    put_text(("score: " + str(score)), SCREEN_WIDTH - 80, 40)
    put_text(("HP: " + str(hp)), SCREEN_WIDTH - 80, 70)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
