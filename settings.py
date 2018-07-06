# define some colors (R, G, B)
from __future__ import division
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 512   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 512  # 16 * 48 or 32 * 24 or 64 * 12
MSG_HEIGHT = 128
MSG_WRAP_WIDTH = 25
MSG_WRAP_HEIGHT = 400
FPS = 60
TITLE = u"Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 300
