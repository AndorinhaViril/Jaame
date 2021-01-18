import data.constants as c
import os
import pygame as pg
class animation():
	def __init__(self):
		self.player_sprites = []
		self.fly_sprites  = []
		self.canonbullet_sprites = []
		self.blocks_sprites = []
		self.cont = 0
		self.x = 100
		self.y = 100
	def load_sprites(self):
		self.blocks_sprites.append(pg.image.load(os.path.join('resources\graphics', 'dirt.png')))
		self.blocks_sprites.append(pg.image.load(os.path.join('resources\graphics', 'grass.png')))
		self.player_sprites.append(pg.image.load(os.path.join('resources\graphics', 'player.png')))	
		self.player_sprites.append(pg.image.load(os.path.join('resources\graphics', 'player2.png')))
	def menu(self, screen):
		screen.blit(self.player_sprites[self.cont],(self.x,self.y))
		screen.blit(self.blocks_sprites[self.cont],(self.x,self.y+55))
		if self.cont == 0:
			self.cont = 1
		else:
			self.cont = 0
	def load(self):#precisa de um sistema multithread
		pass