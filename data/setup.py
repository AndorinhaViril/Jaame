__author__ = "AndorinhaViril"

import os
import pygame as pg
import data.loop
import data.constants as c

os.environ['SDL_VIDEO_CENTERED'] = '1'

pg.display.set_caption(c.TITLE)
SCREEN = pg.display.set_mode(c.SCREEN_SIZE,pg.RESIZABLE)
SCREEN_RECT = SCREEN.get_rect()


programIcon = pg.image.load(os.path.join('resources\graphics','player.png'))

pg.display.set_icon(programIcon)


FONTS = ''
MUSIC = ''
GFX = ''
SFX = ''
