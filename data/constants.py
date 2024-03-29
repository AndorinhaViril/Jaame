__author__ = "AndorinhaViril"

#variaveis de uso mutuo

#screen_configs
SCREEN_ZOOM = .75
ZOOM_OPTIONS = {.25:'4x',.5:'2x',.75:'1.5x',1:'STANDARD',1.5:'-1.5x',2:'-2x',3:'-3x'}
DISPLAY_HEIGHT = 480#720#
DISPLAY_WIDTH = 854#1280#
DISPLAY_SIZE = (DISPLAY_WIDTH,DISPLAY_HEIGHT)
SCREEN_HEIGHT = DISPLAY_HEIGHT*SCREEN_ZOOM
SCREEN_WIDTH = DISPLAY_WIDTH*SCREEN_ZOOM
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
print(SCREEN_SIZE)
#general_configs
FPS = 30
TITLE = "Jaame"
BLOCK_SIZE = (70,70)
DRAW_DISTANCE_X = 7 if SCREEN_ZOOM <= 1 else 7*SCREEN_ZOOM
DRAW_DISTANCE_Y = 5 if SCREEN_ZOOM <= 1 else 5*SCREEN_ZOOM
SAVE_COMPLETED_PHASES = False
COLLISION_BLOCKS_ONLY = True
#colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
REDA = (255,0,0,155)
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
#screen_states
MENU = 'menu'
PAUSE = 'pause'
SPHASE = 'savephase'
LPHASE = 'loadphase'
CONFIG = 'menuconfig'
IMPIKA = 'creditos'
LOAD = 'carregando'
PLAY = 'jogando'
CLOSE = 'sair'
#player_states
STAND = 'standing'
COWER = 'cower'
WALK = 'walk'
WALKR = 'walkright'
WALKL = 'walkleft'
WALKJ = 'walk+jump'
JUMP = 'jump'
CLIMB = 'climb'
FALL = 'fall'
ATTACK = 'atack'
#player_states_for_death
ALIVE = 'live'
STOMPED = 'fall'
SLASH = 'saw'
SHOT = 'shot'

def load_configs():
    text_file = open('resources\\config\\config.cfg', 'r')
    text = text_file.readlines()
    global SAVE_COMPLETED_PHASES
    global COLLISION_BLOCKS_ONLY
    global SCREEN_ZOOM
    global SCREEN_HEIGHT
    global SCREEN_WIDTH
    global SCREEN_SIZE
    global DRAW_DISTANCE_X
    global DRAW_DISTANCE_Y
    
    for line in text:
        content = line.split(':')
        if content[0] == 'scp':
            try:
                SAVE_COMPLETED_PHASES = bool(content[1])
            except ValueError:
                break
        elif content[0] == 'cbo':
            try:
                COLLISION_BLOCKS_ONLY = bool(content[1])
            except ValueError:
                break
        elif content[0] == 'sz':
            try:
                SCREEN_ZOOM = float(content[1])
                SCREEN_HEIGHT = DISPLAY_HEIGHT*SCREEN_ZOOM
                SCREEN_WIDTH = DISPLAY_WIDTH*SCREEN_ZOOM
                SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
                DRAW_DISTANCE_X = 7 if SCREEN_ZOOM <= 1 else 7*SCREEN_ZOOM
                DRAW_DISTANCE_Y = 5 if SCREEN_ZOOM <= 1 else 5*SCREEN_ZOOM
            except ValueError:
                break
def save_configs():
    text_file = open('resources\\config\\config.cfg', 'w')
    text_file.write(f'scp:{SAVE_COMPLETED_PHASES}\ncbo:{COLLISION_BLOCKS_ONLY}\nsz:{SCREEN_ZOOM}')
    
    
    
    
    
    
