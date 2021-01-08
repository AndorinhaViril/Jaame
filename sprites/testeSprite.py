'''
teste de animação /// nada de importante.
'''
import pygame as pg
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()

pg.display.set_caption('teste')
screen = pg.display.set_mode((800,600))
display = pg.display.get_surface()
timing = 10
cont_sprites = 0
WHITE = (90, 90, 0)
done = False
clock = pg.time.Clock()
sprites = []
sprites.append(pg.image.load(os.path.join('', 'parado.png')))
sprites.append(pg.image.load(os.path.join('', 'passo2.png')))
sprites.append(pg.image.load(os.path.join('', 'passo3.png')))
sprites.append(pg.image.load(os.path.join('', 'passo4.png')))
sprites.append(pg.image.load(os.path.join('', 'passo5.png')))
sprite  = sprites[0]
def run():
    global screen
    global display
    global done
    global clock
    global cont_sprites
    cont = 0
    while not done:
        display.fill(WHITE)
        event_loop()
        display.blit(pg.transform.scale2x(sprite), (cont,100))
        cont += 8
        if cont > 800:
            cont = 0
        update()
        clock.tick(60)
        pg.display.update()
def update():
    global timing
    global sprite
    global sprites
    global cont_sprites
    if timing <= 0:
        if cont_sprites == len(sprites)-1:
            cont_sprites = 1
        else:
            cont_sprites += 1
        timing = 10
        sprite = sprites[cont_sprites]
        print(f'{cont_sprites}')
    else:
        timing -= 1
        
def event_loop():
    global done
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
run()
pg.quit()
