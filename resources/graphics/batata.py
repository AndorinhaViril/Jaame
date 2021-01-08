'''
tem como unico proposito teste de "fisica e animação", assim como de funcionalidades.
'''

import random as r
import pygame as pg

try:
    pg.init()
except:
    print('Falhou a inicialização do modulo principal')
SCREEN = pg.display.set_mode(size=(800,600))
SCREEN_RECT = SCREEN.get_rect()

def load_img(name):
    return pg.image.load(name)

class player(pg.sprite.Sprite):
    def __init__(self):
        super(player,self).__init__()
        self.images = []
        self.images.append(load_img('player.png'))
        self.images.append(load_img('player2.png'))
        self.images.append(load_img('climb.png'))
        self.images.append(load_img('stomped.png'))
        self.images.append(load_img('dead.png'))
        self.images.append(load_img('bulleted.png'))
        self.images.append(load_img('lying.png'))
        self.iindex = True
        self.cont = 0
        self.atack_cont = 0
        self.image = self.images[0]
        self.height = 67
        self.width = 40
        self.x = 400
        self.y = 100
        self.speed = 0
        self.speedy = 0
        self.dead = 0
        self.jump = False
        self.atack = False
        self.climb = False
        self.lying = False
        self.lyingcount = 0
        self.climb_side = 0#-1 == esquerda +1 direita
        self.flip_sprite = False
        self.collision = pg.Rect(self.x,self.y,self.width,self.height)
        self.atack_collision = pg.Rect(self.collision.center[0]+20,self.collision.center[1]+20,80,30)
        self.collisions = {'top':False,'bottom':False,'left':False,'right':False}
    def draw(self,screen):
        pg.draw.rect(screen,(190,0,230),self.collision)
        if self.atack:
            pg.draw.rect(screen,(190,0,90),self.atack_collision)
        if self.dead == 3:
            if self.flip_sprite:
                screen.blit(pg.transform.flip(self.images[3],True,False),(self.x,self.y))
            else:
                screen.blit(self.images[3],(self.x,self.y))
        elif self.dead == 4:
            if self.flip_sprite:
                screen.blit(pg.transform.flip(self.images[4],True,False),(self.x,self.y))
            else:
                screen.blit(self.images[4],(self.x,self.y))
        elif self.dead == 5:
            if self.flip_sprite:
                screen.blit(pg.transform.flip(self.images[5],True,False),(self.x,self.y))
            else:
                screen.blit(self.images[5],(self.x,self.y))
        else:
            if self.flip_sprite:
                if self.climb:
                    screen.blit(pg.transform.flip(self.images[2],True,False),(self.x,self.y))
                elif self.lying:
                    screen.blit(pg.transform.flip(self.images[6],True,False),(self.x,self.y))
                else:
                    screen.blit(pg.transform.flip(self.image,True,False),(self.x,self.y))
            else:
                if self.climb:
                    screen.blit(self.images[2],(self.x,self.y))
                elif self.lying:
                    screen.blit(self.images[6],(self.x,self.y))
                else:
                    screen.blit(self.image,(self.x,self.y))
        
    def update(self,fps):
        if self.speed != 0:
            if self.cont >= fps//3:    
                if self.iindex:
                    self.image = self.images[1]
                    self.iindex = not self.iindex
                else:
                    self.image = self.images[0]
                    self.iindex = not self.iindex
                self.cont=0
            self.cont +=1
        if self.atack_cont < 0:
            self.atack = False
            self.atack_cont += 1
        if self.atack:
            self.atack_test()
            if self.atack_cont == 15:
                self.atack_cont = -15
                self.atack = False
            self.atack_cont +=1
        #self.collision = pg.Rect(self.x,self.y,self.width,self.height)
        #print('x: {} y: {}'.format(self.speed,self.speedy))
    def move(self, key, m):
        self.collisions = {'top':False,'bottom':False,'right':False,'left':False}
        if self.dead==0:
            if key[pg.K_DOWN]:
                if self.lyingcount == 15 and not self.lying:
                    self.y = self.y+35
                    self.collision = pg.Rect(self.x,self.y,self.height,self.height-32)
                    self.lying = True
                elif not self.lying:
                    self.lyingcount += 1
            elif not key[pg.K_DOWN]:
                if self.lying:
                    self.lyingcount -= 1
                if self.lyingcount > -5 and self.lying:
                    self.lying = False
                    self.y -= 35
                    self.collision = pg.Rect(self.x,self.y,self.width,self.height)
            if key[pg.K_UP]:
                pass
            if key[pg.K_RIGHT]:
                self.flip_sprite = False
                if self.climb_side == -1:
                    self.climb = False
                    self.climb_side = 0
                if self.speed < 15:
                    self.speed += 1.5
            if key[pg.K_LEFT]:
                self.flip_sprite = True
                if self.climb_side == 1:
                    self.climb = False
                    self.climb_side = 0
                if self.speed > -15:
                    self.speed -= 1.5
            if key[pg.K_z]:
                if not self.jump:
                    self.speedy = -17
                    self.jump = True
                    self.climb = False
                    self.climb_side = 0
            if key[pg.K_x]:
                if not self.atack:
                    self.atack = True
            if key[pg.K_s]:
                self.speed, self.speedy = 0, 0
            if key[pg.K_a]:
                self.x,self.y = 400,120

        if not key[pg.K_LEFT] and not key[pg.K_RIGHT]:
            if self.speed < -10:
                self.speed = -10
            elif self.speed < 0:
                self.speed += 0.5
            if self.speed > 10:
                self.speed = 10
            elif self.speed > 0:
                self.speed -= 0.5     
        rect = self.collision
        rect.y += self.speedy
        collist = []
        collist = self.collision_test(rect,pl,saws)
                    
        for co in collist:
            
            if self.speedy > 0:
                self.collision.bottom = co.top
                self.collisions['bottom'] = True
                self.y = self.collision.top
                #self.speedy = 0

            if self.speedy < 0 :
                self.collision.top = co.bottom
                self.collisions['top'] = True
                self.y = self.collision.top
                self.speedy = 0

        if not self.collisions['bottom'] and not self.climb:
            self.speedy += 1.5
            self.jump = True
        else:
            if self.speedy >=37:
                self.dead = 3
            self.jump = False
            self.speedy = 1

            
        rect = self.collision
        rect.x += self.speed
        collist = []
        collist = self.collision_test(rect,pl,saws)
        for co in collist:
                if self.speed > 0:
                    self.collision.right = co.left
                    self.collisions['right'] = True
                    self.x = self.collision.left
                    self.speed = 0
                    self.climb_test(co,1)
                if self.speed < 0 :
                    self.collision.left = co.right
                    self.collisions['left'] = True
                    self.x = self.collision.left
                    self.speed = 0
                    self.climb_test(co,-1)
                    
        if self.climb:
            self.speed = 0
            self.speedy = 0

        #print(self.collisions)
        if not self.collisions['right'] or not self.collisions['left']:
                self.x += self.speed
                self.collision.x = self.x
        if not self.collisions['bottom'] or not self.collisions['top']:
                self.y += self.speedy
                self.collision.y = self.y
        #print(self.speedy)
    def collision_test(self,rect,posb,poss):
        collist = []
        for i in pl:
            if rect.colliderect(i.collision):
                    collist.append(i.collision)
        for i in saws:
            if i.collision is not None:
                if rect.colliderect(i.collision):
                    self.dead = 4
        for i in broken_saws:
            if i.can_hurt:
                if rect.colliderect(i.collision):
                    self.dead = 4
        for i in flys:
            if rect.colliderect(i.collision):
                s = i.speeds[1]
                if s >20:
                    self.dead = 3
        for i in bull:
            if rect.colliderect(i.collision):
                i.collided = True
                self.dead = 5
        return collist
    def climb_test(self,block,side):
        self.climb_side = side
        col = self.collision
        if side == -1:
            col.left = block.center[0]
        else:
            col.right = block.center[0]
        col.bottom = block.top
        if not self.collisions['bottom']:
            if self.y < block.y:
                for i in pl:
                    if col.colliderect(i.collision):
                        if i.collision is block: 
                            self.climb = True
                        else:
                            self.climb = False
                            break
                    else:
                        self.climb = True
                self.y = block.y-12
                self.collision.y = self.y
    def atack_test(self):
        if not self.flip_sprite:
            self.atack_collision = pg.Rect(self.collision.center[0]+20,self.collision.center[1]-20,70,30)
        else:
            self.atack_collision = pg.Rect(self.collision.center[0]-90,self.collision.center[1]-20,70,30)

        for i in saws:
            if i.collision is not None:
                if self.atack_collision.colliderect(i.collision):
                    i.life -= 1
        for f in flys:
            if self.atack_collision.colliderect(f.collision):
                f.life -= 1
                print(f'xazam {f.life}')
