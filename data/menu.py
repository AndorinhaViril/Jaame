'''
Toda a interface e HUD, assim como seus eventos
'''
import pygame as pg
import data.constants as c
import os

class menu():
    def __init__(self):
        self.font_title = pg.font.Font('resources/fonts/zenda.ttf',44)
        self.font_text = pg.font.Font('resources/fonts/METROLOX.ttf',20)
        self.title = None
        self.itens = []
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
        if self.title is not None:
           screen.blit(self.title,(10,15))
        for i in range(0,len(self.itens_tela)):
            #pg.draw.rect(screen,c.REDA,self.itens_rect[i])
            if self.itens_tela[i] is self.selected_item:
                item = self.font_text.render(self.itens[i],True,c.BLACK)
                screen.blit(item,(self.itens_rect[i].x,self.itens_rect[i].y+2))
            screen.blit(self.itens_tela[i],(self.itens_rect[i].x,self.itens_rect[i].y))
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
                return self.select_index
        pos = mouse[0]
        for i in range(0,len(self.itens_tela)):
            if self.itens_rect[i].collidepoint(mouse[0]):
                self.selected_item = self.itens_tela[i]
                if mouse[1][0]:
                    if self.selected_item is not None:
                        return self.select_index
        return None
class inicial(menu):
    def __init__(self):
        menu.__init__(self)
    def draw(self,screen):
        menu.draw(self,screen)
    def start(self):
        self.itens = ['Play','Load','Configs','Credits','Get out']
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
            rect = itens.get_rect()
            rect.left = 20
            rect.top = 25+self.title.get_height()+itens.get_height()+cont
            self.itens_rect.append(rect)
            self.itens_tela.append(itens)
            cont+=30

    def event(self,mouse,key):
        aux = menu.event(self,mouse,key)
        if aux is not None:
            if aux == 0:
                self.go_to = c.PLAY
            elif aux == 1:
                self.go_to = c.LPHASE
            elif aux == 2:
                self.go_to = c.CONFIG
            elif aux == 3:
                self.go_to = c.IMPIKA
            elif aux == 4:
                self.go_to = c.CLOSE
class pause():
    def __init__(self):
        self.itens = ['Back','Configs','Save Phase','Start Menu']
        self.font_text = pg.font.Font('resources/fonts/METROLOX.ttf',20)
        self.save = pg.image.load(os.path.join('resources\graphics', 'floppy.png'))
        self.save_ = None 
        self.itens_tela = []
        self.itens_rect = []
        self.itens_pos = []
        self.selected_item = None
        self.select_index = -1
        self.go_to = None
        self.can = True
    def reset(self):
        self.selected_item = None
        self.select_index = -1
        self.go_to = None
    def draw(self,screen):
        for i in range(0,len(self.itens_tela)):
            if self.itens_tela[i] is self.selected_item:
                item = self.font_text.render(self.itens[i],True,c.BLACK)
                screen.blit(item,(self.itens_pos[i][0],self.itens_pos[i][1]+2))
            #pg.draw.rect(screen,(0,0,0),self.itens_rect[i])
            screen.blit(self.itens_tela[i],(self.itens_pos[i][0],self.itens_pos[i][1]))
            #screen.blit()
    def start(self):
        self.itens_tela = []
        self.itens_rect = []
        self.itens_pos = []
        self.selected_item = None
        self.select_index = -1
        cont = 0
        for i in self.itens:
            item = self.font_text.render(i,True,c.WHITE)
            self.itens_tela.append(item)
            rect = item.get_rect()
            rect.x = (c.SCREEN_WIDTH/2)-item.get_width()/2
            rect.y = ((c.SCREEN_HEIGHT/3)-item.get_height())+cont
            self.itens_pos.append((rect.x,rect.y))
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
                        self.go_to = c.SPHASE
                if self.selected_item == self.itens_tela[3]:
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
                            self.go_to = c.SPHASE
                        if self.selected_item == self.itens_tela[3]:
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
        self.x = c.SCREEN_WIDTH-(self.item.get_width()*1.5)//1
        self.y = c.SCREEN_HEIGHT-self.item.get_height()
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

