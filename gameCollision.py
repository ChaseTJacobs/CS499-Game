import sys
import pygame

from random import *
from math import pi


TRANSPARENT = (0,0,0,0)
BACKGROUND_COLOR = [255, 255, 255]


class Player(pygame.sprite.Sprite):
	def __init__(self,pos,*groups):
		super(Player,self).__init__(*groups)
		self.pos = pos
		self.image = pygame.image.load("download.png")
		self.mapping = {
			"up": [(64 * i, 524, 64, 64) for i in range(0,9)],
			"left": [(64 * i, 588, 64, 64) for i in range(0,9)],
			"down": [(64 * i, 652, 64, 64) for i in range(0,9)],
			"right": [(64 * i, 716, 64, 64) for i in range(0,9)],
		}
		self.facing = "up"
		#self.image = pygame.Surface((30,30)).convert_alpha()
		#self.image.fill(TRANSPARENT)
		#self.image.fill([0,0,0])
		#pygame.draw.rect(self.image,(0,0,0),[20, 20, 20, 20])
		self.rect = self.image.get_rect(center = self.pos)
		self.mask = pygame.mask.from_surface(self.image)
		self.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
		self.vx = 5
		self.vy = 5
		self.direction = 90
		self.frame = 0
		self.speed = 0

	def movement(self,key):
		#print(key)
		for i in range(2):
			if key[self.move[i]]:
				self.rect.x += self.vx * [-1, 1][i]

		for i in range(2):
			if key[self.move[2:4][i]]:
				self.rect.y += self.vy * [-1, 1][i]
				
		
				
#		if key[0]:
#			self.fire_direction = 6
#			if(key[3] and !key[4]):
				
				
#		if key[32]:
#			print("Fire direction", self.direction)
#			self.vx = 1
#			self.vy = 1
#		else:				
#			self.vx = 5
#			self.vy = 5
			
	def set_direction(self,key):
		print(key)

	def draw(self,surface):
		self.frame = (self.frame + self.speed) % 9
		surface.blit(self.image, (self.rect.x, self.rect.y, 200,100), self.mapping[self.facing][int(self.frame)])


class Enemy(pygame.sprite.Sprite):
	def __init__(self,pos,*groups):
		super(Enemy,self).__init__(*groups)
		self.pos = pos
		self.image = pygame.Surface((100,100)).convert_alpha()
		self.image.fill(TRANSPARENT)
		pygame.draw.circle(self.image,(255,255,0),(30,30),30)
		self.rect = self.image.get_rect(center = self.pos)
		self.mask = pygame.mask.from_surface(self.image)
		self.slid_pos_x = 0
		self.slid_pos_y = 0
		self.counterx = randint(1,5)
		self.countery = randint(1,5)
		
	def draw(self, surface):
		self.slid_pos_x += self.counterx
		self.rect.x += self.counterx
		if self.slid_pos_x > 50:
			self.counterx = self.counterx * -1
		if self.slid_pos_x < -50:
			self.counterx = self.counterx * -1
		
		surface.blit(self.image, self.rect)
		
class Fireball(pygame.sprite.Sprite):
	def __init__(self,pos,*groups):
		super(Fireball,self).__init__(*groups)
		self.pos = pos
		self.image = pygame.Surface((20,20)).convert_alpha()
		self.image.fill(TRANSPARENT)
		pygame.draw.circle(self.image,(255,0,0),(10,10),10)
		self.rect = self.image.get_rect(center = self.pos)
		self.mask = pygame.mask.from_surface(self.image)
		
	def draw(self, surface):
		surface.blit(self.image, self.rect)


class Game:
	def __init__(self):
		self.screen = pygame.display.set_mode((800,600))
		self.player = Player((500,800))
		self.enemy_group = pygame.sprite.Group()
		self.bullet_group = pygame.sprite.Group()
		Enemy((300,250),self.enemy_group)
		Enemy((100,100),self.enemy_group)
		Enemy((500,400),self.enemy_group)
		Enemy((200,550),self.enemy_group)
		Enemy((500,150),self.enemy_group)
		Enemy((100,450),self.enemy_group)
		Enemy((700,400),self.enemy_group)
		self.done = False
		self.fps = 60.0
		self.clock = pygame.time.Clock()

	def event_loop(self):
		key = pygame.key.get_pressed() 
		self.player.movement(key)
		for event in pygame.event.get():
			key = pygame.key.get_pressed()
			if key[32]:
				print(self.player.rect.x)
				print(self.player.rect.y)
				Fireball((self.player.rect.x,self.player.rect.y), self.bullet_group)
#			up = 273
#			down = 274
#			Right = 275
#			left = 276
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				self.player.speed = 0.3
				if event.key == pygame.K_LEFT:
					self.player.facing = "left"
					if key[273]:
						self.player.direction = 315
					elif key[274]:
						self.player.direction = 225
					else:
						self.player.direction = 270
				elif event.key == pygame.K_RIGHT:
					self.player.facing = "right"
					if key[273]:
						self.player.direction = 45
					elif key[274]:
						self.player.direction = 135
					else:
						self.player.direction = 90
				if event.key == pygame.K_UP:
					if key[275]:
						self.player.direction = 45
					elif key[276]:
						self.player.direction = 315
					else:
						self.player.direction = 0
						self.player.facing = "up"
				elif event.key == pygame.K_DOWN:
					if key[275]:
						self.player.direction = 135
					elif key[276]:
						self.player.direction = 225
					else:
						self.player.direction = 180
						self.player.facing = "down"
			elif event.type == pygame.KEYUP:
				if not key[275] and not key[276]:
					if key[273]:
						self.player.facing = "up"
						self.player.direction = 0
					elif key[274]:
						self.player.facing = "down"
						self.player.direction = 180
			
			if not key[273] and not key[274] and not key[275] and not key[276]:
				self.player.speed = 0
				self.player.frame = 0

	def check_collide(self):
		if pygame.sprite.spritecollide(self.player,self.enemy_group,False,pygame.sprite.collide_mask):
			return False

	def draw(self):
		self.screen.fill(BACKGROUND_COLOR)
		self.player.draw(self.screen)
		for cur_sprite in self.enemy_group:
			cur_sprite.draw(self.screen)
		for bullet in self.bullet_group:
			bullet.draw(self.screen)

	def run(self):
#		joysticks = []
#		for i in range(0, pygame.joystick.get_count()):
#			joysticks.append(pygame.joystick.Joystick(i))
#			joysticks[-1].init()
#			print (joysticks[-1].get_name())
		while not self.done:
			self.event_loop()
			self.draw()
			if self.check_collide():
				self.done = True
			pygame.display.update()
			self.clock.tick(self.fps)


if __name__ == '__main__':
	pygame.init()
	game = Game()
	game.run()
	pygame.quit()