class block():
    def __init__(self,xy,wh):
        self.x = xy[0]
        self.y = xy[1]
        self.w = wh[0]
        self.h = wh[1]
        self.collision = pg.Rect(self.x,self.y,self.w,self.h)
    def set_xy(self,xy):
        self.x = xy[0]
        self.y = xy[1]
    def draw(self,screen):
        pg.draw.rect(screen,(0,200,0),self.collision)
class torn_saw():
    def __init__(self,saw):
        self.image = load_img('broken_saw.png')
        self.collision = pg.Rect(saw.collision.x,saw.collision.y,55,54)
        self.collisions = {'top':False,'bottom':False,'right':False,'left':False}
        self.can_hurt = True
        self.flip_sprite = False
        self.speeds = [0,0] 
    def draw(self,screen):
        #pg.draw.rect(screen,(255,40,0),self.collision)
        if self.flip_sprite:
            screen.blit(pg.transform.flip(self.image,True,False),(self.collision.x,self.collision.y))
        else:
            screen.blit(self.image,(self.collision.x,self.collision.y))
    def update(self):

        if self.can_hurt:
            if self.speeds[0] != 0 and self.speeds[1] != 0 or not self.collisions['bottom']:
                self.collision_test()
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
    def collision_test(self):
        self.collision.x += self.speeds[0]
        for b in pl:
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
            if self.collision.colliderect(b.collision):
                if self.speeds[1] > 0 :
                    self.collision.bottom = b.collision.top
                    self.collisions['bottom'] = True
                else:
                    self.collision.top = b.collision.bottom
                    self.collisions['top'] = True
                self.speeds[1] = 0
    
