import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

colors = [WHITE, BLACK, GRAY, LIGHT_BLUE, GREEN, YELLOW, PINK, RED, BLUE]

heights = [100, SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 100]

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)


def put_text(message, m_color):
    text = font.render(message, True, m_color)
    place = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, place)
    pygame.display.flip()


def draw():
    gate_colors = [GRAY, GRAY, GRAY]
    screen.fill(WHITE)
    if gate != -1:
        gate_colors[gate] = GREEN
    pygame.draw.rect(screen, gate_colors[0], (SCREEN_WIDTH - 20, heights[0] - 50, 20, 100))
    pygame.draw.rect(screen, gate_colors[1], (SCREEN_WIDTH - 20, heights[1] - 50, 20, 100))
    pygame.draw.rect(screen, gate_colors[2], (SCREEN_WIDTH - 20, heights[2] - 50, 20, 100))
    pygame.draw.circle(screen, color, (x, y), 20)
    pygame.display.flip()


def victory():
    screen.fill(WHITE)
    put_text("Победа!", GREEN)
    going = True
    while going:
        for v_event in pygame.event.get():
            if v_event.type == pygame.QUIT:
                going = False
    pygame.quit()
    exit()


running = True
x = 0
y = random.choice(heights)
v = 5
color = GREEN
gate = -1
won = 0
lvl = 1

while running:
    if x >= SCREEN_WIDTH - 40:
        v = 0
        if gate == -1 or heights[gate] != y:
            msg = 'Проигрыш!'
            msg_color = RED
        else:
            msg = 'Уровень ' + str(lvl) + ' пройден. Нажмите Enter.'
            msg_color = GREEN
            won = 1
        put_text(msg, msg_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                color = random.choice(colors)
            if x < SCREEN_WIDTH - 40:
                if event.key == pygame.K_1:
                    gate = 0
                if event.key == pygame.K_2:
                    gate = 1
                if event.key == pygame.K_3:
                    gate = 2
            if won and event.key == pygame.K_RETURN:
                x = 0
                y = random.choice(heights)
                gate = -1
                won = 0
                lvl += 1
                v = lvl * 5
    if lvl > 10:
        victory()
    draw()
    x += v
    clock.tick(30)
pygame.quit()
exit()
