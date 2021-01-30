'''
Todos os objetos que possuem colizão, movimento ou que tem que estar na tela durante o gameplay
'''
import pygame as pg
import os
import data.constants as c
import random as r
class player():
    def __init__(self):
        #variaveis
        self.height = 55
        self.width = 40
        self.images = []
        self.images.append(pg.image.load(os.path.join('resources\\graphics', 'player.png')))
        self.images.append(pg.image.load(os.path.join('resources\\graphics', 'player2.png')))
        self.images.append(pg.image.load(os.path.join('resources\\graphics', 'climb.png')))
        self.images.append(pg.image.load(os.path.join('resources\\graphics', 'stomped.png')))
        self.images.append(pg.image.load(os.path.join('resources\\graphics', 'dead.png')))
        self.images.append(pg.image.load(os.path.join('resources\\graphics', 'bulleted.png')))
        #self.sounds = []
        #self.sounds.append(pg.mixer.Sound(os.path.join('resources\sounds', 'fiaeeee.ogg')))
        #self.sounds.append(pg.mixer.Sound(os.path.join('resources\sounds', 'fiaeeee.ogg')))
        self.sprite = self.images[0]
        self.view_collision = False
        self.iindex = True
        self.cont = 0
        self.num_death = 0
        self.atack_cont = 0
        self.x = 0
        self.y = 0
        self.sounds = []
        self.sounds.append(pg.mixer.Sound(os.path.join('resources\\sounds','path.wav')))
        self.sounds.append(pg.mixer.Sound(os.path.join('resources\\sounds','jump.wav')))
        self.state = c.STAND
        self.speed = 0
        self.speedy = 0
        self.jump = False
        self.atack = False
        self.climb = False
        self.dead = c.ALIVE
        self.climb_side = 0#-1 == esquerda +1 direita
        self.flip_sprite = False
        self.on_end = True
        self.startsoundfall = False
        self.sound = False
        self.lookto = ''
        self.looktocount = 0
        self.collision = pg.Rect(self.x,self.y+12,self.width,self.height)
        self.atack_collision = pg.Rect(self.collision.center[0]+20,self.collision.center[1]-10,40,20)
        self.collisions = {'top':False,'bottom':False,'left':False,'right':False}
    def set_xy(self, xy):
        self.x = xy[0]
        self.y = xy[1] + self.height
        self.collision = pg.Rect(self.x,self.y+12,self.width,self.height)
        #print('x: {} y: {}'.format(*xy))
    def set_spawn(self, spawn):
        #print('c:{} b:{}'.format(spawn.center,spawn.bottom))
        if self.dead != c.ALIVE:
            self.num_death += 1
        self.collision.center = spawn.center
        self.collision.bottom = spawn.bottom
        self.x = self.collision.x
        self.y = self.collision.y-12
        self.dead = c.ALIVE
        self.speedy,self.speed = 0,0
    def swap_state(self, state):#não utilizado por apresentar muita inconsistencia
        if self.state != c.FALL:
            if self.state == c.JUMP or self.state == c.WALKJ:
                if state == c.FALL or state == c.WALK:
                    self.state = state
            if self.state == c.WALK:
                if state == c.WALK or state == c.JUMP or state == c.WALKJ:
                    self.state = state
            if self.state == c.STAND:
                if state == c.COWER or state == c.WALK or state == c.JUMP or state == c.WALKJ:
                    self.state = state
            if self.state == c.COWER:
                if state == c.STAND or state == c.WALK or state == c.JUMP:
                    self.state = state
        else:
            self.state = state
            
    def draw(self,screen,camera):
        if self.view_collision:
            col = pg.Rect(self.collision.x-camera[0],self.collision.y-camera[1],self.width,self.height)
            pg.draw.rect(screen,c.REDA,col)
        if self.atack:
            pg.draw.rect(screen,(190,0,90),pg.Rect(self.atack_collision.x-camera[0],self.atack_collision.y-camera[1],40,20))
        if self.flip_sprite:
            if self.dead == c.ALIVE:
                if self.climb:
                    screen.blit(pg.transform.flip(self.images[2],True,False),(self.x-camera[0],self.y-camera[1]))
                else:
                    screen.blit(pg.transform.flip(self.sprite,True,False),(self.x-camera[0],self.y-camera[1]))
            else:
                if self.dead == c.STOMPED:
                    screen.blit(pg.transform.flip(self.images[3],True,False),(self.x-camera[0],self.y-camera[1]))
                elif self.dead == c.SLASH:
                    screen.blit(pg.transform.flip(self.images[4],True,False),(self.x-camera[0],self.y-camera[1]))
                elif self.dead == c.SHOT:
                    screen.blit(pg.transform.flip(self.images[5],True,False),(self.x-camera[0],self.y-camera[1]))
        else:
            if self.dead == c.ALIVE:
                if self.climb:
                    screen.blit(self.images[2],(self.x-camera[0],self.y-camera[1]))
                else:
                    screen.blit(self.sprite,(self.x-camera[0],self.y-camera[1]))
            else:
                if self.dead == c.STOMPED:
                    screen.blit(self.images[3],(self.x-camera[0],self.y-camera[1]))
                elif self.dead == c.SLASH:
                    screen.blit(self.images[4],(self.x-camera[0],self.y-camera[1]))
                elif self.dead == c.SHOT:
                    screen.blit(self.images[5],(self.x-camera[0],self.y-camera[1]))

    def update(self,fps,saws):
        if self.speed != 0:
            if self.cont >= fps//5:    
                if self.iindex:
                    self.sprite = self.images[1]
                    self.iindex = not self.iindex
                    self.sounds[0].play()
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
        if self.dead == c.ALIVE:
            if key[pg.K_DOWN]:
                self.swap_state(c.COWER)
                if self.looktocount == 30:
                    self.lookto = 'down'
                    self.looktocount = 0
                else:
                    self.looktocount += 1
            if key[pg.K_UP]:
                if self.looktocount == 30:
                    self.lookto = 'up'
                    self.looktocount = 0
                else:
                    self.looktocount += 1
            if not key[pg.K_DOWN] and not key[pg.K_UP]:
                self.lookto = ''
            if key[pg.K_RIGHT]:
                self.swap_state(c.WALK)
                self.flip_sprite = False
                if self.climb_side == -1:
                    self.climb = False
                    self.climb_side = 0
                if self.speed < c.MAX_SPEED:
                    self.speed += c.ACCEL
            if key[pg.K_LEFT]:
                self.swap_state(c.WALK)
                self.flip_sprite = True
                if self.climb_side == 1:
                    self.climb = False
                    self.climb_side = 0
                if self.speed > c.MAX_SPEED*-1:
                    self.speed -= c.ACCEL
            if key[pg.K_a]:
                self.y= -2
                self.collision.y = -2
            if key[pg.K_z]:
                if not self.jump:
                    self.sounds[1].play()
                    self.speedy = c.JUMP_FORCE
                    self.jump = True
                    self.climb = False
                    self.climb_side = 0
            if key[pg.K_x]:
                if not self.atack:
                    self.atack = True
        if not key[pg.K_LEFT] and not key[pg.K_RIGHT]:
            self.swap_state(c.STAND)
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
            self.state = c.FALL
            self.speedy += c.ACCEL
            self.jump = True
            if self.speedy > 110:
                self.dead = c.STOMPED
        else:
            if self.speedy >= c.TERMINAL_SPEED:
                self.dead = c.STOMPED
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
                        self.dead = c.SLASH    
            elif colUni.type == 'b':
                if rect.collidepoint(colUni.point):
                    colUni.collided = True
                    self.dead = c.SHOT
            elif colUni.type == 'f':
                if rect.colliderect(colUni.collision):
                    if colUni.speeds[1]>20:
                        self.dead = c.STOMPED
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
            self.atack_collision = pg.Rect(self.collision.center[0]+20,self.collision.center[1]-20,40,20)
        else:
            self.atack_collision = pg.Rect(self.collision.center[0]-60,self.collision.center[1]-20,40,20)
        for i in collides:
            if i.type == 's':
                if i.collision is not None:
                    if self.atack_collision.colliderect(i.collision):
                        i.life -= 1
            if i.type == 'f':
                if self.atack_collision.colliderect(i.collision):
                    i.life -= 1

