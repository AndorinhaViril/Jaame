import pygame as pg
import data.constants as c
import os
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
                item = self.font_text.render(self.itens[i],True,c.BLACK)
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
        title = self.font_text.render("JAAME", True, c.BLACK)
        self.title = title
        cont = 0
        for i in self.itens:
            itens = self.font_text.render(i,True,c.WHITE)
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
                    self.go_to = c.PLAY
                if self.selected_item == self.itens_tela[1]:
                    self.go_to = c.CONFIG
                if self.selected_item == self.itens_tela[2]:
                    self.go_to = c.IMPIKA
                if self.selected_item == self.itens_tela[3]:
                    self.go_to = c.CLOSE
        pos = mouse[0]
        for i in range(0,len(self.itens_tela)):
            if self.itens_rect[i].collidepoint(mouse[0]):
                self.selected_item = self.itens_tela[i]
                if mouse[1][0]:
                    if self.selected_item is not None:
                        if self.selected_item == self.itens_tela[0]:
                            self.go_to = c.PLAY
                        if self.selected_item == self.itens_tela[1]:
                            self.go_to = c.CONFIG
                        if self.selected_item == self.itens_tela[2]:
                            self.go_to = c.IMPIKA
                        if self.selected_item == self.itens_tela[3]:
                            self.go_to = c.CLOSE

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
                item = self.font_text.render(self.itens[i],True,c.BLACK)
                screen.blit(item,((c.DISPLAY_WIDTH/2)-self.itens_tela[i].get_width()/2+2,(c.DISPLAY_HEIGHT/3)-self.itens_tela[i].get_height()+cont+2))
            screen.blit(self.itens_tela[i],((c.DISPLAY_WIDTH/2)-self.itens_tela[i].get_width()/2,(c.DISPLAY_HEIGHT/3)-self.itens_tela[i].get_height()+cont))
            
            cont+=30
    def start(self):
        self.itens_tela = []
        self.itens_rect = []
        self.selected_item = None
        self.select_index = -1
        cont = 0
        for i in self.itens:
            item = self.font_text.render(i,True,c.WHITE)
            self.itens_tela.append(item)
            rect = item.get_rect()
            rect.left = (c.DISPLAY_WIDTH/2)-item.get_width()/2
            rect.top = (c.DISPLAY_HEIGHT/3)-item.get_height()+cont
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
                    self.go_to = c.PLAY
                if self.selected_item == self.itens_tela[1]:
                    self.go_to = c.CONFIG
                if self.selected_item == self.itens_tela[2]:
                    self.go_to = c.MENU

        pos = mouse[0]
        for i in range(0,len(self.itens_tela)):
            if self.itens_rect[i].collidepoint(mouse[0]):
                self.selected_item = self.itens_tela[i]
                if mouse[1][0]:
                    if self.selected_item is not None:
                        if self.selected_item == self.itens_tela[0]:
                            self.go_to = c.PLAY
                        if self.selected_item == self.itens_tela[1]:
                            self.go_to = c.CONFIG
                        if self.selected_item == self.itens_tela[2]:
                            self.go_to = c.MENU

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
        self.item = self.font_text.render('LOADING',True,c.BLACK)
        self.x = c.DISPLAY_WIDTH-(self.item.get_width()*1.5)//1
        self.y = c.DISPLAY_HEIGHT-self.item.get_height()
        point = pg.Rect(self.x+self.item.get_width()+4,self.y+self.item.get_height()-7,2,2)
        point1 = pg.Rect(self.x+self.item.get_width()+8,self.y+self.item.get_height()-7,2,2)
        point2 = pg.Rect(self.x+self.item.get_width()+12,self.y+self.item.get_height()-7,2,2)
        self.points.append(point)
        self.points.append(point1)
        self.points.append(point2)
    def draw(self,screen):
        screen.blit(self.item,(self.x,self.y))
        for i in self.points:
            pg.draw.rect(screen,c.BLACK,i)


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
                item = self.font_text.render(self.itens[i],True,c.BLACK)
                screen.blit(item,((c.DISPLAY_WIDTH/2)-self.itens_tela[i].get_width()/2+2,(c.DISPLAY_HEIGHT/3)-self.itens_tela[i].get_height()+cont+2))
            screen.blit(self.itens_tela[i],(c.DISPLAY_WIDTH/2-self.itens_tela[i].get_width()/2, c.DISPLAY_HEIGHT/3-self.itens_tela[i].get_height()+cont))
            cont = cont + 30

    def start(self):
        self.itens_tela = []
        self.itens_rect = []
        self.selected_item = None
        self.select_index = -1
        cont = 0
        for i in self.itens:
            item = self.font_text.render(i,True,c.WHITE)
            self.itens_tela.append(item)
            rect = item.get_rect()
            
            rect.left = (c.DISPLAY_WIDTH/2)-item.get_width()/2
            rect.top = (c.DISPLAY_HEIGHT/3)-item.get_height()+cont
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
    
