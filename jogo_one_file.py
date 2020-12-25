import pygame as pg
import os
import random

#constantes
#configs
SCREEN_HEIGHT = 480
SCREEN_WIDTH = 854
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
DISPLAY_HEIGHT = 480#720#
DISPLAY_WIDTH = 854#1280#
DISPLAY_SIZE = (DISPLAY_WIDTH,DISPLAY_HEIGHT)
FPS = 30
TITLE = "Jaame"
BLOCK_SIZE = (70,70)
DRAW_DISTANCE_X = 7
DRAW_DISTANCE_Y = 5
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
MAX_SPEED = 20
JUMP_FORCE = -16
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
#configsIniciais
try:
    pg.init()
except:
    print('Falhou a inicialização do modulo principal')



os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()

pg.display.set_caption(TITLE)
SCREEN = pg.display.set_mode(SCREEN_SIZE,pg.RESIZABLE)
SCREEN_RECT = SCREEN.get_rect()


programIcon = pg.image.load(os.path.join('resources\graphics','player.png'))

pg.display.set_icon(programIcon)

#classes
class menu():
    def __init__(self):
        self.itens = ['Play','Configs','Credits','Get out']
        self.font_title = pg.font.Font('resources/fonts/zenda.ttf',44)
        self.font_text = pg.font.Font('resources/fonts/METROLOX.ttf',20)
        self.title = None
        self.itens_tela = []
        self.itens_rect = []
        self.selected_item = None
        self.select_index = -1
        self.go_to = None
    def reset(self):
        self.selected_item = None
        self.select_index = -1
        self.go_to = None
    def draw(self,screen):
        screen.blit(self.title,(10,15))
        cont = 0
        for i in range(0,len(self.itens_tela)):
            if self.itens_tela[i] is self.selected_item:
                item = self.font_text.render(self.itens[i],True,BLACK)
                screen.blit(item,(20+2,25+self.title.get_height()+self.itens_tela[i].get_height()+cont+2))
            
            screen.blit(self.itens_tela[i],(20,25+self.title.get_height()+self.itens_tela[i].get_height()+cont))
            
            cont+=30
    def start(self):
        self.title = None
        self.itens_tela = []
        self.itens_rect = []
        self.selected_item = None
        self.select_index = -1
        self.can = True
        self.go_to = None
        title = self.font_text.render("JAAME", True, BLACK)
        self.title = title
        cont = 0
        for i in self.itens:
            itens = self.font_text.render(i,True,WHITE)
            self.itens_tela.append(itens)
            rect = itens.get_rect()
            rect.left = 20
            rect.top = 25+self.title.get_height()+itens.get_height()+cont
            self.itens_rect.append(rect)
            cont+=30

    def event(self,mouse,key):
        if key[pg.K_DOWN]:
            if self.can:
                self.can =False
                if self.select_index < len(self.itens_tela)-1:
                    self.select_index += 1
                else:
                    self.select_index = 0
                self.selected_item = self.itens_tela[self.select_index]
        if key[pg.K_UP]:
            if self.can:
                self.can = False
                if self.select_index > 0:
                    self.select_index -= 1
                else:
                    self.select_index = len(self.itens_tela)-1
                self.selected_item = self.itens_tela[self.select_index]
        if not key[pg.K_UP] and not key[pg.K_DOWN]:
            self.can = True
        if key[pg.K_RETURN] or key[pg.K_RIGHT] or key[pg.K_LEFT] or key[pg.K_z]:
            if self.selected_item is not None:
                if self.selected_item == self.itens_tela[0]:
                    self.go_to = PLAY
                if self.selected_item == self.itens_tela[1]:
                    self.go_to = CONFIG
                if self.selected_item == self.itens_tela[2]:
                    self.go_to = IMPIKA
                if self.selected_item == self.itens_tela[3]:
                    self.go_to = CLOSE
        pos = mouse[0]
        for i in range(0,len(self.itens_tela)):
            if self.itens_rect[i].collidepoint(mouse[0]):
                self.selected_item = self.itens_tela[i]
                if mouse[1][0]:
                    if self.selected_item is not None:
                        if self.selected_item == self.itens_tela[0]:
                            self.go_to = PLAY
                        if self.selected_item == self.itens_tela[1]:
                            self.go_to = CONFIG
                        if self.selected_item == self.itens_tela[2]:
                            self.go_to = IMPIKA
                        if self.selected_item == self.itens_tela[3]:
                            self.go_to = CLOSE

class pause():
    def __init__(self):
        self.itens = ['Back','Configs','Start Menu']
        self.font_text = pg.font.Font('resources/fonts/METROLOX.ttf',20)
        self.itens_tela = []
        self.itens_rect = []
        self.selected_item = None
        self.select_index = -1
        self.go_to = None
        self.can = True
    def reset(self):
        self.selected_item = None
        self.select_index = -1
        self.go_to = None
    def draw(self,screen):
        cont = 0
        for i in range(0,len(self.itens_tela)):
            if self.itens_tela[i] is self.selected_item:
                item = self.font_text.render(self.itens[i],True,BLACK)
                screen.blit(item,((DISPLAY_WIDTH/2)-self.itens_tela[i].get_width()/2+2,(DISPLAY_HEIGHT/3)-self.itens_tela[i].get_height()+cont+2))
            screen.blit(self.itens_tela[i],((DISPLAY_WIDTH/2)-self.itens_tela[i].get_width()/2,(DISPLAY_HEIGHT/3)-self.itens_tela[i].get_height()+cont))
            
            cont+=30
    def start(self):
        self.itens_tela = []
        self.itens_rect = []
        self.selected_item = None
        self.select_index = -1
        cont = 0
        for i in self.itens:
            item = self.font_text.render(i,True,WHITE)
            self.itens_tela.append(item)
            rect = item.get_rect()
            rect.left = (DISPLAY_WIDTH/2)-item.get_width()/2
            rect.top = (DISPLAY_HEIGHT/3)-item.get_height()+cont
            self.itens_rect.append(rect)
            cont+=30
    def event(self,mouse,key):
        if key[pg.K_DOWN]:
            if self.can:
                self.can =False
                if self.select_index < len(self.itens_tela)-1:
                    self.select_index += 1
                else:
                    self.select_index = 0
                self.selected_item = self.itens_tela[self.select_index]
        if key[pg.K_UP]:
            if self.can:
                self.can = False
                if self.select_index > 0:
                    self.select_index -= 1
                else:
                    self.select_index = len(self.itens_tela)-1
                self.selected_item = self.itens_tela[self.select_index]
        if not key[pg.K_UP] and not key[pg.K_DOWN]:
            self.can = True
        if key[pg.K_RETURN] or key[pg.K_RIGHT] or key[pg.K_LEFT] or key[pg.K_z]:
            if self.selected_item is not None:
                if self.selected_item == self.itens_tela[0]:
                    self.go_to = PLAY
                if self.selected_item == self.itens_tela[1]:
                    self.go_to = CONFIG
                if self.selected_item == self.itens_tela[2]:
                    self.go_to = MENU

        pos = mouse[0]
        for i in range(0,len(self.itens_tela)):
            if self.itens_rect[i].collidepoint(mouse[0]):
                self.selected_item = self.itens_tela[i]
                if mouse[1][0]:
                    if self.selected_item is not None:
                        if self.selected_item == self.itens_tela[0]:
                            self.go_to = PLAY
                        if self.selected_item == self.itens_tela[1]:
                            self.go_to = CONFIG
                        if self.selected_item == self.itens_tela[2]:
                            self.go_to = MENU