class saw():
    def __init__(self,block):
        self.x = 0
        self.y = 0
        self.life = 45
        self.deactived = False
        self.block = block
        self.image = load_img('saw.png')
        self.collision = pg.Rect(self.x,self.y,55,60)
    def start(self):
        self.deactived = False
        self.life = 45
        self.image = load_img('saw.png')
        self.collision = pg.Rect(self.x,self.y,55,60)
        self.collision.center = self.block.collision.center
        self.collision.bottom = self.block.collision.top
        self.x = self.collision.x
        self.y = self.collision.y
    def update(self):
        if self.life == 0 and not self.deactived:
            self.deactived = True
            self.deactive()
    def draw(self,screen):
##        if self.life != 0: 
##            pg.draw.rect(screen,(255,0,0),self.collision)
        screen.blit(self.image,(self.x,self.y))
    def deactive(self):
        ts = torn_saw(self)
        ts.throw()
        broken_saws.append(ts)
        self.collision = None
        self.image = load_img('broken_saw_holder.png')
        self.x = self.block.collision.center[0]
        self.y = self.block.collision.top-self.image.get_height()
        
class canon():
    def __init__(self,side,rect):
        self.x = 0
        self.y = 0
        self.side = side
        self.atack_time = 0
        self.image = load_img('canon.png')
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
            rect = pg.Rect(self.x,self.y,35,60)
            rect.center = self.block.center
            self.x = rect.x
            self.y = rect.y-20
            self.image = pg.transform.rotate(self.image,270)
        if self.side == 2:
            rect.center = self.block.center
            self.x = rect.x-20
            self.y = rect.y
        if self.side == 3:
            rect.center = self.block.center
            self.x = rect.x+20
            self.y = rect.y
            self.image = pg.transform.rotate(self.image,180)
        if self.side == 4:
            rect = pg.Rect(self.x,self.y,35,60)
            rect.center = self.block.center
            self.x = rect.x
            self.y = rect.y+20
            self.image = pg.transform.rotate(self.image,90)
        
    def set_xy(self,xy):
        self.x = xy[0]
        self.y = xy[1]
    def update(self):
        if self.atack_time == 200:
            b = bullet(self)
            b.start()
            bull.append(b)
            self.atack_time = 0
            
        else:
            self.atack_time +=1
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))
        
class bullet():
    def __init__(self,canon):
        self.x = 0
        self.y = 0
        self.canon = canon
        self.side = canon.side
        self.image = load_img('bullet.png')
        self.collision = pg.Rect(self.x,self.y,7,5)
        self.speed = 0
        self.speedy = 0
        self.collided = False
    def set_xy(self,xy):
        self.x = xy[0]
        self.y = xy[1]
    def update(self):
        if self.side == 1:
            self.speedy = -8
        elif self.side == 2:
            self.speed = -8
        elif self.side == 3:
            self.speed = 8
        elif self.side == 4:
            self.speedy = 8
        self.collision.x += self.speed
        self.collision.y += self.speedy
        self.x = self.collision.x
        self.y = self.collision.y
        self.collision_test()
    def collision_test(self):
        for b in pl:
            if self.collision.colliderect(b.collision):
                self.collided = True
                break
            
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))
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
        elif self.side == 2:
            self.x = self.canon.x
            self.y = self.canon.y+16
            self.collision.x = self.x
            self.collision.y = self.y
        elif self.side == 3:
            self.x = self.canon.x+60
            self.y = self.canon.y+16
            self.collision.x = self.x
            self.collision.y = self.y
            self.image = pg.transform.rotate(self.image,180)
        elif self.side == 4:
            self.collision = pg.Rect(self.x,self.y,5,7)
            self.x = self.canon.x+16
            self.y = self.canon.y+60
            self.collision.x = self.x
            self.collision.y = self.y
            self.image = pg.transform.rotate(self.image,90)