class credits():
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
        item = self.font_text.render('by AndorinhaViril  inc.',True,c.BLACK)
        screen.blit(item,((c.DISPLAY_WIDTH/2)-item.get_width()/2,0))
        if self.itens_tela is self.selected_item:
            item = self.font_text.render(self.item,True,c.BLACK)
            screen.blit(item,((c.DISPLAY_WIDTH/2)-self.itens_tela.get_width()/2+2,(c.DISPLAY_HEIGHT)-self.itens_tela.get_height()+2))
        screen.blit(self.itens_tela,((c.DISPLAY_WIDTH/2)-self.itens_tela.get_width()/2,(c.DISPLAY_HEIGHT)-self.itens_tela.get_height()))
    def reset(self):
        self.selected_item = None
        self.select_index = -1
        self.go_to = None
    def start(self):
        self.itens_tela = None
        self.itens_rect = None
        self.selected_item = None
        self.select_index = -1
        item = self.font_text.render(self.item,True,c.WHITE)
        self.itens_tela = item
        rect = item.get_rect()
        rect.left = (c.DISPLAY_WIDTH/2)-item.get_width()/2
        rect.top = (c.DISPLAY_HEIGHT)-item.get_height()
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
                    self.go_to = c.MENU
        pos = mouse[0]
        if self.itens_rect.collidepoint(pos):
            self.selected_item = self.itens_tela
            if mouse[1][0]:
                if self.selected_item is not None:
                    self.go_to = c.MENU
                        
class hud():
    def __init__(self):
        self.font_text = pg.font.Font('resources/fonts/METROLOX.ttf',20)
        self.heart = pg.image.load(os.path.join('resources\graphics', 'hart.png'))
    def draw(self,screen,player_pos,end_pos,status):
        if status == c.ALIVE:
            item = self.font_text.render('{}, {} - {}, {}'.format(player_pos[0],player_pos[1],end_pos[0]//70,end_pos[1]//70),True,c.BLACK)
            screen.blit(item,(50,0))
            screen.blit(self.heart,(0,0))
        else:
            item = self.font_text.render('DIED',True,c.BLACK)
            item2 = self.font_text.render('DIED',True,c.WHITE)
            item3 = self.font_text.render('PRESS R TO RESTART',True,c.WHITE)
            item4 = self.font_text.render('PRESS R TO RESTART',True,c.BLACK)
            x = c.DISPLAY_WIDTH/2 - item.get_width()/2
            y = c.DISPLAY_HEIGHT/2 - item.get_height()
            x2 = c.DISPLAY_WIDTH/2 - item3.get_width()/2
            y2 = c.DISPLAY_HEIGHT/2 + item.get_height()
            screen.blit(item,  (x,y))
            screen.blit(item2, (x-2,y-2))
            screen.blit(item4, (x2,y2))
            screen.blit(item3, (x2-2,y2-2))