class load_screen():
    def __init__(self):
        self.font_text = pg.font.Font('resources/fonts/METROLOX.ttf',20)
        self.item = None
        self.x = 0
        self.y = 0
        self.points = []

    def start(self):
        self.item = None
        self.x = 0
        self.y = 0
        self.points = []
        self.item = self.font_text.render('LOADING',True,BLACK)
        self.x = DISPLAY_WIDTH-(self.item.get_width()*1.5)//1
        self.y = DISPLAY_HEIGHT-self.item.get_height()
        point = pg.Rect(self.x+self.item.get_width()+4,self.y+self.item.get_height()-7,2,2)
        point1 = pg.Rect(self.x+self.item.get_width()+8,self.y+self.item.get_height()-7,2,2)
        point2 = pg.Rect(self.x+self.item.get_width()+12,self.y+self.item.get_height()-7,2,2)
        self.points.append(point)
        self.points.append(point1)
        self.points.append(point2)
    def draw(self,screen):
        screen.blit(self.item,(self.x,self.y))
        for i in self.points:
            pg.draw.rect(screen,BLACK,i)


class config():
    def __init__(self):
        self.itens = ['Back']
        self.font_text = pg.font.Font('resources/fonts/METROLOX.ttf',20)
        self.title = None
        self.itens_tela = []
        self.itens_rect = []
        self.selected_item = None
        self.go_to = None
        self.from_ = None
        self.can = True
    def draw(self, screen):
        cont = 0
        for i in range(0,len(self.itens_tela)):
            if self.itens_tela[i] is self.selected_item:
                item = self.font_text.render(self.itens[i],True,BLACK)
                screen.blit(item,((DISPLAY_WIDTH/2)-self.itens_tela[i].get_width()/2+2,(DISPLAY_HEIGHT/3)-self.itens_tela[i].get_height()+cont+2))
            screen.blit(self.itens_tela[i],(DISPLAY_WIDTH/2-self.itens_tela[i].get_width()/2, DISPLAY_HEIGHT/3-self.itens_tela[i].get_height()+cont))
            cont = cont + 30

    def start(self):
        self.itens_tela = []
        self.itens_rect = []
        self.selected_item = None
        self.select_index = -1
        cont = 0
        for i in self.itens:
            item = self.font_text.render(i,True,WHITE)
            self.itens_tela.append(item)
            rect = item.get_rect()
            
            rect.left = (DISPLAY_WIDTH/2)-item.get_width()/2
            rect.top = (DISPLAY_HEIGHT/3)-item.get_height()+cont
            self.itens_rect.append(rect)
            cont+=30
    def reset(self):
        self.selected_item = None
        self.select_index = -1
        self.go_to = None
    def event(self,mouse,key):
        if key[pg.K_DOWN]:
            if self.can:
                self.can =False
                if self.select_index < len(self.itens_tela)-1:
                    self.select_index += 1
                else:
                    self.select_index = 0
                self.selected_item = self.itens_tela[self.select_index]
        if key[pg.K_UP]:
            if self.can:
                self.can = False
                if self.select_index > 0:
                    self.select_index -= 1
                else:
                    self.select_index = len(self.itens_tela)-1
                self.selected_item = self.itens_tela[self.select_index]
        if not key[pg.K_UP] and not key[pg.K_DOWN]:
            self.can = True
        if key[pg.K_RETURN] or key[pg.K_RIGHT] or key[pg.K_LEFT] or key[pg.K_z]:
            if self.selected_item is not None:
                if self.selected_item == self.itens_tela[0]:
                    self.go_to = self.from_
        pos = mouse[0]
        for i in range(0,len(self.itens_tela)):
            if self.itens_rect[i].collidepoint(mouse[0]):
                self.selected_item = self.itens_tela[i]
                if mouse[1][0]:
                    if self.selected_item is not None:
                        if self.selected_item == self.itens_tela[0]:
                            self.go_to = self.from_
    def set_from(self,f):
        self.from_ = f
    
class creditz():
    def __init__(self):
        self.item = 'Back'
        self.font_text = pg.font.Font('resources/fonts/METROLOX.ttf',20)
        self.title = None
        self.itens_tela = None
        self.itens_rect = None
        self.selected_item = None
        self.go_to = None
        self.can = True
    def draw(self,screen):
        item = self.font_text.render('by AndorinhaViril  in',True,BLACK)
        screen.blit(item,((DISPLAY_WIDTH/2)-item.get_width()/2,0))
        if self.itens_tela is self.selected_item:
            item = self.font_text.render(self.item,True,BLACK)
            screen.blit(item,((DISPLAY_WIDTH/2)-self.itens_tela.get_width()/2+2,(DISPLAY_HEIGHT)-self.itens_tela.get_height()+2))
        screen.blit(self.itens_tela,((DISPLAY_WIDTH/2)-self.itens_tela.get_width()/2,(DISPLAY_HEIGHT)-self.itens_tela.get_height()))
    def reset(self):
        self.selected_item = None
        self.select_index = -1
        self.go_to = None
    def start(self):
        self.itens_tela = None
        self.itens_rect = None
        self.selected_item = None
        self.select_index = -1
        item = self.font_text.render(self.item,True,WHITE)
        self.itens_tela = item
        rect = item.get_rect()
        rect.left = (DISPLAY_WIDTH/2)-item.get_width()/2
        rect.top = (DISPLAY_HEIGHT)-item.get_height()
        self.itens_rect = rect

    def event(self,mouse,key):
        if key[pg.K_DOWN]:
            if self.can:
                self.can =False
                self.selected_item = self.itens_tela
        if key[pg.K_UP]:
            if self.can:
                self.can = False
                self.selected_item = self.itens_tela
        if not key[pg.K_UP] and not key[pg.K_DOWN]:
            self.can = True
        if key[pg.K_RETURN] or key[pg.K_RIGHT] or key[pg.K_LEFT] or key[pg.K_z]:
            if self.selected_item is not None:
                if self.selected_item == self.itens_tela:
                    self.go_to = MENU
        pos = mouse[0]
        if self.itens_rect.collidepoint(pos):
            self.selected_item = self.itens_tela
            if mouse[1][0]:
                if self.selected_item is not None:
                    self.go_to = MENU
                        
