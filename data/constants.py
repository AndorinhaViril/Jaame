__author__ = "AndorinhaViril"
'''
variaveis de de uso mutuo
'''
#configs
SCREEN_HEIGHT = 480
SCREEN_WIDTH = 854
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
DISPLAY_HEIGHT = 480#720#
DISPLAY_WIDTH = 854#1280#
DISPLAY_SIZE = (DISPLAY_WIDTH,DISPLAY_HEIGHT)
FPS = 60
TITLE = "Jaame"
BLOCK_SIZE = (70,70)
DRAW_DISTANCE_X = 6
DRAW_DISTANCE_Y = 6
#COLORS
WHITE = (255, 255, 255)
RED = (255, 0, 0)
REDA = (255,0,0,255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
NAVYBLUE = (60, 60, 100)
GREEN = (0, 255, 0)
FOREST_GREEN = (30, 162, 35)
BLUE = (0, 0, 255)
SKY_BLUE = (40, 145, 250)
YELLOW = (255, 255, 0)
ORANGE = (255, 130, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
NEAR_BLACK = (20, 15, 50)
COMBLUE = (90, 120, 255)
GOLD = (255, 215, 0)
GBROWN = (145,105,90)
BGCOLORP = GBROWN
BGCOLOR = COMBLUE
#speeds
ACCEL = 1.5
MAX_SPEED = 15
JUMP_FORCE = -17
TERMINAL_SPEED = 37
BULLETSPEED = 8
#ScreenStates
MENU = 'menu'
PAUSE = 'pause'
CONFIG = 'menuconfig'
IMPIKA = 'creditos'
LOAD = 'carregando'
PLAY = 'jogando'
CLOSE = 'sair'
#PlayerStates
STAND = 'standing'
COWER = 'cower'
WALK = 'walk'
WALKR = 'walkright'
WALKL = 'walkleft'
WALKJ = 'walk+jump'
JUMP = 'jump'
CLIMB = 'climb'
FALL = 'fall'
ATTACK ='atack'
#PlayerStatesForDeath
ALIVE = 'live'
STOMPED = 'fall'
SLASH = 'saw'
SHOT = 'shot'
