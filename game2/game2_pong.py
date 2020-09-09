import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

square = pygame.Rect(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10, 20, 20)

velocity_x = -5
velocity_y = 0

left_pad = pygame.Surface((20, 80)).get_rect(center=(20, SCREEN_HEIGHT//2))
right_pad = pygame.Surface((20, 80)).get_rect(center=(SCREEN_WIDTH - 20, SCREEN_HEIGHT//2))

pads = [left_pad, right_pad]

running = 1
clock = pygame.time.Clock()

left_player = 0
right_player = 0
ready = 0

font = pygame.font.Font(None, 36)


def put_text(message, x, y):
    text = font.render(message, True, WHITE)
    place = text.get_rect(center=(x, y))
    screen.blit(text, place)


def victory():
    player = '1' if left_player > right_player else '2'
    screen.fill(BLACK)
    put_text(("Player " + player + " won!"), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        if not ready and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ready = 1

    if left_player >= 7 or right_player >= 7 and abs(left_player - right_player) > 1:
        victory()

    if square.x > SCREEN_WIDTH or square.x < 0:
        if square.x > SCREEN_WIDTH:
            left_player += 1
        else:
            right_player += 1
        velocity_x = random.choice((-5, 5))
        velocity_y = 0
        square.x = SCREEN_WIDTH // 2 - 10
        square.y = SCREEN_HEIGHT // 2 - 10
        ready = 0

    if ready:
        square.move_ip(velocity_x, velocity_y)

    if square.collidelist(pads) >= 0:
        velocity_x = -velocity_x * 1.1
        velocity_y = random.randint(-8, 8)

    if square.y >= SCREEN_HEIGHT - square.height or square.y <= 0:
        velocity_y = -velocity_y

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and left_pad.y > 0:
        left_pad.y -= 8
    if keys[pygame.K_s] and left_pad.y < SCREEN_HEIGHT - 80:
        left_pad.y += 8

    if keys[pygame.K_UP] and right_pad.y > 0:
        right_pad.y -= 8
    if keys[pygame.K_DOWN] and right_pad.y < SCREEN_HEIGHT - 80:
        right_pad.y += 8

    screen.fill(BLACK)

    put_text(("Player 1 score: " + str(left_player)), SCREEN_WIDTH // 2 - 200, 40)
    put_text(("Player 2 score: " + str(right_player)), SCREEN_WIDTH // 2 + 200, 40)

    pygame.draw.rect(screen, WHITE, square)
    pygame.draw.rect(screen, WHITE, right_pad)
    pygame.draw.rect(screen, WHITE, left_pad)

    pygame.display.flip()
    clock.tick(30)
