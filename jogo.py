import pygame
from data import loop
try:
    pygame.init()
except:
    print('Falhou a inicialização do modulo principal')
    
main = loop.Control('Jaame')
main.main()
pygame.quit()

