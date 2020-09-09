import pygame as pg
from settings import *
from os import path
from random import randrange


class Images:
    def __init__(self):
        self.images_dict = dict()

    def load_images(self, folder, file_name, amount, name, scale_x=1, scale_y=1):
        img_list = []
        self.images_dict.update({name: img_list})
        for i in range(1, amount + 1):
            filename = path.join(folder, file_name + str(i) + '.png')
            img = pg.image.load(filename).convert()
            img.set_colorkey(WHITE)
            img_rect = img.get_rect()
            img = pg.transform.scale(img, (int(img_rect.width / scale_x),
                                           int(img_rect.height / scale_y)))
            img_list.append(img)


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.running_imgs = game.images.images_dict['run']
        self.jumping_imgs = game.images.images_dict['jump']
        self.shooting_imgs = game.images.images_dict['shoot']
        self.game = game
        self.running = True
        self.jumping = False
        self.shooting = False
        self.image = self.running_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.center = (75, HEIGHT - 150)
        self.vel_y = 0
        self.current_frame = 0
        self.last_update = 0

    def jump_cut(self):
        if self.jumping:
            if self.vel_y < -3:
                self.vel_y = -3

    def jump(self):
        if self.jumping is False and self.shooting is False:
            self.game.speed += 1
            self.jumping = True
            self.vel_y = -18

    def shoot(self):
        if self.shooting is False and self.jumping is False:
            self.shooting = True
            self.current_frame = 0
            self.game.speed = 0

    def update(self):
        self.animate()
        if self.jumping:
            self.rect.centery += self.vel_y
            self.vel_y += 0.6
            if self.rect.centery > HEIGHT - 150:
                self.rect.centery = HEIGHT - 150
                self.jumping = False
                self.game.speed = GAME_SPEED

    def animate(self):
        now = pg.time.get_ticks()
        if self.jumping:
            if self.vel_y < 0:
                self.image = self.jumping_imgs[0]
            else:
                self.image = self.jumping_imgs[1]
        elif self.shooting:
            if self.current_frame == len(self.shooting_imgs) - 1:
                self.shooting = False
                self.current_frame = 0
                self.game.speed = GAME_SPEED
                Bullet(self)
            elif now - self.last_update > 75:
                self.last_update = now
                self.current_frame += 1
                self.image = self.shooting_imgs[self.current_frame]
        else:
            if now - self.last_update > 75:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.running_imgs)
                self.image = self.running_imgs[self.current_frame]


class Zombie(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.zombies
        super().__init__(self.groups)
        self.game = game
        self.vel = self.game.speed + 1
        self.images = game.images.images_dict['zombie']
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = randrange(WIDTH + 50, WIDTH + 600)
        self.rect.centery = HEIGHT - 140
        self.last_update = 0
        self.current_frame = 0

    def update(self):
        self.vel = self.game.speed + 1
        self.animate()
        self.rect.x -= self.vel
        if self.rect.x < -self.rect.width:
            self.game.score += 1
            self.kill()

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 150:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.last_update = now


class Zarm(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.zarms
        super().__init__(self.groups)
        self.game = game
        self.vel = 0
        self.image = game.images.images_dict['zarm'][0]
        self.rect = self.image.get_rect()
        self.rect.centerx = randrange(WIDTH + 50, WIDTH + 300)
        self.rect.bottom = HEIGHT - 50

    def update(self):
        self.vel = self.game.speed
        if not self.game.player.shooting:
            self.rect.x -= self.vel
        if self.rect.x < -self.rect.width:
            self.game.score += 1
            self.kill()


class Bullet(pg.sprite.Sprite):
    def __init__(self, player):
        self.groups = player.game.all_sprites, player.game.bullets
        super().__init__(self.groups)
        self.vel = 30
        self.image = player.game.images.images_dict['bullet'][0]
        self.rect = self.image.get_rect()
        self.rect.center = (player.rect.centerx + 50, player.rect.centery + 5)

    def update(self):
        if self.rect.x > WIDTH:
            self.kill()
        self.rect.centerx += self.vel
