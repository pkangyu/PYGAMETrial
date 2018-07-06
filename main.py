from __future__ import division
from __future__ import absolute_import
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

class Game(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, u"img")
        map_folder = path.join(game_folder, u"map")
        self.dialog_img = pg.image.load(path.join(img_folder, u'DialogBox.png'))
        self.player_img = path.join(img_folder, u"player")
        self.map_name = u"MRT"
        self.map = TiledMap(path.join(map_folder, self.map_name+u".TMX"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()


    def new(self):
        # initialize all variables and do all the setup for a new game

        self.all_sprites =  pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.walls_message = pg.sprite.Group()
        #for row, tiles in enumerate(self.map.data):
        #    for col, tile in enumerate(tiles):
        #    for col, tile in enumerate(tiles):
        #        if tile == '1':
        #            Wall(sel f, col, row)
        #        if tile == 'P':
        #            self.player = Player(self, col, row)

        for tile_object in self.map.tmxdata.objects:
             if tile_object.name == u'Player':
                self.player = Player(self, tile_object.x, tile_object.y)
             if tile_object.type in [u'npc',u'wall']:
                obj = Obstacle(self, tile_object.x, tile_object.y ,tile_object.width ,tile_object.height)
                self.walls.add(obj)
                if tile_object.type in [u'npc']:
                    obj = Obstacle(self, tile_object.x - 16, tile_object.y - 16 ,tile_object.width + 32, tile_object.height + 32, tile_object.name)
                    self.walls_message.add(obj)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(BLACK)
        pg.display.set_caption(u"{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if self.player.dialog_activation:
            self.player.draw_dialog()
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