class plataform():
    def __init__(self, phase):
        self.height = 70
        self.width = 70
        self.phase = phase
        self.spawn = None
        self.end = None
        #self.x = 140
        #self.y = 450
        self.cont = 0
        self.visible = True
        self.things_collide = []
        self.things_draw = []
        self.blocks = []
        self.saws = []
        self.broken_saws = []
        self.canons = []
        self.bullets = []
        self.flys = []
        #self.collision = pg.Rect(self.x,self.y,self.width,self.height)
    def draw(self,screen,camera):
##        if self.visible:
##            pg.draw.rect(screen,c.RED,[self.x, self.y, self.width, self.height])
        '''for b in self.blocks:
            #if b.x+70-camera[0] > 0 and b.y+70-camera[1] > 0 or b.x-camera[0] < c.SCREEN_WIDTH and b.y-camera[1] < c.SCREEN_HEIGHT:
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
##        pg.draw.rect(screen,c.REDA,sp)
        ed = pg.Rect(self.end.x-camera[0],(self.end.y)-camera[1],self.end.width,self.end.height)
        pg.draw.rect(screen,c.REDA,ed)
    def update(self,camera,pos,dead):
        ppos = [pos[0]//70,pos[1]//70]
        for ca in self.canons:
            ca.update(self.bullets)
        for bu in self.bullets:
            bu.update(self.blocks)
            if bu.collided or self.bullet_collide(bu.side,bu.pos):
                self.bullets.remove(bu)
        for s in self.saws:
            s.update(self.broken_saws)
        for bs in self.broken_saws:
            if bs in self.things_collide:
                bs.update(self.things_draw) 
        for f in self.flys:
            if f.life <= 0:
                self.flys.remove(f)
                break
            if f in self.things_collide:
                f.update(pos,dead,self.things_draw)
        self.collide_draw_update(ppos)
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
            if b.pos[1] >= pos[0]-c.DRAW_DISTANCE_X and b.pos[1] <= pos[0]+c.DRAW_DISTANCE_X and b.pos[0] <= pos[1]+c.DRAW_DISTANCE_Y and b.pos[0] >= pos[1]-c.DRAW_DISTANCE_Y:
                self.things_draw.append(b)
                if b.pos[1] >= pos[0]-1 and b.pos[1] <= pos[0]+1 and b.pos[0] <= pos[1]+1 and b.pos[0] >= pos[1]-1:
                    if b.has_collision:
                        self.things_collide.append(b) 
        for s in self.saws:
            if s.pos[1] >= pos[0]-c.DRAW_DISTANCE_X and s.pos[1] <= pos[0]+c.DRAW_DISTANCE_X and s.pos[0] <= pos[1]+c.DRAW_DISTANCE_Y and s.pos[0] >= pos[1]-c.DRAW_DISTANCE_Y:
                self.things_draw.append(s)
                if s.pos[1] >= pos[0]-1 and s.pos[1] <= pos[0]+1 and s.pos[0] <= pos[1]+1 and s.pos[0] >= pos[1]-1:
                    self.things_collide.append(s)
        for bs in self.broken_saws:
            if bs.pos[1] >= pos[0]-c.DRAW_DISTANCE_X and bs.pos[1] <= pos[0]+c.DRAW_DISTANCE_X and bs.pos[0] <= pos[1]+c.DRAW_DISTANCE_Y and bs.pos[0] >= pos[1]-c.DRAW_DISTANCE_Y:
                if bs.can_hurt:
                    self.things_collide.append(bs)
                self.things_draw.append(bs)
        for ca in self.canons:
            if ca.pos[1] >= pos[0]-c.DRAW_DISTANCE_X and ca.pos[1] <= pos[0]+c.DRAW_DISTANCE_X and ca.pos[0] <= pos[1]+c.DRAW_DISTANCE_Y and ca.pos[0] >= pos[1]-c.DRAW_DISTANCE_Y:
                self.things_draw.append(ca)
        for bu in self.bullets:
            if bu.pos[1] >= pos[0]-c.DRAW_DISTANCE_X and bu.pos[1] <= pos[0]+c.DRAW_DISTANCE_X and bu.pos[0] <= pos[1]+c.DRAW_DISTANCE_Y and bu.pos[0] >= pos[1]-c.DRAW_DISTANCE_Y:
                self.things_draw.append(bu)
                if bu.pos[1] >= pos[0]-1 and bu.pos[1] <= pos[0]+1 and bu.pos[0] <= pos[1]+1 and bu.pos[0] >= pos[1]-1:
                    self.things_collide.append(bu)
        for f in self.flys:
            if f.pos[1] >= pos[0]-c.DRAW_DISTANCE_X and f.pos[1] <= pos[0]+c.DRAW_DISTANCE_X and f.pos[0] <= pos[1]+c.DRAW_DISTANCE_Y and f.pos[0] >= pos[1]-c.DRAW_DISTANCE_Y:
                self.things_draw.append(f)
                self.things_collide.append(f)
    def copy_phase(self):
        cont_x = 0
        cont_y = 0
        for s in self.phase:
            b = None
            cont_x = 0
            for a in s:
                if cont_y == 0:
                    if cont_x == 0:
                        b = block((cont_x,cont_y),c.BLOCK_SIZE,(cont_y,cont_x),True)
                    else:
                        b = block((cont_x*self.width,cont_y),c.BLOCK_SIZE,(cont_y,cont_x),True)
                else:
                    if cont_x == 0:
                        b = block((cont_x,cont_y*self.height),c.BLOCK_SIZE,(cont_y,cont_x),True)
                    else:
                        b = block((cont_x*self.width,cont_y*self.height),c.BLOCK_SIZE,(cont_y,cont_x),True)
                if a[3] == '9':
                    #print('9')
                    b.set_has_collision(True)
                if a[0] == '9':
                    b.type = 2
                    self.blocks.append(b)
                elif a[0] == '1':
                    self.spawn = b.collision
                    b.set_has_collision(True)
                elif a[0] == '8':
                    self.end = b.collision
                    b.type = 0
                    b.set_has_collision(True)
                    self.blocks.append(b)
                elif a[0] == '3':
                    b.type = 3
                    b.set_sprite(pg.image.load(os.path.join('resources\\graphics', 'grass.png')))
                    self.blocks.append(b)
                if a[1] == '1':
                    s = saw(b)
                    s.start()
                    self.saws.append(s)
                elif a[1] =='2':
                    #print(f'canon {a}')
                    if a[2] == '2':
                        ca = canon(2,b)
                        ca.start()
                        self.canons.append(ca)
                    if a[2] == '3':
                        ca = canon(3,b)
                        ca.start()
                        self.canons.append(ca)
                elif a[1] == '6':
                    #print(f'fly {a}')
                    f = fly(b)
                    self.flys.append(f)
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
    def __init__(self, xy, wh, pos, scalable):
        #chama o construtor da classe mãe
        pg.sprite.Sprite.__init__(self)
        self.sprite = pg.image.load(os.path.join('resources\\graphics', 'dirt.png'))
        self.scalable = scalable
        self.height = 70
        self.width = 70
        self.type = 2
        self.pos = pos
        self.x = xy[0]
        self.y = xy[1]
        self.collision = pg.Rect(self.x,self.y,self.width,self.height)
        self.has_collision = False
    def set_xy(self,xy):
        self.x = xy[0]
        self.y = xy[1]
    def draw(self,screen,camera):
        if c.COLLISION_BLOCKS_ONLY:
            if self.has_collision:
                screen.blit(self.sprite,(self.x-camera[0],self.y-camera[1]))
        else:
            screen.blit(self.sprite,(self.x-camera[0],self.y-camera[1]))
    def set_sprite(self,sprite):
        self.sprite = sprite
    def set_has_collision(self, has_collision):
        self.has_collision = has_collision
    def update(self,camera):
        pass
    
class saw():
    def __init__(self,block):
        self.x = 0
        self.y = 0
        self.type = 's'
        self.life = 45
        self.deactived = False
        self.pos = (block.pos[0]-1,block.pos[1])
        self.block = block
        self.image = pg.image.load(os.path.join('resources\\graphics', 'saw.png'))
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
        #pg.draw.rect(screen,(255,0,0),pg.Rect(self.x-camera[0],self.y-camera[1],55,60))
        screen.blit(self.image,(self.x-camera[0],self.y-camera[1]))
    def deactive(self,bsaws):
        ts = torn_saw(self)
        ts.throw()
        bsaws.append(ts)
        self.collision = None
        self.image = pg.image.load(os.path.join('resources\\graphics', 'broken_saw_holder.png'))
        self.x = self.block.collision.center[0]
        self.y = self.block.collision.top-self.image.get_height()
class torn_saw():
    def __init__(self,saw):
        self.type = 'ts'
        self.pos = [saw.pos[0],saw.pos[1]]
        self.image = pg.image.load(os.path.join('resources\\graphics', 'broken_saw.png'))
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
        self.type = -1
        self.pos = rect.pos
        self.side = side
        self.atack_time = 100
        self.image = pg.image.load(os.path.join('resources\\graphics', 'canon.png'))
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
        self.image = pg.image.load(os.path.join('resources\\graphics', 'bullet.png'))
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
            self.speedy = -c.BULLETSPEED
        elif self.side == 2:
            self.x = self.canon.x
            self.y = self.canon.y+16
            self.collision.x = self.x
            self.collision.y = self.y
            self.speed = -c.BULLETSPEED
        elif self.side == 3:
            self.x = self.canon.x+60
            self.y = self.canon.y+16
            self.collision.x = self.x
            self.collision.y = self.y
            self.image = pg.transform.rotate(self.image,180)
            self.speed = c.BULLETSPEED
        elif self.side == 4:
            self.collision = pg.Rect(self.x,self.y,5,7)
            self.x = self.canon.x+16
            self.y = self.canon.y+60
            self.collision.x = self.x
            self.collision.y = self.y
            self.image = pg.transform.rotate(self.image,90)
            self.speedy = c.BULLETSPEED
class fly():
    
    def __init__(self,block):
        self.image = pg.image.load(os.path.join('resources\\graphics', 'fly.png'))
        self.collision = pg.Rect(block.collision.center[0],block.collision.bottom,30,25)
        self.collisions = {'top':False,'bottom':False,'right':False,'left':False}
        self.speeds = [0,0]
        self.type = 'f'
        self.life = 5
        self.is_flying = False
        self.pos = [self.collision.y//70,self.collision.x//70]
    def draw(self,screen,camera):
##        col = pg.Rect(self.collision.x-camera[0],self.collision.y-camera[1],30,25)
##        pg.draw.rect(screen,c.REDA,col)
        if not self.is_flying:
            screen.blit(pg.transform.flip(self.image,False,True),(self.collision.x-camera[0],self.collision.y-camera[1]))
        else:
            screen.blit(self.image,(self.collision.x-camera[0],self.collision.y-camera[1]))
            
    def update(self,ppos,palive,blocks):
        spos = (self.collision.x,self.collision.y)
        dist = int((((spos[0] - ppos[0])**2 + (spos[1] - ppos[1])**2)**0.5)//1)
        if dist <=70*5 and spos[1] < ppos[1]:
            self.is_flying = True
        if self.is_flying:
            self.move(ppos,dist,palive,blocks)
            
    def move(self,target,dist,palive,blocks):
        spos = self.collision.center
        self.collision_test(blocks)
        if spos[1] < target[1]-20 and dist<= 70*5 and palive:
            if target[0]-10 < spos[0] and target[0]+10 > spos[0]:
                self.speeds[0] = 0
            elif spos[0] <= target[0]:
                self.speeds[0] = 10
            elif spos[0] >= target[0]:
                self.speeds[0] = -10
            if (spos[0] - 10 <= target[0] and spos[0] + 10 >= target[0]):
                self.speeds[1] = 30
            
        else:
            if not self.collisions['top']:
                self.speeds[1] = -10
            else:
                self.is_flying = False
        self.pos = [self.collision.y/70,self.collision.x/70]
    def collision_test(self,blocks):
        self.collisions = {'top':False,'bottom':False,'right':False,'left':False}
        self.collision.y += self.speeds[1]
        for b in blocks:
            if b.type == 2:
                if self.collision.colliderect(b.collision):
                    if self.speeds[1] > 0:
                        self.speeds[1] = 0
                        self.collision.bottom = b.collision.top
                        self.collisions['bottom'] = True
                    elif self.speeds[1] < 0:
                        self.speeds[1] = 0
                        self.collision.top = b.collision.bottom
                        self.collisions['top'] = True
        self.collision.x += self.speeds[0]
        for b in blocks:
            if b.type == 2:
                if self.collision.colliderect(b.collision):
                    if self.speeds[0] > 0:
                        self.speeds[0] = 0
                        self.collision.right = b.collision.left
                        self.collisions['right'] = True
                    elif self.speeds[0] < 0:
                        self.speeds[0] = 0
                        self.collision.left = b.collision.right
                        self.collisions['left'] = True    