class fly():
    
    def __init__(self,block):
        self.image = load_img('fly.png')
        self.collision = pg.Rect(block.collision.center[0],block.collision.bottom,30,25)
        self.collisions = {'top':False,'bottom':False,'right':False,'left':False}
        self.speeds = [0,0]
        self.life = 5
        self.is_flying = False

    def draw(self,screen):
        if not self.is_flying:
            screen.blit(pg.transform.flip(self.image,False,True),(self.collision.x,self.collision.y))
        else:
            screen.blit(self.image,(self.collision.x,self.collision.y))
            
    def update(self,ppos,palive):
        spos = (self.collision.x,self.collision.y)
        dist = int((((spos[0] - ppos[0])**2 + (spos[1] - ppos[1])**2)**0.5)//1)
        if dist <=70*5 and spos[1] < ppos[1]:
            self.is_flying = True
        if self.is_flying:
            self.move(ppos,dist,palive)
         
    def move(self,target,dist,palive):
        spos = self.collision.center
        self.collision_test()
        if spos[1] < target[1] and dist<= 70*5 and palive:
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
        
    def collision_test(self):
        self.collisions = {'top':False,'bottom':False,'right':False,'left':False}
        self.collision.y += self.speeds[1]
        for b in pl:
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
        for b in pl:
            if self.collision.colliderect(b.collision):
                if self.speeds[0] > 0:
                    self.speeds[0] = 0
                    self.collision.right = b.collision.left
                    self.collisions['right'] = True
                elif self.speeds[0] < 0:
                    self.speeds[0] = 0
                    self.collision.left = b.collision.right
                    self.collisions['left'] = True

                    
class Control(object):
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.caption = caption
        self.fps = 30
        self.show_fps = True
        self.state = None
        self.color = (123,241,153)
    def update(self):
        self.screen.fill(self.color)
        player.update(self.clock.get_fps())
        for c in canons:
            c.update()
        for b in bull:
            b.update()
            if b.collided:
                bull.remove(b)
        for s in saws:
            s.update()
        for bs in broken_saws:
            bs.update()
        for f in flys:
            if f.life <= 0:
                flys.remove(f)
                break
            f.update(player.collision.center,(player.dead == 0))
        self.draw()
    def draw(self):
        player.draw(self.screen)
        for b in pl:
            b.draw(self.screen)
        for saw in saws:
            saw.draw(self.screen)
        for c in canons:
            c.draw(self.screen)
        for bl in bull:
            bl.draw(self.screen)
        for bs in broken_saws:
            bs.draw(self.screen)
        for f in flys:
            f.draw(self.screen)
    def restart(self):
        player.dead = 0
        player.speed = 0
        player.speedy = 0
        player.x = 400
        player.y = 100
        broken_saws = []
        for s in saws:
            s.start()
    def event_loop(self):
        player.move(pg.key.get_pressed(),pg.mouse.get_pos())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.restart()
    def main(self):

        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = '{} - {:.2f} FPS'.format(self.caption,fps)
                pg.display.set_caption(with_fps)


player = player()

pl = []
pl.append(block((0,0),(1600,2)))
pl.append(block((0,598),(800,50)))
pl.append(block((0,0),(2,600)))
pl.append(block((798,0),(2,600)))
pl.append(block((100,460),(70,70)))
pl.append(block((170,390),(70,70)))
pl.append(block((240,320),(70,70)))
pl.append(block((310,250),(70,70)))
pl.append(block((380,180),(70,70)))
pl.append(block((450,110),(70,70)))
pl.append(block((520,320),(70,70)))
pl.append(block((590,320),(70,70)))
pl.append(block((660,320),(70,70)))
saws = []
s = saw(pl[7])
s.start()
s2 = saw(pl[11])
s3 = saw(pl[12])
s2.start()
s3.start()
saws.append(s2)
saws.append(s3)
saws.append(s)
broken_saws = []
canons = []
canons.append(canon(3,pl[4]))
canons.append(canon(1,pl[6]))
canons.append(canon(2,pl[5]))
canons.append(canon(4,pl[9]))
flys = []
f = fly(pl[10])
flys.append(f)
for c in canons:
    c.start()
bull = []
c = Control('teste')
c.main()
pg.quit()
