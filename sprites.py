from __future__ import with_statement
from __future__ import absolute_import
import pygame as pg
from settings import *
from io import open
from os import path
from test import *
import json

with open(u'dialog.json') as data_file:
    dialog_msg = json.load(data_file)
def collide_with_walls(sprite, group, dir):
    if dir == u'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel[0] > 0:
                sprite.pos[0] = hits[0].rect.left - sprite.rect.width
            if sprite.vel[0] < 0:
                sprite.pos[0] = hits[0].rect.right
            sprite.vel[0] = 0
            sprite.rect.x = sprite.pos[0]
    if dir == u'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel[1] > 0:
                sprite.pos[1] = hits[0].rect.top - sprite.rect.height
            if sprite.vel[1] < 0:
                sprite.pos[1] = hits[0].rect.bottom
            sprite.vel[1] = 0
            sprite.rect.y = sprite.pos[1]


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.state = 1
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.front[0]
        self.rect = self.image.get_rect()
        self.vel = [0, 0]
        self.pos = [x, y]
        self.dialog_activation = False
        self.dialog_time = 0
        self.more_dialog = False
        self.dialog_no = 0
        self.dialog_time2 = 0
        self.rect.x = x
        self.rect.y = y

    def draw_dialog(self):
        self.dialog_now2 = pg.time.get_ticks()
        hit = self.collide_dialog[0].name
        image = pg.transform.scale(self.game.dialog_img, (WIDTH, MSG_HEIGHT))
        image.set_colorkey(WHITE)
        #blit dialog box
        self.game.screen.blit(image, (0, MSG_HEIGHT*3))
        Name = pg.font.SysFont(u"monospace", 15).render(dialog_msg[hit][u"Name"] + u":",  1, BLACK)
        #blit name
        self.game.screen.blit(Name, (MSG_WRAP_WIDTH, MSG_WRAP_HEIGHT))
        msg = wrapline(dialog_msg[hit][u"msg"], pg.font.SysFont(u"monospace", 15), WIDTH)
        msg_splitted = [msg[x:x+4] for x in xrange(0, len(msg), 4)]
        if len(msg_splitted) > 1:
            self.more_dialog = True
        if self.more_dialog:
                if self.dialog_no - 1 == len(msg_splitted):
                    self.dialog_no = 0
                    self.more_dialog = False
                    self.dialog_activation = False
                if pg.key.get_pressed()[pg.K_SPACE]:
                        if self.dialog_now2 - self.dialog_time2 > 200 :
                            pg.time.delay(500)
                            self.dialog_no += 1
                            self.first_ignore = False
                            self.dialog_time2 = self.dialog_now2 
                            self.dialog_time = self.dialog_now2
                        else:
                            pass
                else:
                    pass
        self.display_msg = msg_splitted[self.dialog_no]
        LINE_HEIGHT = 15
        for i in self.display_msg:
            Msg = pg.font.SysFont(u"monospace", 15).render(i,1, BLACK)
            self.game.screen.blit(Msg, (MSG_WRAP_WIDTH, MSG_WRAP_HEIGHT + LINE_HEIGHT))
            LINE_HEIGHT += 15

    def load_images(self):
        self.back = [pg.image.load(path.join(self.game.player_img, u'back.png')).convert(),
                     pg.image.load(path.join(self.game.player_img, u'back2.png')).convert()]
        for frame in self.back:
            frame.set_colorkey(YELLOW)
        self.front = [pg.image.load(path.join(self.game.player_img, u'front.png')).convert(),
                     pg.image.load(path.join(self.game.player_img, u'front2.png')).convert()]
        for frame in self.front:
            frame.set_colorkey(YELLOW)
        self.right = [pg.image.load(path.join(self.game.player_img, u'right.png')).convert(),
                     pg.image.load(path.join(self.game.player_img, u'right2.png')).convert()]
        for frame in self.right:
            frame.set_colorkey(YELLOW)
        self.left = [pg.image.load(path.join(self.game.player_img, u'left.png')).convert(),
                     pg.image.load(path.join(self.game.player_img, u'left2.png')).convert()]
        for frame in self.left:
            frame.set_colorkey(YELLOW)
        self.resting = [pg.image.load(path.join(self.game.player_img, u'resting.png')).convert(),
                     pg.image.load(path.join(self.game.player_img, u'resting2.png')).convert()]
        for frame in self.resting:
            frame.set_colorkey(YELLOW)

    def get_keys(self):
        self.dialog_now = pg.time.get_ticks()
        self.vel = [0, 0]
        keys = pg.key.get_pressed()
        if not self.dialog_activation:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.vel[0] = -PLAYER_SPEED
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.vel[0] = PLAYER_SPEED
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.vel[1] = -PLAYER_SPEED
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.vel[1] = PLAYER_SPEED
            if self.vel[0] != 0 and self.vel[1] != 0:
                self.vel = [self.vel[0] * 0.7071, self.vel[1] *0.7071 ]
        if keys[pg.K_SPACE] and self.dialog_now - self.dialog_time > 200:
            if pg.sprite.spritecollide(self, self.game.walls_message, False) :
                self.collide_dialog = pg.sprite.spritecollide(self, self.game.walls_message, False)
                if self.more_dialog:
                    pass
                else:
                    self.dialog_activation = not self.dialog_activation
                self.dialog_time = self.dialog_now

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel[0] != 0 and self.vel[1] == 0:
            self.state = 1
        elif self.vel[1] != 0 and self.vel[0] == 0 :
            self.state = 2
        elif self.vel[1] == 0 and self.vel[0] == 0:
            self.state = 3
        else:
            pass

        if self.state == 1:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.front)
                if self.vel[0] > 0:
                    self.image =  self.right[self.current_frame]
                else:
                    self.image = self.left[self.current_frame]
        elif self.state == 2:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.front)
                if self.vel[1] > 0:
                    self.image = self.front[self.current_frame]
                else:
                    self.image = self.back[self.current_frame]

        elif self.state == 3:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.front)
                self.image = self.resting[self.current_frame]

    def update(self):
        self.get_keys()
        self.animate()
        self.pos = [self.vel[0] * self.game.dt,self.vel[1] * self.game.dt ]
        self.rect.x = self.rect.x + self.pos[0]
        collide_with_walls(self, self.game.walls, u'x')
        self.rect.y = self.rect.y + self.pos[1]
        collide_with_walls(self, self.game.walls, u'y')

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, name=None):
        self.name = name
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect((x, y , w, h))
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
#        self.game = game
#        self.image = game.dialog_img
#        self.rect = self.image.get_rect()
#        self.rect.center = (WIDTH/2, HEIGHT/2)

def draw_text(surf, text, size, x, y):
    ## selecting a cross platform font to display the score
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)       ## True denotes the font to be anti-aliased
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