class save_phase():
    def __init__(self):
        self.font_text = pg.font.Font('resources/fonts/METROLOX.ttf',20)
        self.itens = ['Save','Back']
        self.itens_tela = []
        self.itens_rect = []
        self.itens_pos = []
        self.selected_item = None
        self.select_index = -1
        self.go_to = None
    def reset(self):
        self.selected_item = None
        self.select_index = -1
        self.go_to = None
    def draw(self,screen):
        for i in range(0,len(self.itens_tela)):
            if self.itens_tela[i] is self.selected_item:
                item = self.font_text.render(self.itens[i],True,c.BLACK)
                screen.blit(item,(self.itens_pos[i][0],self.itens_pos[i][1]+2))
            #pg.draw.rect(screen,(0,0,0),self.itens_rect[i])
            screen.blit(self.itens_tela[i],(self.itens_pos[i][0],self.itens_pos[i][1]))
            #screen.blit()
    def start(self):
        self.itens_tela = []
        self.itens_rect = []
        self.itens_pos = []
        self.selected_item = None
        self.select_index = -1
        self.save = False
        cont = 0
        for i in self.itens:
            item = self.font_text.render(i,True,c.WHITE)
            self.itens_tela.append(item)
            rect = item.get_rect()
            rect.x = (c.SCREEN_WIDTH/2)-item.get_width()/2
            rect.y = ((c.SCREEN_HEIGHT/3)-item.get_height())+cont
            self.itens_pos.append((rect.x,rect.y))
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
                    self.save = True
                    self.go_to = c.PAUSE
                if self.selected_item == self.itens_tela[1]:
                    self.go_to = c.PAUSE

        pos = mouse[0]
        for i in range(0,len(self.itens_tela)):
            if self.itens_rect[i].collidepoint(mouse[0]):
                self.selected_item = self.itens_tela[i]
                if mouse[1][0]:
                    if self.selected_item is not None:
                        if self.selected_item == self.itens_tela[0]:
                            self.save = True
                            self.go_to = c.PAUSE
                        if self.selected_item == self.itens_tela[1]:
                            self.go_to = c.PAUSE

class load_phase():
    def __init__(self):
        self.font_text = pg.font.Font('resources/fonts/METROLOX.ttf',20)
        self.archieves = []
        self.itens_tela = []
        self.itens_rect = []
        self.itens_pos = []
        self.to_load = None
        self.selected_item = None
        self.select_index = -1
        self.go_to = None
    def start(self):
        self.itens_tela = []
        self.itens_rect = []
        self.itens_pos = []
        self.selected_item = None
        self.archieves = []
        self.select_index = -1
        self.to_load = None
        caminhos = [os.path.join('maps', nome) for nome in os.listdir('maps')]
        arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
        for arq in arquivos: 
            if arq.lower().endswith(".phg"):
                aux = arq.replace('.phg','')
                aux = aux.replace('maps\\','')
                self.archieves.append(aux)
        self.archieves.append('Back')
        
        cont = 0
        for i in self.archieves:
            item = self.font_text.render(i,True,c.WHITE)
            self.itens_tela.append(item)
            rect = item.get_rect()
            rect.x = (c.SCREEN_WIDTH/2)-item.get_width()/2
            rect.y = ((c.SCREEN_HEIGHT/3)-item.get_height())+cont
            self.itens_pos.append((rect.x,rect.y))
            self.itens_rect.append(rect)
            cont+=30
    def reset(self):
        self.selected_item = None
        self.select_index = -1
        self.go_to = None
    def draw(self,screen):
        for i in range(0,len(self.itens_tela)):
            if self.itens_tela[i] is self.selected_item:
                item = self.font_text.render(self.archieves[i],True,c.BLACK)
                screen.blit(item,(self.itens_pos[i][0],self.itens_pos[i][1]+2))
            #pg.draw.rect(screen,(0,0,0),self.itens_rect[i])
            screen.blit(self.itens_tela[i],(self.itens_pos[i][0],self.itens_pos[i][1]))
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
                if self.selected_item == self.itens_tela[len(self.itens_tela)-1]:
                    self.go_to = c.MENU
                else:
                    self.to_load = f'maps\\{self.archieves[self.select_index]}.phg'
                    self.go_to = c.PLAY
        pos = mouse[0]
        for i in range(0,len(self.itens_tela)):
            if self.itens_rect[i].collidepoint(mouse[0]):
                self.selected_item = self.itens_tela[i]
                if mouse[1][0]:
                    if self.selected_item is not None:
                        if self.selected_item == self.itens_tela[len(self.itens_tela)-1]:
                            self.go_to = c.MENU
                        else:
                            self.to_load = f'maps\\{self.archieves[i]}.phg'
                            self.go_to = c.PLAY
   
