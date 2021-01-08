'''
controla o que deve e quando será processado/executado
'''
__author__ = "AnddorinhaViril"
import random as r
import data.setup
import os
import data.menu as m
from data.engine import *
import data.constants as c
from data.components import phasegenerator as phg

class Control(object):
    def __init__(self, caption):
        self.screen = pg.Surface(c.DISPLAY_SIZE)
        self.display = pg.display.get_surface()
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
        self.player = player()
        self.phase = phg.phase()
        self.plataform = None
        self.menu = m.menu()
        self.pause = m.pause()
        self.loading = m.load_screen()
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
        if self.state == c.PLAY:
            self.player.draw(self.screen,self.camera)
            self.plataform.draw(self.screen,self.camera)
            self.hud.draw(self.screen,(self.player.x//70,self.player.y//70),(self.plataform.end.x//1,self.plataform.end.y//1),self.player.dead)
        elif self.state == c.MENU:
            self.menu.draw(self.screen)
        elif self.state == c.PAUSE:
            self.pause.draw(self.screen)
        elif self.state == c.LOAD:
            self.loading.draw(self.screen)
        elif self.state == c.CONFIG:
            self.config.draw(self.screen)
        elif self.state == c.IMPIKA:
            self.credits.draw(self.screen)
        self.display.blit(pg.transform.scale(self.screen,self.display.get_size()),(0,0))
        pg.display.update()
    
    def cameramove(self):  
        self.camera[0] += (self.player.x-self.camera[0]-c.DISPLAY_WIDTH/2)/2
        if self.player.lookto == 'up':
            self.camera[1] += (self.player.y-190-self.camera[1]-c.DISPLAY_HEIGHT/2)/2
        elif self.player.lookto == 'down':
            self.camera[1] += (self.player.y+210-self.camera[1]-c.DISPLAY_HEIGHT/2)/2
        else:
            self.camera[1] += (self.player.y-self.camera[1]-c.DISPLAY_HEIGHT/2)/2
        if self.player.on_end or self.new:
            self.camera[0] += (self.player.x-self.camera[0]-c.DISPLAY_WIDTH/2)
            self.camera[1] += (self.player.y-self.camera[1]-c.DISPLAY_HEIGHT/2)
    def event_loop(self):
        if self.state == c.PLAY:
            self.player.move(pg.key.get_pressed(),self.plataform.things_collide,self.plataform.phase)
        elif self.state == c.MENU:
            mp = []
            p = pg.mouse.get_pos()
            mp.append(p[0])#//2)
            mp.append(p[1])#//2)
            self.menu.event((mp,pg.mouse.get_pressed()),pg.key.get_pressed())
        elif self.state == c.PAUSE:
            mp = []
            p = pg.mouse.get_pos()
            mp.append(p[0])#//2)
            mp.append(p[1])#//2)
            self.pause.event((mp,pg.mouse.get_pressed()),pg.key.get_pressed())
        elif self.state == c.CONFIG:
            mp = []
            p = pg.mouse.get_pos()
            mp.append(p[0])#//2)
            mp.append(p[1])#//2)
            self.config.event((mp,pg.mouse.get_pressed()),pg.key.get_pressed())
        elif self.state == c.IMPIKA:
            mp = []
            p = pg.mouse.get_pos()
            mp.append(p[0])#//2)
            mp.append(p[1])#//2)
            self.credits.event((mp,pg.mouse.get_pressed()),pg.key.get_pressed())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:#apenas para fim de testes
                    self.restart()
                if event.key == pg.K_ESCAPE:
                    if self.state == c.PLAY:
                        self.state = c.PAUSE
                    elif self.state == c.PAUSE:
                        self.state = c.PLAY
            if event.type == pg.VIDEORESIZE:
            # There's some code to add back window content here.
                self.display = pg.display.set_mode((event.w, event.h),pg.RESIZABLE)
                new_size = [self.display.get_size()[0]/2,self.display.get_size()[1]/2]
                c.SCREEN_WIDTH = self.display.get_size()[0]
                c.SCREEN_HEIGHT = self.display.get_size()[1]
                
##                self.screen  = pg.Surface(new_size)
##                c.DISPLAY_WIDTH = new_size[0]
##                c.DISPLAY_HEIGHT = new_size[1]
                self.menu.start()
                self.pause.start()
                self.loading.start()
                self.credits.start()
                self.config.start()
                
    def next_phase(self):
        if self.player.on_end and self.state == c.PLAY or self.new:
            if not self.new:
                som = pg.mixer.Sound('resources\musics\win.ogg')
                som.play()
            self.new = False
            stt = self.state
            self.state = c.LOAD
            self.draw()
            self.clock.tick(5000)
            self.phase = phg.phase()
            self.phase.setNearCells()
            self.plataform = plataform(self.phase.doIt())
            self.plataform.copy_phase()
            self.player.set_spawn(self.plataform.spawn)
            self.cameramove()
            self.player.on_end = False
            self.state = stt

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
        elif self.state == c.CONFIG:
            if self.config.go_to is not None:
                self.state = self.config.go_to
                self.config.go_to = None
                self.config.reset()
        elif self.state == c.IMPIKA:
            if self.credits.go_to is not None:
                self.state = self.credits.go_to
                self.credits.go_to = None
                self.credits.reset()
    def restart(self):
        self.player.set_spawn(self.plataform.spawn)
    def main(self):
        pg.mixer.init()
        self.menu.start()
        self.pause.start()
        self.loading.start()
        self.credits.start()
        self.config.start()
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
