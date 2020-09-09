import pygame as pg
from os import path
from settings import *
from sprites import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.images = Images()
        self.bg = None
        self.bg2 = None
        self.bg_rect = None
        self.bg_x = 0
        self.bg2_x = 0
        self.load_data()
        self.all_sprites = None
        self.zombies = None
        self.zarms = None
        self.player = None
        self.bullets = None
        self.spawn_zombie = pg.USEREVENT + 1
        self.spawn_zarms = pg.USEREVENT + 2
        self.speed = GAME_SPEED
        self.playing = False
        self.score = 0

    def load_data(self):
        file_dir = path.dirname(__file__)
        img_dir = path.join(file_dir, 'img')
        bg = path.join(img_dir, BACKGROUND)
        self.bg = pg.image.load(bg).convert()
        self.bg = pg.transform.scale(self.bg, (1500, 600))
        self.bg_rect = self.bg.get_rect()
        self.bg_x = 0
        self.bg2_x = self.bg_rect.width
        self.images.load_images(img_dir, 'bullet', 1, 'bullet', 3, 3)
        zombie_dir = path.join(img_dir, 'zombie')
        self.images.load_images(zombie_dir, 'go', 10, 'zombie', 2.5, 2.5)
        self.images.load_images(zombie_dir, 'zarm', 1, 'zarm', 2, 2)
        alien_dir = path.join(img_dir, 'alien')
        self.images.load_images(alien_dir, 'run', 6, 'run', 3, 3)
        self.images.load_images(alien_dir, 'jump', 2, 'jump', 3, 3)
        self.images.load_images(alien_dir, 'shoot', 7, 'shoot', 3, 3)

    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.zombies = pg.sprite.Group()
        self.zarms = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.player = Player(self)
        pg.time.set_timer(self.spawn_zombie, ZOMBIE_FREQ)
        pg.time.set_timer(self.spawn_zarms, ZARMS_FREQ)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def update(self):
        self.all_sprites.update()
        bullet_hit = pg.sprite.groupcollide(self.bullets, self.zombies, True, True)
        if bullet_hit:
            self.score += 1
        zombie_hits = pg.sprite.spritecollide(self.player, self.zombies, False)
        if zombie_hits:
            self.playing = False
        zarm_hits = pg.sprite.spritecollide(self.player, self.zarms, False)
        if zarm_hits \
                and self.player.rect.right > zarm_hits[0].rect.centerx - 20 \
                and self.player.rect.centerx < zarm_hits[0].rect.centerx + 20 \
                and not self.player.jumping:
            self.playing = False

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_1:
                    self.player.shoot()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
            if event.type == self.spawn_zombie:
                Zombie(game)
            if event.type == self.spawn_zarms:
                Zarm(self)

    def draw(self):
        self.screen.blit(self.bg, (self.bg_x, 0))
        self.screen.blit(self.bg, (self.bg2_x, 0))
        self.bg_x -= self.speed
        self.bg2_x -= self.speed
        if self.bg_x < -self.bg_rect.width:
            self.bg_x = self.bg_rect.width
        if self.bg2_x < -self.bg_rect.width:
            self.bg2_x = self.bg_rect.width

        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH - 30, 30)
        pg.display.flip()

    def end(self):
        if not self.running:
            return
        self.screen.blit(self.bg, (0, 0))
        self.draw_text("GAME OVER", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4 - 50)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


game = Game()
while game.running:
    game.new()
    game.end()
pg.quit()