class config():
    def __init__(self):
        self.itens = [f'Zoom {c.ZOOM_OPTIONS[c.SCREEN_ZOOM]}','Show Only Blocks with Collision' if c.COLLISION_BLOCKS_ONLY else 'SHOW ALL BLOCKS','No Save Completed Phases' if not c.SAVE_COMPLETED_PHASES else 'Save Completed Phases','Back']
        self.font_text = pg.font.Font('resources/fonts/METROLOX.ttf',20)
        self.title = None
        self.itens_tela = []
        self.itens_rect = []
        self.selected_item = None
        self.zoom = c.SCREEN_ZOOM
        self.go_to = None
        self.from_ = None
        self.can = True
        self.can_side = True
    def draw(self, screen):
        cont = 0
        for i in range(0,len(self.itens_tela)):
            if i == 0:
                self.itens[0] = f'Zoom {c.ZOOM_OPTIONS[self.zoom]}'
            if self.itens_tela[i] is self.selected_item:
                item = self.font_text.render(self.itens[i],True,c.BLACK)
                screen.blit(item,((c.SCREEN_WIDTH/2)-self.itens_tela[i].get_width()/2+2,(c.SCREEN_HEIGHT/3)-self.itens_tela[i].get_height()+cont+2))
            screen.blit(self.itens_tela[i],(c.SCREEN_WIDTH/2-self.itens_tela[i].get_width()/2, c.SCREEN_HEIGHT/3-self.itens_tela[i].get_height()+cont))
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
            
            rect.left = (c.SCREEN_WIDTH/2)-item.get_width()/2
            rect.top = (c.SCREEN_HEIGHT/3)-item.get_height()+cont
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
        if key[pg.K_RETURN] or key[pg.K_z]:
            if self.selected_item is not None:
                if self.selected_item == self.itens_tela[3]:
                    self.go_to = self.from_
        if key[pg.K_RIGHT] or key[pg.K_LEFT]:
            if self.selected_item == self.itens_tela[0]:
                if self.can_side:
                    self.can_side = False
                    zidx = 0
                    for i,zoom in enumerate(c.ZOOM_OPTIONS):
                        if zoom == self.zoom:
                            zidx = i
                    if key[pg.K_RIGHT]:
                        if zidx < len(c.ZOOM_OPTIONS)-1:
                            zidx += 1
                        else:
                            zidx = 0
                    
                    if key[pg.K_LEFT]:
                        if zidx == 0:
                            zidx = len(c.ZOOM_OPTIONS)-1
                        else:
                            zidx -=1
                    for i,zoom in enumerate(c.ZOOM_OPTIONS):
                            if i == zidx:
                                self.zoom = zoom
                                c.DRAW_DISTANCE_X = 7 if c.SCREEN_ZOOM <= 1 else 7*self.zoom
                                c.DRAW_DISTANCE_Y = 5 if c.SCREEN_ZOOM <= 1 else 5*self.zoom
                                break
                    self.itens_tela[0] = self.font_text.render(f'Zoom {c.ZOOM_OPTIONS[self.zoom]}',True,c.WHITE)
                    self.selected_item = self.itens_tela[0]
            if self.selected_item == self.itens_tela[1]:
                if self.can_side:
                    self.can_side = False
                    if c.COLLISION_BLOCKS_ONLY:
                        c.COLLISION_BLOCKS_ONLY = False
                        self.itens[1] = 'SHOW ALL BLOCKS'
                        self.itens_tela[1] = self.font_text.render(self.itens[1],True,c.WHITE)
                        self.selected_item = self.itens_tela[1]
                    else:
                        c.COLLISION_BLOCKS_ONLY = True
                        self.itens[1] = 'Show Only Blocks with Collision'
                        self.itens_tela[1] = self.font_text.render(self.itens[1],True,c.WHITE)
                        self.selected_item = self.itens_tela[1]
            if self.selected_item == self.itens_tela[2]:
                if self.can_side:
                    self.can_side = False
                    if c.SAVE_COMPLETED_PHASES:
                        c.SAVE_COMPLETED_PHASES = False
                        self.itens[2] = 'No Save Completed Phases'
                        self.itens_tela[2] = self.font_text.render(self.itens[2],True,c.WHITE)
                        self.selected_item = self.itens_tela[2]
                    else:
                        c.SAVE_COMPLETED_PHASES = True
                        self.itens[2] = 'Save Completed Phases'
                        self.itens_tela[2] = self.font_text.render(self.itens[2],True,c.WHITE)
                        self.selected_item = self.itens_tela[2]
            if self.selected_item == self.itens_tela[3]:
                self.go_to = self.from_
        if not key[pg.K_LEFT] and not key[pg.K_RIGHT]:
            self.can_side = True
        pos = mouse[0]
        for i in range(0,len(self.itens_tela)):
            if self.itens_rect[i].collidepoint(mouse[0]):
                self.selected_item = self.itens_tela[i]
                if mouse[1][0]:
                    if self.selected_item is not None:
                        if self.selected_item == self.itens_tela[3]:
                            self.go_to = self.from_
    def set_from(self,f):
        self.from_ = f
    
