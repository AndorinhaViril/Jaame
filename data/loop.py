'''
controla o que deve e quando será processado/executado
'''
__author__ = "AnddorinhaViril"
import random as r
import pygame as pg
import os
import time
import data.menu as m
import data.animation as a
from data.engine import player, plataform
import data.constants as c
from data.components import phasegenerator as phg

class Control(object):
    def __init__(self, caption):
        c.load_configs()
        try:
            pg.mixer.pre_init(44100, 16, 2, 4096)
            pg.init()
        except:
            print('Falhou a inicialização do modulo principal')
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.display.set_icon(pg.image.load(os.path.join('resources\\graphics','player.png')))
        self.screen = pg.Surface(c.SCREEN_SIZE)
        self.display = pg.display.set_mode(c.DISPLAY_SIZE,pg.RESIZABLE)
        self.done = False
        self.camera = [0,0]
        self.clock = pg.time.Clock()
        self.phasetime = None 
        self.caption = caption
        self.fps = c.FPS
        self.show_fps = True
        #self.current_time = 0.0
        self.keys = pg.key.get_pressed()
        #self.state_dict = {}
        self.new = False
        #self.state_name = None
        self.first_load = True
        self.state = c.MENU
        self.timer = None
        self.player = player()
        self.phase = phg.phase()
        self.animation = a.animation()
        self.plataform = None
        self.menu = m.inicial()
        self.pause = m.pause()
        self.loading = m.load_screen()
        self.loadphase = m.load_phase()
        self.savephase = m.save_phase()
        self.config = m.config()
        self.credits = m.credits()
        self.hud = m.hud()
        self.debug = False
    def update(self):
        if self.debug:
            print('update: atualiza o q vai ser na tela')
        if self.state == c.PLAY:
            self.player.update(self.clock.get_fps(),self.plataform.things_collide)
            self.plataform.update(self.camera,self.player.collision.center,self.player.dead==c.ALIVE)
            self.cameramove()
            #self.screen.get_rect().move
        self.draw()
        self.state_update()
    def draw(self):
        if self.debug:
            print('draw: atualiza o q esta na tela')
        if self.state != c.PLAY:
            self.screen.fill(c.BGCOLOR)
        else:
            self.screen.fill(c.BGCOLORP)
            #self.screen.blit(pg.transform.scale(pg.image.load(os.path.join('resources\graphics', 'dirt.png')),(854,480)),(0,0))
        if self.state == c.PLAY:
            self.player.draw(self.screen,self.camera)
            self.plataform.draw(self.screen,self.camera)
            self.hud.draw(self.screen,(self.player.x//70,self.player.y//70),(self.plataform.end.x//1,self.plataform.end.y//1),self.player.dead,self.player.num_death,(self.timer-time.time()))
        elif self.state == c.MENU:
            self.menu.draw(self.screen)
            self.animation.menu(self.screen,self.get_mouse_pos(),self.clock.get_fps())
        elif self.state == c.PAUSE:
            self.pause.draw(self.screen)
        elif self.state == c.LPHASE:
            self.loadphase.draw(self.screen)
        elif self.state == c.SPHASE:
            self.savephase.draw(self.screen)
        elif self.state == c.LOAD:
            self.loading.draw(self.screen)
        elif self.state == c.CONFIG:
            self.config.draw(self.screen)
        elif self.state == c.IMPIKA:
            self.credits.draw(self.screen)
        #self.display.blit(pg.transform.scale2x(self.screen),(0,0))
        if self.screen.get_size() != self.display.get_size():
            self.display.blit(pg.transform.scale(self.screen,self.display.get_size()),(0,0))
        else:
            self.display.blit(self.screen,(0,0))
        pg.display.update()
    
    def cameramove(self):  
        if self.screen.get_size()[0] > self.display.get_size()[0]:
            display_x = (c.DISPLAY_WIDTH+(c.SCREEN_WIDTH/2)/2)
            display_y = (c.DISPLAY_HEIGHT+(c.SCREEN_HEIGHT/2)/2)
        else:
            display_x = c.SCREEN_WIDTH/2
            display_y = c.SCREEN_HEIGHT/2
        self.camera[0] += (self.player.x-self.camera[0]-display_x)/2
        if self.player.lookto == 'up':
            self.camera[1] += (self.player.y-190-self.camera[1]-display_y)/2
        elif self.player.lookto == 'down':
            self.camera[1] += (self.player.y+210-self.camera[1]-display_y)/2
        else:
            self.camera[1] += (self.player.y-self.camera[1]-display_y)/2
        if self.player.on_end or self.new:
            self.camera[0] += (self.player.x-self.camera[0]-display_x)
            self.camera[1] += (self.player.y-self.camera[1]-display_y)
    def get_mouse_pos(self):
        mp = []
        p = pg.mouse.get_pos()
        if c.SCREEN_ZOOM == 1:
            mp.append(p[0])
            mp.append(p[1])
        else:
            mp.append(p[0]*c.SCREEN_ZOOM)
            mp.append(p[1]*c.SCREEN_ZOOM)
        return mp
    def event_loop(self):
        if self.state == c.PLAY:
            self.player.move(pg.key.get_pressed(),self.plataform.things_collide,self.plataform.phase)
        elif self.state == c.MENU:
            self.menu.event((self.get_mouse_pos(),pg.mouse.get_pressed()),pg.key.get_pressed())
        elif self.state == c.PAUSE:
            self.pause.event((self.get_mouse_pos(),pg.mouse.get_pressed()),pg.key.get_pressed())
        elif self.state == c.LPHASE:
            self.loadphase.event((self.get_mouse_pos(),pg.mouse.get_pressed()),pg.key.get_pressed())
        elif self.state == c.SPHASE:
            self.savephase.event((self.get_mouse_pos(),pg.mouse.get_pressed()),pg.key.get_pressed())
        elif self.state == c.CONFIG:
            self.config.event((self.get_mouse_pos(),pg.mouse.get_pressed()),pg.key.get_pressed())
        elif self.state == c.IMPIKA:
            self.credits.event((self.get_mouse_pos(),pg.mouse.get_pressed()),pg.key.get_pressed())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.restart()
                if event.key == pg.K_t:#apenas para testes
                    self.player.set_xy((self.plataform.end.x-70,self.plataform.end.y))
                if event.key == pg.K_ESCAPE:
                    if self.state == c.PLAY:
                        self.state = c.PAUSE
                    elif self.state == c.PAUSE:
                        self.state = c.PLAY
            if event.type == pg.VIDEORESIZE:
                self.display = pg.display.set_mode((event.w,event.h),pg.RESIZABLE)
                self.resize_screen()
    def resize_screen(self):
        if c.SCREEN_ZOOM == 1:
            new_size = [self.display.get_size()[0],self.display.get_size()[1]]
        else:
            new_size = [self.display.get_size()[0]*c.SCREEN_ZOOM,self.display.get_size()[1]*c.SCREEN_ZOOM]
        c.SCREEN_WIDTH = new_size[0]
        c.SCREEN_HEIGHT = new_size[1]
        c.DISPLAY_SIZE = (self.display.get_size()[0],self.display.get_size()[1])
        c.SCREEN_SIZE = (c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        self.screen = pg.Surface(c.SCREEN_SIZE)
        self.screen  = pg.Surface(new_size)
        self.menu.start()
        self.pause.start()
        self.loading.start()
        self.credits.start()
        self.config.start()
        self.loadphase.start()
        self.savephase.start()
    def next_phase(self):
        if self.player.on_end and self.state == c.PLAY or self.new:
            if not self.new:
                som = pg.mixer.Sound(os.path.join('resources\\musics','win.wav'))
                som.play()
                if c.SAVE_COMPLETED_PHASES and self.loadphase.to_load == None:
                    self.phase.write_phase()
            self.new = False
            stt = self.state
            self.state = c.LOAD
            self.draw()
            self.phase = phg.phase()
            if self.loadphase.to_load == None:
                self.phase.setNearCells()
            
                self.plataform = plataform(self.phase.doIt())
            else:
                self.plataform = plataform(self.phase.read_phase(self.loadphase.to_load))
                self.loadphase.to_load = None
            self.plataform.copy_phase()
            self.player.set_spawn(self.plataform.spawn)
            self.cameramove()
            self.player.on_end = False
            self.player.num_death = 0
            self.state = stt
            self.timer = time.time()

    def state_update(self):
        if self.state == c.MENU:
            if self.menu.go_to is not None:
                if self.menu.go_to is c.CLOSE:
                    self.done = True
                else:
                    self.state = self.menu.go_to
                    if self.state == c.PLAY:
                        self.new = True
                    if self.state == c.CONFIG:
                        self.config.set_from(c.MENU)
                    self.menu.reset()
        elif self.state == c.PAUSE:
            if self.pause.go_to is not None:
                if self.pause.go_to is c.CLOSE:
                    self.done = True
                else:
                    self.state = self.pause.go_to
                    self.pause.go_to = None
                    if self.state == c.CONFIG:
                        self.config.set_from(c.PAUSE)
                self.pause.reset()
        elif self.state == c.SPHASE:
            if self.savephase.go_to is not None:
                if self.savephase.go_to is c.CLOSE:
                    self.done = True
                else:
                    if self.savephase.save:
                        self.phase.write_phase()
                        self.savephase.save = False
                    self.state = self.savephase.go_to
                    self.savephase.go_to = None
                self.savephase.reset()
        elif self.state == c.LPHASE:
            if self.loadphase.go_to is not None:
                if self.loadphase.go_to is c.CLOSE:
                    self.done = True
                else:
                    if self.loadphase.to_load is not None:
                        self.new = True
                    self.state = self.loadphase.go_to
                    self.loadphase.go_to = None
                self.loadphase.reset()
        elif self.state == c.CONFIG:
            if self.config.go_to is not None:
                if self.config.zoom != c.SCREEN_ZOOM:
                    #print(f'resize new: {self.config.zoom} old: {c.SCREEN_ZOOM}')
                    c.SCREEN_ZOOM = self.config.zoom
                    self.resize_screen()
                self.state = self.config.go_to
                self.config.reset()
                c.save_configs()
        elif self.state == c.IMPIKA:
            if self.credits.go_to is not None:
                self.state = self.credits.go_to
                self.credits.go_to = None
                self.credits.reset()
    def restart(self):
        self.player.set_spawn(self.plataform.spawn)
    def main(self):
        pg.mixer.init()
        self.animation.load_sprites()
        self.menu.start()
        self.pause.start()
        self.loading.start()
        self.credits.start()
        self.config.start()
        self.loadphase.start()
        self.savephase.start()
        while not self.done:
            if self.first_load and self.state == c.PLAY:
                self.next_phase()
            self.event_loop()
            self.update()
            self.clock.tick(self.fps)
            self.next_phase()
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = '{} - {:.2f} FPS'.format(self.caption,fps)
                pg.display.set_caption(with_fps)
        pg.quit()