class hud():
    def __init__(self):
        self.font_text = pg.font.Font('resources/fonts/METROLOX.ttf',20)
    def draw(self,screen,player_pos,end_pos,status):
        if status == ALIVE:
            item = self.font_text.render('{}, {} - {}, {}'.format(player_pos[0],player_pos[1],end_pos[0]//70,end_pos[1]//70),True,BLACK)
            screen.blit(item,(0,0))
        else:
            item = self.font_text.render('DIED',True,BLACK)
            item2 = self.font_text.render('DIED',True,WHITE)
            item3 = self.font_text.render('PRESS R TO RESTART',True,WHITE)
            item4 = self.font_text.render('PRESS R TO RESTART',True,BLACK)
            x = DISPLAY_WIDTH/2 - item.get_width()/2
            y = DISPLAY_HEIGHT/2 - item.get_height()
            x2 = DISPLAY_WIDTH/2 - item3.get_width()/2
            y2 = DISPLAY_HEIGHT/2 + item.get_height()
            screen.blit(item,  (x,y))
            screen.blit(item2, (x-2,y-2))
            screen.blit(item4, (x2,y2))
            screen.blit(item3, (x2-2,y2-2))
        
class player(pg.sprite.Sprite):

    def __init__(self):
        #chama o construtor da classe mãe
        pg.sprite.Sprite.__init__(self)
        #variaveis
        self.height = 55
        self.width = 40
        self.images = []
        self.images.append(pg.image.load(os.path.join('resources\graphics', 'player.png')))
        self.images.append(pg.image.load(os.path.join('resources\graphics', 'player2.png')))
        self.images.append(pg.image.load(os.path.join('resources\graphics', 'climb.png')))
        self.images.append(pg.image.load(os.path.join('resources\graphics', 'stomped.png')))
        self.images.append(pg.image.load(os.path.join('resources\graphics', 'dead.png')))
        self.images.append(pg.image.load(os.path.join('resources\graphics', 'bulleted.png')))
        #self.sounds = []
        #self.sounds.append(pg.mixer.Sound(os.path.join('resources\sounds', 'fiaeeee.ogg')))
        #self.sounds.append(pg.mixer.Sound(os.path.join('resources\sounds', 'fiaeeee.ogg')))
        self.sprite = self.images[0]
        self.view_collision = False
        self.iindex = True
        self.cont = 0
        self.atack_cont = 0
        self.x = 0
        self.y = 0
        self.state = STAND
        self.speed = 0
        self.speedy = 0
        self.jump = False
        self.atack = False
        self.climb = False
        self.dead = ALIVE
        self.climb_side = 0#-1 == esquerda +1 direita
        self.flip_sprite = False
        self.on_end = True
        self.startsoundfall = False
        self.sound = False
        self.lookto = ''
        self.collision = pg.Rect(self.x,self.y+12,self.width,self.height)
        self.atack_collision = pg.Rect(self.collision.center[0]+20,self.collision.center[1]+20,20,10)
        self.collisions = {'top':False,'bottom':False,'left':False,'right':False}
    def set_xy(self, xy):
        self.x = xy[0]
        self.y = xy[1] + self.height
        #print('x: {} y: {}'.format(*xy))
    def set_spawn(self, spawn):
        #print('c:{} b:{}'.format(spawn.center,spawn.bottom))
        self.collision.center = spawn.center
        self.collision.bottom = spawn.bottom
        self.x = self.collision.x
        self.y = self.collision.y-12
        self.dead = ALIVE
        self.speedy,self.speed = 0,0
    def swap_state(self, state):
        if self.state != FALL:
            if self.state == JUMP or self.state == WALKJ:
                if state == FALL or state == WALK:
                    self.state = state
            if self.state == WALK:
                if state == WALK or state == JUMP or state == WALKJ:
                    self.state = state
            if self.state == STAND:
                if state == COWER or state == WALK or state == JUMP or state == WALKJ:
                    self.state = state
            if self.state == COWER:
                if state == STAND or state == WALK or state == JUMP:
                    self.state = state
        else:
            self.state = state
            
    def draw(self,screen,camera):
        if self.view_collision:
            col = pg.Rect(self.collision.x-camera[0],self.collision.y-camera[1],self.width,self.height)
            pg.draw.rect(screen,REDA,col)
        if self.atack:
            pg.draw.rect(screen,(190,0,90),pg.Rect(self.atack_collision.x-camera[0],self.atack_collision.y-camera[1],20,10))
        if self.flip_sprite:
            if self.dead == ALIVE:
                if self.climb:
                    screen.blit(pg.transform.flip(self.images[2],True,False),(self.x-camera[0],self.y-camera[1]))
                else:
                    screen.blit(pg.transform.flip(self.sprite,True,False),(self.x-camera[0],self.y-camera[1]))
            else:
                if self.dead == STOMPED:
                    screen.blit(pg.transform.flip(self.images[3],True,False),(self.x-camera[0],self.y-camera[1]))
                elif self.dead == SLASH:
                    screen.blit(pg.transform.flip(self.images[4],True,False),(self.x-camera[0],self.y-camera[1]))
                elif self.dead == SHOT:
                    screen.blit(pg.transform.flip(self.images[5],True,False),(self.x-camera[0],self.y-camera[1]))
        else:
            if self.dead == ALIVE:
                if self.climb:
                    screen.blit(self.images[2],(self.x-camera[0],self.y-camera[1]))
                else:
                    screen.blit(self.sprite,(self.x-camera[0],self.y-camera[1]))
            else:
                if self.dead == STOMPED:
                    screen.blit(self.images[3],(self.x-camera[0],self.y-camera[1]))
                elif self.dead == SLASH:
                    screen.blit(self.images[4],(self.x-camera[0],self.y-camera[1]))
                elif self.dead == SHOT:
                    screen.blit(self.images[5],(self.x-camera[0],self.y-camera[1]))

    def update(self,fps,saws):           
        if self.speed != 0:
            if self.cont >= fps//5:    
                if self.iindex:
                    self.sprite = self.images[1]
                    self.iindex = not self.iindex
                else:
                    self.sprite = self.images[0]
                    self.iindex = not self.iindex
                self.cont=0
            self.cont +=1
        if self.atack:
            self.atack_test(saws)
            if self.atack_cont == 15:
                self.atack_cont = 0
                self.atack = False
            self.atack_cont +=1
        #print('cd:{} speedy:{}'.format(self.collisions['bottom'],self.speedy))
        #print('{} {} {} {}'.format(self.collisions['top'],self.collisions['bottom'],self.collisions['left'],self.collisions['right']))
        #print('speedx: {} speedy: {}'.format(self.speed,self.speedy))
    def move(self,key,all_collisions,phase):
        self.collisions = {'top':False,'bottom':False,'right':False,'left':False}
        if self.dead == ALIVE:
            if key[pg.K_DOWN]:
                self.swap_state(COWER)
                self.lookto = 'down'
            if key[pg.K_UP]:
                self.lookto = 'up'
            if not key[pg.K_DOWN] and not key[pg.K_UP]:
                self.lookto = ''
            if key[pg.K_RIGHT]:
                self.swap_state(WALK)
                self.flip_sprite = False
                if self.climb_side == -1:
                    self.climb = False
                    self.climb_side = 0
                if self.speed < MAX_SPEED:
                    self.speed += ACCEL
            if key[pg.K_LEFT]:
                self.swap_state(WALK)
                self.flip_sprite = True
                if self.climb_side == 1:
                    self.climb = False
                    self.climb_side = 0
                if self.speed > MAX_SPEED*-1:
                    self.speed -= ACCEL
            if key[pg.K_a]:
                self.y= -2
                self.collision.y = -2
            if key[pg.K_z]:
                if not self.jump:
                    self.speedy = JUMP_FORCE
                    self.jump = True
                    self.climb = False
                    self.climb_side = 0
            if key[pg.K_x]:
                if not self.atack:
                    self.atack = True
        if not key[pg.K_LEFT] and not key[pg.K_RIGHT]:
            self.swap_state(STAND)
            if self.speed < -10:
                self.speed = -10
            elif self.speed < 0:
                self.speed += 0.5
            if self.speed > 10:
                self.speed = 10
            elif self.speed > 0:
                self.speed -= 0.5
        #teste de colisoes
        rect = self.collision
        rect.y += self.speedy
        collist = self.has_collision(rect,all_collisions)
        
        for co in collist:
            if self.speedy > 0:
                self.collision.bottom = co.collision.top
                self.collisions['bottom'] = True
                self.y = self.collision.top - 12

            if self.speedy < 0 :
                self.collision.top = co.collision.bottom
                self.collisions['top'] = True
                self.y = self.collision.top - 12
                self.speedy = 0
        if not self.collisions['bottom'] and not self.climb:
            self.state = FALL
            self.speedy += ACCEL
            self.jump = True
        else:
            if self.speedy >= TERMINAL_SPEED:
                self.dead = STOMPED
            self.speedy = 1
            self.jump = False
        rect = self.collision
        rect.x += self.speed
        collist = self.has_collision(rect,all_collisions)
        for co in collist:
            if self.speed > 0:
                self.collision.right = co.collision.left
                self.collisions['right'] = True
                self.x = self.collision.left
                self.speed = 0
                self.climb_test(co,1,phase)
            if self.speed < 0 :
                self.collision.left = co.collision.right
                #print('cx:{} cy:{} px:{} py:{}'.format(co.x,co.y,self.x,self.y))
                self.collisions['left'] = True
                self.x = self.collision.left
                self.speed = 0
                self.climb_test(co,-1,phase)
                
        if self.climb:
            self.speed = 0
            self.speedy = 0
        #fim do teste de colisoes
        if not self.collisions['right'] or not self.collisions['left']:
            self.x += self.speed
            self.collision.x = self.x
        if not self.collisions['bottom'] or not self.collisions['top']:
            self.y += self.speedy
            self.collision.y = self.y+12            
            
    def has_collision(self,rect,collision_array):
        collide = []
        for colUni in collision_array:
            if colUni.type == 's' or colUni.type == 'ts':
                if colUni.collision is not None:
                    if rect.colliderect(colUni.collision):
                        self.dead = SLASH    
            elif colUni.type == 'b':
                if rect.collidepoint(colUni.point):
                    colUni.collided = True
                    self.dead = SHOT
            else:
                if rect.colliderect(colUni.collision):
                    if colUni.type == 2 or colUni.type == 99:
                        collide.append(colUni)
                    elif colUni.type == 0:
                        self.on_end = True
        return collide
    def climb_test(self,block,side,phase):
        if block.scalable:
            self.climb_side = side

            if block.pos[0] == 0:
                if abs(self.y - block.y) < 10 and not self.collisions['bottom']:
                        self.climb = True
            else:
                if block.pos[1] == 0 and side == 1:
                    if phase[block.pos[0]-1][block.pos[1]][0] == '0':
                        if abs(self.y - block.y) < 10 and not self.collisions['bottom']:
                            self.climb = True
                elif block.pos[1] == len(phase[block.pos[0]])-1:
                    if phase[block.pos[0]-1][block.pos[1]][0] == '0' or phase[block.pos[0]-1][block.pos[1]][0] == '8':
                        if abs(self.y - block.y) < 10 and not self.collisions['bottom']:
                            self.climb = True
                elif (phase[block.pos[0]-1][block.pos[1]][0] == '0' or phase[block.pos[0]-1][block.pos[1]][0] == '8') and (phase[block.pos[0]-1][block.pos[1]-side][0] == '0' or phase[block.pos[0]-1][block.pos[1]][0] == '8'):
                        if abs(self.y - block.y) < 10 and not self.collisions['bottom']:
                            self.climb = True
            if self.climb:
                self.y = block.y-12
                self.collision.y = self.y
    def atack_test(self,collides):
        if not self.flip_sprite:
            self.atack_collision = pg.Rect(self.collision.center[0]+20,self.collision.center[1],20,10)
        else:
            self.atack_collision = pg.Rect(self.collision.center[0]-40,self.collision.center[1],20,10)
        for i in collides:
            if i.type == 's':
                if i.collision is not None:
                    if self.atack_collision.colliderect(i.collision):
                        i.life -= 1

class plataform():
    def __init__(self, phase):
        self.height = 70
        self.width = 70
        self.phase = phase
        self.spawn = None
        self.end = None
        self.x = 140
        self.y = 450
        self.cont = 0
        self.visible = True
        self.things_collide = []
        self.things_draw = []
        self.blocks = []
        self.saws = []
        self.broken_saws = []
        self.canons = []
        self.bullets = []
        #self.collision = pg.Rect(self.x,self.y,self.width,self.height)
    def draw(self,screen,camera):
##        if self.visible:
##            pg.draw.rect(screen,RED,[self.x, self.y, self.width, self.height])
        '''for b in self.blocks:
            #if b.x+70-camera[0] > 0 and b.y+70-camera[1] > 0 or b.x-camera[0] < SCREEN_WIDTH and b.y-camera[1] < SCREEN_HEIGHT:
            if b.type != 0 and b.sprite != None:
                screen.blit(b.sprite,(b.x-camera[0],b.y-camera[1]))
        for s in self.saws:
            s.draw(screen,camera)
        for ca in self.canons:
            ca.draw(screen,camera)
        for bu in self.bullets:
            bu.draw(screen,camera)'''
        for t in self.things_draw:
            t.draw(screen,camera)

##        sp = pg.Rect(self.spawn.x-camera[0],self.spawn.y-camera[1],self.spawn.width,self.spawn.height)
##        pg.draw.rect(screen,REDA,sp)
        ed = pg.Rect(self.end.x-camera[0],(self.end.y)-camera[1],self.end.width,self.end.height)
        pg.draw.rect(screen,REDA,ed)
    def update(self,camera,pos):
        for ca in self.canons:
            ca.update(self.bullets)
        for bu in self.bullets:
            bu.update(self.blocks)
            if bu.collided or self.bullet_collide(bu.side,bu.pos):
                self.bullets.remove(bu)
        for s in self.saws:
            s.update(self.broken_saws)
        for bs in self.broken_saws:
            bs.update(self.things_collide)
        self.collide_draw_update(pos)
    def bullet_collide(self,side,pos):
        if side == 2:
            if  pos[1] < 0 or pos[1] > len(self.phase[pos[0]]):
                return True
            for i in range(pos[1],0,-1):
                if self.phase[pos[0]][i][0] == '9':
                    if pos[1] == i:
                        return True
                    break
        if side == 3:
            if  pos[1] < 0 or pos[1] > len(self.phase[pos[0]]):
                return True
            for i in range(pos[1],len(self.phase[pos[0]])):
                if self.phase[pos[0]][i][0] == '9':
                    if pos[1] == i:
                        return True
                    break
        return False
        
    def collide_draw_update(self,pos):
        self.things_collide = []
        self.things_draw = []
        
        for b in self.blocks:
            if b.pos[1] >= pos[0]-DRAW_DISTANCE_X and b.pos[1] <= pos[0]+DRAW_DISTANCE_X and b.pos[0] <= pos[1]+DRAW_DISTANCE_Y and b.pos[0] >= pos[1]-DRAW_DISTANCE_Y:
                self.things_collide.append(b)
                self.things_draw.append(b)
        for s in self.saws:
            if s.pos[1] >= pos[0]-DRAW_DISTANCE_X and s.pos[1] <= pos[0]+DRAW_DISTANCE_X and s.pos[0] <= pos[1]+DRAW_DISTANCE_Y and s.pos[0] >= pos[1]-DRAW_DISTANCE_Y:
                self.things_collide.append(s)
                self.things_draw.append(s)
        for bs in self.broken_saws:
            if bs.pos[1] >= pos[0]-DRAW_DISTANCE_X and bs.pos[1] <= pos[0]+DRAW_DISTANCE_X and bs.pos[0] <= pos[1]+DRAW_DISTANCE_Y and bs.pos[0] >= pos[1]-DRAW_DISTANCE_Y:
                if bs.can_hurt:
                    self.things_collide.append(bs)
                self.things_draw.append(bs)
        for ca in self.canons:
            if ca.pos[1] >= pos[0]-DRAW_DISTANCE_X and ca.pos[1] <= pos[0]+DRAW_DISTANCE_X and ca.pos[0] <= pos[1]+DRAW_DISTANCE_Y and ca.pos[0] >= pos[1]-DRAW_DISTANCE_Y:
                self.things_draw.append(ca)
        for bu in self.bullets:
            if bu.pos[1] >= pos[0]-DRAW_DISTANCE_X and bu.pos[1] <= pos[0]+DRAW_DISTANCE_X and bu.pos[0] <= pos[1]+DRAW_DISTANCE_Y and bu.pos[0] >= pos[1]-DRAW_DISTANCE_Y:
                self.things_collide.append(bu)
                self.things_draw.append(bu)

    def copy_phase(self):
        cont_x = 0
        cont_y = 0
        for s in self.phase:
            b = None
            cont_x = 0
            for a in s:
                if cont_y == 0:
                    if cont_x == 0:
                        b = block((cont_x,cont_y),BLOCK_SIZE,(cont_y,cont_x),True)
                    else:
                        b = block((cont_x*self.width,cont_y),BLOCK_SIZE,(cont_y,cont_x),True)
                else:
                    if cont_x == 0:
                        b = block((cont_x,cont_y*self.height),BLOCK_SIZE,(cont_y,cont_x),True)
                    else:
                        b = block((cont_x*self.width,cont_y*self.height),BLOCK_SIZE,(cont_y,cont_x),True)
                if a[0] == '9':
                    b.type = 2
                    self.blocks.append(b)
                elif a[0] == '1':
                    self.spawn = b.collision
                elif a[0] == '8':
                    self.end = b.collision
                    b.type = 0
                    self.blocks.append(b)
                elif a[0] == '3':
                    b.type = 3
                    b.set_sprite(pg.image.load(os.path.join('resources\graphics', 'grass.png')))
                    self.blocks.append(b)
                if a[1] == '1':
                    s = saw(b)
                    s.start()
                    self.saws.append(s)
                elif a[1] =='2':
                    if a[3] == '2':
                        ca = canon(2,b)
                        ca.start()
                        self.canons.append(ca)
                    if a[3] == '3':
                        ca = canon(3,b)
                        ca.start()
                        self.canons.append(ca)
                cont_x+=1
            cont_y +=1
        bl = block((0,0),(1600,2),(0,0),False)
        bl.type = 99
        self.blocks.append(bl)
        bl = block((0,598),(800,2),(0,598),False)
        bl.type = 99
        self.blocks.append(bl)
        bl = block((0,0),(2,600),(0,0),False)
        bl.type = 99
        self.blocks.append(bl)
        bl = block((798,0),(2,600),(798,0),False)
        bl.type = 99
        self.blocks.append(bl)
class block(pg.sprite.Sprite):
    def __init__(self, xy, wh, pos,scalable):
        #chama o construtor da classe mãe
        pg.sprite.Sprite.__init__(self)
        self.sprite = pg.image.load(os.path.join('resources\graphics', 'dirt.png'))
        self.scalable = scalable
        self.height = 70
        self.width = 70
        self.type = 2
        self.pos = pos
        self.x = xy[0]
        self.y = xy[1]
        self.collision = pg.Rect(self.x,self.y,self.width,self.height)
    def set_xy(self,xy):
        self.x = xy[0]
        self.y = xy[1]
    def draw(self,screen,camera):
        screen.blit(self.sprite,(self.x-camera[0],self.y-camera[1]))
    def set_sprite(self,sprite):
        self.sprite = sprite
    def update(self,camera):
        pass
    
class saw():
    def __init__(self,block):
        self.x = 0
        self.y = 0
        self.type = 's'
        self.life = 45
        self.deactived = False
        self.pos = (block.pos[0],block.pos[1]-1)
        self.block = block
        self.image = pg.image.load(os.path.join('resources\graphics', 'saw.png'))
        self.collision = pg.Rect(self.x,self.y,55,60)
    def start(self):
        self.collision.center = self.block.collision.center
        self.collision.bottom = self.block.collision.top
        self.x = self.collision.x
        self.y = self.collision.y
    def update(self,bsaws):
        if self.life == 0 and not self.deactived:
            self.deactived = True
            self.deactive(bsaws)
    def draw(self,screen,camera):
        #pg.draw.rect(screen,(255,0,0),self.collision)
        screen.blit(self.image,(self.x-camera[0],self.y-camera[1]))
    def deactive(self,bsaws):
        ts = torn_saw(self)
        ts.throw()
        bsaws.append(ts)
        self.collision = None
        self.image = pg.image.load(os.path.join('resources\graphics', 'broken_saw_holder.png'))
        self.x = self.block.collision.center[0]
        self.y = self.block.collision.top-self.image.get_height()
class torn_saw():
    def __init__(self,saw):
        self.type = 'ts'
        self.pos = [saw.pos[0],saw.pos[1]]
        self.image = pg.image.load(os.path.join('resources\graphics', 'broken_saw.png'))
        self.collision = pg.Rect(saw.collision.x,saw.collision.y,55,54)
        self.collisions = {'top':False,'bottom':False,'right':False,'left':False}
        self.can_hurt = True
        self.flip_sprite = False
        self.speeds = [0,0] 
    def draw(self,screen,camera):
        #pg.draw.rect(screen,(255,40,0),pg.Rect(self.collision.x-camera[0],self.collision.y-camera[1],55,54))
        if self.flip_sprite:
            screen.blit(pg.transform.flip(self.image,True,False),(self.collision.x-camera[0],self.collision.y-camera[1]))
        else:
            screen.blit(self.image,(self.collision.x-camera[0],self.collision.y-camera[1]))
    def update(self,pl):
        if self.can_hurt:
            if self.speeds[0] != 0 and self.speeds[1] != 0 or not self.collisions['bottom']:
                self.collision_test(pl)
            else:
                self.can_hurt = False
            if not self.collisions['bottom']:
                self.speeds[1] +=1.5
        
    def throw(self):
        velx = [-15,15,8,-8,-20,20,25,-25]
        vely = [-15,-4,-25,-35,-30,-40,-45]
        self.speeds[0] = r.choice(velx)
        self.speeds[1] = r.choice(vely)
        if self.speeds[0] < 0:
            self.flip_sprite = True
    def collision_test(self,pl):
        self.collision.x += self.speeds[0]
        for b in pl:
            if b.type == 2 or b.type == 99:
                if self.collision.colliderect(b.collision):

                    if self.speeds[0] > 0 :
                        self.collision.right = b.collision.left
                        self.collisions['right'] = True
                    else:
                        self.collision.left = b.collision.right
                        self.collisions['left'] = True
                    self.speeds[1] = 0
                    self.speeds[0] = 0

        self.collision.y += self.speeds[1]
        for b in pl:
            if b.type == 2 or b.type == 99:
                if self.collision.colliderect(b.collision):
                    if self.speeds[1] > 0 :
                        self.collision.bottom = b.collision.top
                        self.collisions['bottom'] = True
                    else:
                        self.collision.top = b.collision.bottom
                        self.collisions['top'] = True
                    self.speeds[1] = 0
        self.pos[0],self.pos[1] = self.collision.y//70,self.collision.x//70
class canon():
    def __init__(self,side,rect):
        self.x = 0
        self.y = 0
        
        self.pos = rect.pos
        self.side = side
        self.atack_time = 100
        self.image = pg.image.load(os.path.join('resources\graphics', 'canon.png'))
        self.block = rect.collision
    def start(self):
        '''
          1
          _
       2 |_| 3

          4
        '''
        rect = pg.Rect(self.x,self.y,60,35)
        if self.side == 1:
            self.pos = (self.pos[0],self.pos[1]-1)
            rect = pg.Rect(self.x,self.y,35,60)
            rect.center = self.block.center
            self.x = rect.x
            self.y = rect.y-20
            self.image = pg.transform.rotate(self.image,270)
        if self.side == 2:
            self.pos = (self.pos[0]-1,self.pos[1])
            rect.center = self.block.center
            self.x = rect.x-20
            self.y = rect.y
        if self.side == 3:
            self.pos = (self.pos[0]+1,self.pos[1])
            rect.center = self.block.center
            self.x = rect.x+20
            self.y = rect.y
            self.image = pg.transform.rotate(self.image,180)
        if self.side == 4:
            self.pos = (self.pos[0],self.pos[1]+1)
            rect = pg.Rect(self.x,self.y,35,60)
            rect.center = self.block.center
            self.x = rect.x
            self.y = rect.y+20
            self.image = pg.transform.rotate(self.image,90)
        
    def set_xy(self,xy):
        self.x = xy[0]
        self.y = xy[1]
    def update(self,bullets):
        if self.atack_time == 200:
            b = bullet(self)
            b.start()
            bullets.append(b)
            self.atack_time = 0
            
        else:
            self.atack_time +=1
    def draw(self,screen,camera):
        screen.blit(self.image,(self.x-camera[0],self.y-camera[1]))
        
class bullet():
    def __init__(self,canon):
        self.x = 0
        self.y = 0
        self.type = 'b'
        self.pos = [0,0]
        self.canon = canon
        self.side = canon.side
        self.image = pg.image.load(os.path.join('resources\graphics', 'bullet.png'))
        self.collision = pg.Rect(self.x,self.y,7,5)
        self.point = [0,0]
        self.speed = 0
        self.speedy = 0
        self.collided = False
    def set_xy(self,xy):
        self.x = xy[0]
        self.y = xy[1]
    def update(self,pc):
        self.collision.x += self.speed
        self.collision.y += self.speedy
        self.x = self.collision.x
        self.y = self.collision.y
        self.pos[0],self.pos[1] = self.y//70,self.x//70
        if self.side == 1:
            self.point[0],self.point[1] = self.x+3,self.y
        elif self.side == 2:
            self.point[0],self.point[1] = self.x,self.y+3
        elif self.side == 3:
            self.point[0],self.point[1] = self.x+7,self.y+3
        elif self.side == 4:
            self.point[0],self.point[1] = self.x+3,self.y+7

    def draw(self,screen,camera):
        screen.blit(self.image,(self.x-camera[0],self.y-camera[1]))
    def start(self):
        
        '''
          1
          _
       2 |_| 3

          4
        '''
        self.collision = pg.Rect(self.x,self.y,7,5)
        if self.side == 1:
            self.collision = pg.Rect(self.x,self.y,5,7)
            self.x = self.canon.x+16
            self.y = self.canon.y
            self.collision.x = self.x
            self.collision.y = self.y
            self.image = pg.transform.rotate(self.image,270)
            self.speedy = -BULLETSPEED
        elif self.side == 2:
            self.x = self.canon.x
            self.y = self.canon.y+16
            self.collision.x = self.x
            self.collision.y = self.y
            self.speed = -BULLETSPEED
        elif self.side == 3:
            self.x = self.canon.x+60
            self.y = self.canon.y+16
            self.collision.x = self.x
            self.collision.y = self.y
            self.image = pg.transform.rotate(self.image,180)
            self.speed = BULLETSPEED
        elif self.side == 4:
            self.collision = pg.Rect(self.x,self.y,5,7)
            self.x = self.canon.x+16
            self.y = self.canon.y+60
            self.collision.x = self.x
            self.collision.y = self.y
            self.image = pg.transform.rotate(self.image,90)
            self.speedy = BULLETSPEED
class ladder():
    def __init__(self):
        pass
class enemy():
    def __init__(self):
        pass
    
class cell():
    def __init__(self, pos):
        self.pos = pos
        self.hasNear = {'n':False,'s':False,'w':False,'e':False}
        self.n = None
        self.s = None
        self.e = None
        self.w = None
        self.type = '9000'
    def hasNearCells(self,*direction):
        for d in direction:
            self.findCellOn(d)
    def findCellOn(self, direction):
        if direction == 'n':
            if self.pos[1] - 1 >= 0:
                self.hasNear['n'] = True
                return (self.pos[0],self.pos[1]-1)
            else:
                self.hasNear['n'] = False
                return None
        elif direction == 's':
            if self.pos[1] + 1 < 26:
                self.hasNear['s'] = True
                return (self.pos[0],self.pos[1]+1)
            else:
                self.hasNear['s'] = False
                return None
        elif direction == 'w':
            if self.pos[0] - 1 >= 0:
                self.hasNear['w'] = True
                return (self.pos[0]-1,self.pos[1])
            else:
                self.hasNear['w'] = False
                return None
        elif direction == 'e':
            if self.pos[0] + 1 < 64:
                self.hasNear['e'] = True
                return (self.pos[0]+1,self.pos[1])
            else:
                self.hasNear['e'] = False
                return None


        
class phase():
    def __init__(self):
        self.height = 26
        self.width = 64
        self.write = False
        self.matriz = [[cell((x,y)) for x in range(self.width)] for y in range(self.height)]
        self.matrizvisual =  [[0 for x in range(self.width)] for y in range(self.height)]
        self.exit = ((random.randrange(1,63),random.randrange(21,24)))
        self.spawn = ((random.randrange(2,62),random.randrange(1,4)))
        self.lastDirection = None
        self.path = []
        self.firstDirection = None
    def set_write(self, is_writing):
        self.write = is_writing
    def findCellByPosition(self,position):
        if position is not None:
            return self.matriz[position[1]][position[0]]
        else:
            return None
  
    def setNearCells(self):
        for lista in self.matriz:
            for cell in lista:
                cell.n = self.findCellByPosition(cell.findCellOn('n'))
                cell.w = self.findCellByPosition(cell.findCellOn('w'))
                cell.s = self.findCellByPosition(cell.findCellOn('s'))
                cell.e = self.findCellByPosition(cell.findCellOn('e'))
                self.updateCell(cell)
    def setCellType(self,cell,tipe):
        cell.type = tipe
        self.updateCell(cell)
    def updateCell(self,cell):
        self.matriz[cell.pos[1]][cell.pos[0]] = cell
    def doIt(self):
        self.path = []
        self.firstDirection = None
        start = self.findCellByPosition(self.spawn)
        end = self.findCellByPosition(self.exit)
        self.random_path(start,end,True)
        self.random_path(start,end,True)
        for i in range(1,15):
            start = (random.randrange(2,63), random.randrange(1+i,23))
            end = (random.randrange(1,63),random.randrange(start[1],24))
            self.random_path(self.findCellByPosition(start),self.findCellByPosition(end),False)
        #print()
        self.post_processing() 
        return self.write_phase()
    def random_path(self,start,end,is_initial):
        aux = start
        path = []
        randchoice = None
        self.lastDirection = None
        done = False
        possibleNear = []
        cont = 0
        aux1 = None
        while not done:
            aux1 = aux
            if aux is not start:
                possibleNear = []
                if aux.hasNear['w'] is True and self.lastDirection != 'e':
                    if aux.w.hasNear['w']:
                        if aux.pos[1] < end.pos[1]:
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                        elif aux.pos[1] == end.pos[1] and aux.pos[0] > end.pos[0]:
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                if aux.hasNear['e'] is True and self.lastDirection != 'w':
                    if aux.e.hasNear['e']:
                        if aux.pos[1] < end.pos[1]:
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                        elif aux.pos[1] == end.pos[1] and aux.pos[0] < end.pos[0]:
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                if aux.hasNear['s'] is True and self.lastDirection !='s':
                    if aux.pos[1] < end.pos[1]:
                        possibleNear.append(aux.s)
##                if len(possibleNear) == 0:
##                    print('a: {} s: {} e: {}'.format(start.pos,aux.pos,end.pos))
                randchoice = random.choice(possibleNear)              
            elif aux is start:
                if is_initial:
                    self.setCellType(aux,'1000')
                    if aux.hasNear['w'] == True and aux.w is not self.firstDirection:
                        possibleNear.append(aux.w)
                    if aux.hasNear['e'] == True and aux.e is not self.firstDirection:
                        possibleNear.append(aux.e)
                    randchoice = random.choice(possibleNear)
                    self.firstDirection  = randchoice
                else:
                    if aux.type == '9000':
                        self.setCellType(aux,'0000')
                    if start.pos[1] != end.pos[1]:
                        if aux.hasNear['w'] == True and aux.w.type != '0000':
                            possibleNear.append(aux.w)
                        if aux.hasNear['e'] == True and aux.e.type != '0000':
                            possibleNear.append(aux.e)
                        if aux.hasNear['s'] == True and aux.s.type != '0000':
                            possibleNear.append(aux.s)

                    else:
                        if aux.hasNear['w'] == True and end.pos[0] < aux.pos[0]:
                            possibleNear.append(aux.w)
                        if aux.hasNear['e'] == True and end.pos[0] > aux.pos[0]:
                            possibleNear.append(aux.e)
                    if len(possibleNear) > 0:
                        randchoice = random.choice(possibleNear)
                    else:
                        done = True
                        break
            self.setCellType(randchoice,'0000')
            
            if randchoice is aux.s:
                if randchoice.hasNear['s'] is True and randchoice.s.pos[1] < end.pos[1]:
                    self.setCellType(randchoice.s,'0000')
                    randchoice = randchoice.s
                    if randchoice.hasNear['s'] is True and randchoice.s.pos[1] < end.pos[1]:
                        self.setCellType(randchoice.s,'0000')
                        aux = randchoice.s
            self.lastDirection = 'e' if randchoice is aux.e else 'w' if randchoice is aux.w else 's' if randchoice is aux.s else ''
            if aux is aux1 or aux1 == None:
                aux = randchoice
            if is_initial:
                path.append(aux.pos)
            if aux is end or aux.e is end or aux.s is end or aux.w is end:
                if is_initial:
                    self.setCellType(end,'8000')
                else:
                    self.setCellType(end,'0000')
                if is_initial:
                    self.path.append(path)
                done = True   
            
        
    def reDoIt(self):
        self.exit = ((random.randrange(1,63),random.randrange(21,24)))
        self.spawn = ((random.randrange(2,63),random.randrange(1,4)))
        self.doIt()
    def verify_path(self):
        aux = []
        aux3 = []
        aux.append(self.findCellByPosition(self.spawn))
        while len(aux) != 0:
            aux2 = []
            for cell in aux:
                #print('{} | {}'.format(cell.pos,cell.type))
                if cell.type == '8000':
                    return True
                else:
                    aux3.append(cell)
                    if  cell.hasNear['e']:
                        if cell.e.type != '9000' and cell.e.type != '1000' and not cell.e in aux3:
                            aux2.append(cell.e)
                    if  cell.hasNear['w']:
                        if cell.w.type != '9000' and cell.w.type != '1000' and not cell.w in aux3:
                            aux2.append(cell.w)
                    if  cell.hasNear['s']:
                        if cell.s.type != '9000' and cell.s.type != '1000' and not cell.s in aux3:
                            aux2.append(cell.s)
                    aux.remove(cell)
            for c in aux2:
                aux.append(c)
        return False
    def get_cells_without_traps(self):
        cwt = []
        aux = None
        for list_ in self.path:
            for pos in list_:
                if aux == None:
                    aux = pos
                elif pos[1] != aux[1]:
                    cwt.append(pos)
                    aux = pos
        return cwt
    def post_processing(self):
        self.vertically_widen()
        self.setCellType(self.findCellByPosition(self.spawn),'1000')
        self.setCellType(self.findCellByPosition(self.exit),'8000')
        self.setCellType(self.findCellByPosition((self.spawn[0],self.spawn[1]+1)),'9000')
        self.setCellType(self.findCellByPosition((self.exit[0],self.exit[1]+1)),'9000')
        if not self.verify_path():
            self.reDoIt()
        self.set_traps()
    def set_traps(self):
        spaces = 0
        cells = []
        cellsDown = []
        cannotcells = self.get_cells_without_traps()
        for list_ in self.matriz:
            for cell in list_:
                if cell.type[0] == '0':
                    if cell.hasNear['w']:
                        if cell.w.type[0] == '9':
                            cells.append(cell.w)
                    if cell.hasNear['e']:
                        if cell.e.type[0] == '9':
                            cells.append(cell.e)
                    if cell.s.type[0] == '9':
                        if cell.pos[0] < self.spawn[0]-5 and cell.pos[0] >self.spawn[0]+5:
                            cellsDown.append(cell.s)
                        elif cell.pos[1] != self.spawn[1]:
                            cellsDown.append(cell.s)
                    spaces += 1
        traps = spaces//20
        rand = None
        can = True
        if len(cellsDown) > 0:
            for i in range(0,traps):
                rand = random.choice(cellsDown)
                if rand.hasNear['n']:
                    if rand.n.hasNear['n']:                    
                        if rand.n.n.type[0] == '0':
                            for pos in cannotcells:
                                if pos[1]+1 == rand.pos[1] and pos[0] == rand.pos[0]:
                                    can = False
                    else:
                        can = False
                    if can:
                        if rand.hasNear['e']:
                            if rand.e.type[1] == '0':
                                rand.type = self.format_cell_type(rand.type,'1',1)
                            else:
                                if rand.e.hasNear['e']:
                                    if rand.e.e.type[1] != '1':
                                        rand.type = self.format_cell_type(rand.type,'1',1)
                                else:
                                    rand.type = self.format_cell_type(rand.type,'1',1)
                        elif rand.hasNear['w']:
                            if rand.w.type[1] == '1':
                                if rand.w.hasNear['w']:
                                    if rand.w.w.type[1] != '1':
                                        rand.type = self.format_cell_type(rand.type,'1',1)
                                else:
                                    rand.type = self.format_cell_type(rand.type,'1',1)
                            else:
                                rand.type = self.format_cell_type(rand.type,'1',1)
                cellsDown.remove(rand)
                can = True
                if len(cellsDown) == 0:
                    break


        if len(cells) > 0:
            for i in range(0,traps):
                rand = random.choice(cells)
                rand.type = self.format_cell_type(rand.type,'2',1)
                if rand.hasNear['n']:
                    if rand.n.type[1] != 2:
                        if rand.hasNear['e']:
                            if rand.e.type[0] =='0':
                                rand.type = self.format_cell_type(rand.type,'3',3)
                        if rand.hasNear['w']:
                            if rand.w.type[0] =='0':
                                rand.type = self.format_cell_type(rand.type,'2',3)
                cells.remove(rand)
                if len(cells) == 0:
                    break
    def format_cell_type(self,type_,type_to_add,where):
        aux = list(type_)
        aux[where] = type_to_add
        return ''.join(aux)
    def vertically_widen(self):
        self.setNearCells()
        for list_ in self.matriz:
            for cell in list_:
                if cell.type == '0000' and cell.hasNear['n'] or cell.type == '8000' and cell.hasNear['n'] or cell.type == '1000' and cell.hasNear['n']:
                    if cell.n.hasNear['n']:
                        if cell.n.type == '9000' and cell.n.n.type != '0000':
                            self.setCellType(cell.n,'0000')

    def write_phase(self):
        text_complete = ''
        contador = 0
        for cont in range(0,26):
            for contItem in range(0,64):
                self.matrizvisual[cont][contItem] = self.matriz[cont][contItem].type
        if self.write:#praticamente inutil    
            text_file = open("data\components\saida.txt", "w")
            for i in self.matrizvisual:
                text = '{}\n'.format(i)
                text = text.replace('[','')
                text = text.replace(']','')
                text = text.replace(', ','')
                text_complete += text
                
                text_file.write(text)
            text_file.close()
        return self.matrizvisual
            
    def read_phase(self):#legancy -NÃO UTILIZAR-
        file = open("saida.txt", "r")
        text = file.read()
        file.close()    
        phase = []
        for row in text:
            phase.append(row)
        return phase
    
class Control(object):
    def __init__(self, caption):
        self.screen = pg.Surface(DISPLAY_SIZE)
        self.display = pg.display.get_surface()
        self.done = False
        self.camera = [0,0]
        self.clock = pg.time.Clock()
        self.phasetime = None 
        self.caption = caption
        self.fps = FPS
        self.show_fps = True
        #self.current_time = 0.0
        self.keys = pg.key.get_pressed()
        #self.state_dict = {}
        self.new = False
        #self.state_name = None
        self.first_load = True
        self.state = MENU
        self.player = player()
        self.phase = phase()
        self.plataform = None
        self.menu = menu()
        self.pause = pause()
        self.loading = load_screen()
        self.config = config()
        self.credits = creditz()
        self.hud = hud()
        self.debug = False
    def update(self):
        if self.debug:
            print('update: atualiza o q vai ser na tela')
        if self.state == PLAY:
            self.player.update(self.clock.get_fps(),self.plataform.things_collide)
            self.plataform.update(self.camera,(self.player.x//70,self.player.y//70))
            self.cameramove()
            self.screen.get_rect().move
        self.draw()
        self.state_update()
    def draw(self):
        if self.debug:
            print('draw: atualiza o q esta na tela')
        if self.state != PLAY:
            self.screen.fill(BGCOLOR)
        else:
            self.screen.fill(BGCOLORP)
        if self.state == PLAY:
            self.player.draw(self.screen,self.camera)
            self.plataform.draw(self.screen,self.camera)
            self.hud.draw(self.screen,(self.player.x//70,self.player.y//70),(self.plataform.end.x//1,self.plataform.end.y//1),self.player.dead)
        elif self.state == MENU:
            self.menu.draw(self.screen)
        elif self.state == PAUSE:
            self.pause.draw(self.screen)
        elif self.state == LOAD:
            self.loading.draw(self.screen)
        elif self.state == CONFIG:
            self.config.draw(self.screen)
        elif self.state == IMPIKA:
            self.credits.draw(self.screen)
        self.display.blit(pg.transform.scale(self.screen,self.display.get_size()),(0,0))
        pg.display.update()
    
    def cameramove(self):  
        self.camera[0] += (self.player.x-self.camera[0]-DISPLAY_WIDTH/2)/2
        if self.player.lookto == 'up':
            self.camera[1] += (self.player.y-120-self.camera[1]-DISPLAY_HEIGHT/2)/2
        elif self.player.lookto == 'down':
            self.camera[1] += (self.player.y+120-self.camera[1]-DISPLAY_HEIGHT/2)/2
        else:
            self.camera[1] += (self.player.y-self.camera[1]-DISPLAY_HEIGHT/2)/2
        if self.player.on_end or self.new:
            self.camera[0] += (self.player.x-self.camera[0]-DISPLAY_WIDTH/2)
            self.camera[1] += (self.player.y-self.camera[1]-DISPLAY_HEIGHT/2)
    def event_loop(self):
        if self.state == PLAY:
            self.player.move(pg.key.get_pressed(),self.plataform.things_collide,self.plataform.phase)
        elif self.state == MENU:
            mp = []
            p = pg.mouse.get_pos()
            mp.append(p[0])#//2)
            mp.append(p[1])#//2)
            self.menu.event((mp,pg.mouse.get_pressed()),pg.key.get_pressed())
        elif self.state == PAUSE:
            mp = []
            p = pg.mouse.get_pos()
            mp.append(p[0])#//2)
            mp.append(p[1])#//2)
            self.pause.event((mp,pg.mouse.get_pressed()),pg.key.get_pressed())
        elif self.state == CONFIG:
            mp = []
            p = pg.mouse.get_pos()
            mp.append(p[0])#//2)
            mp.append(p[1])#//2)
            self.config.event((mp,pg.mouse.get_pressed()),pg.key.get_pressed())
        elif self.state == IMPIKA:
            mp = []
            p = pg.mouse.get_pos()
            mp.append(p[0])#//2)
            mp.append(p[1])#//2)
            self.credits.event((mp,pg.mouse.get_pressed()),pg.key.get_pressed())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.restart()
                if event.key == pg.K_ESCAPE:
                    if self.state == PLAY:
                        self.state = PAUSE
                    elif self.state == PAUSE:
                        self.state = PLAY
            if event.type == pg.VIDEORESIZE:
            # There's some code to add back window content here.
                self.display = pg.display.set_mode((event.w, event.h),pg.RESIZABLE)
                new_size = [self.display.get_size()[0]/2,self.display.get_size()[1]/2]
                #self.screen  = pg.Surface(new_size)
                DISPLAY_WIDTH = new_size[0]
                DISPLAY_HEIGHT = new_size[1]
                self.menu.start()
                self.pause.start()
                self.loading.start()
                self.credits.start()
                self.config.start()
                
    def next_phase(self):
        if self.player.on_end and self.state == PLAY or self.new:
            self.new = False
            stt = self.state
            self.state = LOAD
            self.draw()
            self.clock.tick(5000)
            self.phase = phase()
            self.phase.setNearCells()
            self.plataform = plataform(self.phase.doIt())
            self.plataform.copy_phase()
            self.player.set_spawn(self.plataform.spawn)
            self.cameramove()
            self.player.on_end = False
            self.state = stt

    def state_update(self):
        if self.state == MENU:
            if self.menu.go_to is not None:
                if self.menu.go_to is CLOSE:
                    self.done = True
                else:
                    self.state = self.menu.go_to
                    if self.state == PLAY:
                        self.new = True
                    if self.state == CONFIG:
                        self.config.set_from(MENU)
                    self.menu.reset()
        elif self.state == PAUSE:
            if self.pause.go_to is not None:
                if self.pause.go_to is CLOSE:
                    self.done = True
                else:
                    self.state = self.pause.go_to
                    self.pause.go_to = None
                    if self.state == CONFIG:
                        self.config.set_from(PAUSE)
                self.pause.reset()
        elif self.state == CONFIG:
            if self.config.go_to is not None:
                self.state = self.config.go_to
                self.config.go_to = None
                self.config.reset()
        elif self.state == IMPIKA:
            if self.credits.go_to is not None:
                self.state = self.credits.go_to
                self.credits.go_to = None
                self.credits.reset()
    def restart(self):
        self.player.set_spawn(self.plataform.spawn)
    def main(self):
        self.menu.start()
        self.pause.start()
        self.loading.start()
        self.credits.start()
        self.config.start()
        while not self.done:
            if self.first_load and self.state == PLAY:
                self.next_phase()
            self.event_loop()
            self.update()
            self.clock.tick(self.fps)
            self.next_phase()
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = '{} - {:.2f} FPS'.format(self.caption,fps)
                pg.display.set_caption(with_fps)

main = Control('Jaame')
main.main()
pg.quit()