class credits():
    def __init__(self):
        self.item = 'Back'
        self.font_text = pg.font.Font(os.path.join('resources\\fonts','METROLOX.ttf'),20)
        self.title = None
        self.itens_tela = None
        self.itens_rect = None
        self.selected_item = None
        self.go_to = None
        self.can = True
    def draw(self,screen):
        item = self.font_text.render('\n\nby AndorinhaViril  inc.',True,c.BLACK)
        screen.blit(item,((c.SCREEN_WIDTH/2)-item.get_width()/2,0))
        if self.itens_tela is self.selected_item:
            item = self.font_text.render(self.item,True,c.BLACK)
            screen.blit(item,((c.SCREEN_WIDTH/2)-self.itens_tela.get_width()/2+2,(c.SCREEN_HEIGHT)-self.itens_tela.get_height()+2))
        screen.blit(self.itens_tela,((c.SCREEN_WIDTH/2)-self.itens_tela.get_width()/2,(c.SCREEN_HEIGHT)-self.itens_tela.get_height()))
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
        rect.left = (c.SCREEN_WIDTH/2)-item.get_width()/2
        rect.top = (c.SCREEN_HEIGHT)-item.get_height()
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
        self.heart = pg.image.load(os.path.join('resources\graphics', 'dark_hart.png'))
    def draw(self,screen,player_pos,end_pos,status,num_deaths,timer):
        if status == c.ALIVE:
            item = self.font_text.render('{}, {} | {}, {}'.format(player_pos[0],player_pos[1],end_pos[0]//70,end_pos[1]//70),True,c.BLACK)
            if num_deaths > 0:
                num = self.font_text.render(f' {num_deaths}',True,c.BLACK)
                screen.blit(self.heart,(0,0))
                screen.blit(num,(22,0))

            screen.blit(item,(100,0))
            t = self.getTime(timer)
            screen.blit(t,(c.SCREEN_WIDTH-t.get_width(),0))
        else:
            item = self.font_text.render('DIED',True,c.BLACK)
            item2 = self.font_text.render('DIED',True,c.WHITE)
            item3 = self.font_text.render('PRESS R TO RESTART',True,c.WHITE)
            item4 = self.font_text.render('PRESS R TO RESTART',True,c.BLACK)
            x = c.SCREEN_WIDTH/2 - item.get_width()/2
            y = c.SCREEN_HEIGHT/2 - item.get_height()
            x2 = c.SCREEN_WIDTH/2 - item3.get_width()/2
            y2 = c.SCREEN_HEIGHT/2 + item.get_height()
            screen.blit(item,  (x,y))
            screen.blit(item2, (x-2,y-2))
            screen.blit(item4, (x2,y2))
            screen.blit(item3, (x2-2,y2-2))
    def getTime(self,timer):
        ti = int(timer // 1) * -1
        minu = 0
        sec = 0

        if ti > 59:
            minu = ti//60
            sec = ti-(60*minu)
        else:
            sec = ti
        if int(sec) < 10:
            return self.font_text.render(f'{minu} : 0{int(sec)}',True,c.BLACK)
        else:
            return self.font_text.render(f'{minu} : {int(sec)}',True,c.BLACK)
