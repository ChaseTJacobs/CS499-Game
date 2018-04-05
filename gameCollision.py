import sys
import pygame
from pygame.locals import *
from random import *
from math import pi


TRANSPARENT = (0,0,0,0)
BACKGROUND_COLOR = [255, 255, 255]
HEIGHT = 740
WIDTH = 800
RED = [255,0,0]
BLUE = [0,0,255]
GREEN = [0,255,0]

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,file_name,*groups):
		super(Player,self).__init__(*groups)
		self.pos = pos
		self.image = pygame.image.load(file_name)
		self.mapping = {
			"up": [(64 * i, 524, 64, 63) for i in range(0,9)],
			"left": [(64 * i, 588, 64, 61) for i in range(0,9)],
			"down": [(64 * i, 652, 64, 63) for i in range(0,9)],
			"right": [(64 * i, 716, 64, 63) for i in range(0,9)],
		}
		self.facing = "up"
		self.fBallCD = 25
		self.fBall = 50
		self.teleDistance = 75
		self.tele = 101
		self.teleCD = 100
		self.health = 100
		#self.image = pygame.Surface((30,30)).convert_alpha()
		#self.image.fill(TRANSPARENT)
		#self.image.fill([255,0,0])
		#pygame.draw.rect(self.image,(0,0,0),[20, 20, 20, 20])
		self.rect = self.image.get_rect(center = self.pos)
		self.mask = pygame.mask.from_surface(self.image)
		self.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
		self.vx = 4
		self.vy = 4
		self.pushX = 0
		self.pushY = 0
		self.direction = 90
		self.frame = 0
		self.speed = 0

	def teleport(self):
		self.tele = 0
		if self.direction == 0:
			self.rect.y -= self.teleDistance
		elif self.direction == 45:
			self.rect.x += self.teleDistance * .75
			self.rect.y -= self.teleDistance * .75
		elif self.direction == 90:
			self.rect.x += self.teleDistance
		elif self.direction == 135:
			self.rect.x += self.teleDistance * .75
			self.rect.y += self.teleDistance * .75
		elif self.direction == 180:
			self.rect.y += self.teleDistance
		elif self.direction == 225:
			self.rect.x -= self.teleDistance * .75
			self.rect.y += self.teleDistance * .75
		elif self.direction == 270:
			self.rect.x -= self.teleDistance
		elif self.direction == 315:
			self.rect.x -= self.teleDistance * .75
			self.rect.y -= self.teleDistance * .75

	def set_direction(self,key):
		print(key)

	def draw(self,surface):
		self.frame = (self.frame + self.speed) % 9
		if self.pushX > 0:
			self.pushX -= .5
			if self.pushX < 0:
				self.pushX = 0
		if self.pushX < 0:
			self.pushX += .5
			if self.pushX > 0:
				self.pushX = 0
		if self.pushY > 0:
			self.pushY -= .5
			if self.pushY < 0:
				self.pushY = 0
		if self.pushY < 0:
			self.pushY += .5
			if self.pushY > 0:
				self.pushY = 0
		self.rect.x += self.pushX
		self.rect.y += self.pushY
		surface.blit(self.image, (self.rect.x, self.rect.y, 200,100), self.mapping[self.facing][int(self.frame)])
		self.mask = pygame.mask.from_surface(self.image.subsurface(self.mapping[self.facing][int(self.frame)]))

class Fireball(pygame.sprite.Sprite):
	def __init__(self,pos,color,direction, *groups):
		super(Fireball,self).__init__(*groups)
		self.pos = pos
		self.direction = direction
		self.color = color
		self.image = pygame.Surface((20,20)).convert_alpha()
		self.image.fill(TRANSPARENT)
		pygame.draw.circle(self.image,self.color,(10,10),10)
		self.rect = self.image.get_rect(center = self.pos)
		self.mask = pygame.mask.from_surface(self.image)
		self.xDir = 0
		self.yDir = 0

		if self.direction == 0:
			self.yDir = -15
		elif self.direction == 45:
			self.xDir = 11
			self.yDir = -11
		elif self.direction == 90:
			self.xDir = 15
		elif self.direction == 135:
			self.xDir = 11
			self.yDir = 11
		elif self.direction == 180:
			self.yDir = 15
		elif self.direction == 225:
			self.xDir = -11
			self.yDir = 11
		elif self.direction == 270:
			self.xDir = -15
		elif self.direction == 315:
			self.xDir = -11
			self.yDir = -11

	def draw(self, surface):
		self.rect.x += self.xDir
		self.rect.y += self.yDir
		surface.blit(self.image, self.rect)

class Fireball2(pygame.sprite.Sprite):
	def __init__(self,pos,color,direction, *groups):
		super(Fireball2,self).__init__(*groups)
		self.pos = pos
		self.direction = direction
		self.color = color
		self.image = pygame.Surface((20,20)).convert_alpha()
		self.image.fill(TRANSPARENT)
		pygame.draw.circle(self.image,(255,0,255),(10,10),10)
		self.rect = self.image.get_rect(center = self.pos)
		self.mask = pygame.mask.from_surface(self.image)
		self.xDir = 0
		self.yDir = 0

		if self.direction == 0:
			self.yDir = -15
		elif self.direction == 45:
			self.xDir = 11
			self.yDir = -11
		elif self.direction == 90:
			self.xDir = 15
		elif self.direction == 135:
			self.xDir = 11
			self.yDir = 11
		elif self.direction == 180:
			self.yDir = 15
		elif self.direction == 225:
			self.xDir = -11
			self.yDir = 11
		elif self.direction == 270:
			self.xDir = -15
		elif self.direction == 315:
			self.xDir = -11
			self.yDir = -11

	def draw(self, surface):
		self.rect.x += self.xDir
		self.rect.y += self.yDir
		surface.blit(self.image, self.rect)



class Game:
	def __init__(self):
		#initializing the display screen and establishing two surfaces: one for playing and
		#one for player stats and information
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32)
		self.arena = pygame.surface.Surface((WIDTH, HEIGHT - 100))
		self.stats = pygame.surface.Surface((WIDTH, 100))
		for x in range(200):
			c = int((x/199.)*255.)
			red = (c, 0, 0)
			green = (0, c, 0)
			blue = (0, 0, c)
			black = (0,0,0)
			player1_health = Rect(x, 0, 200, 40)
			player2_health = Rect(400+x, 0, 200, 40)
			line_rect = Rect(x, 0, 1, 100)
			# pygame.draw.rect(self.arena, red, line_rect)
			pygame.draw.rect(self.stats, black, line_rect)
			pygame.draw.rect(self.stats, green, player1_health)
			pygame.draw.rect(self.stats, blue, player2_health)

		#setting up the sprites that we are going to use as our players
		self.player1 = Player((600,700),"green_hair.png")
		self.player2 = Player((800, 900), "white_hair.png")
		self.player2.move = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]

		#setting the background and creating an inverted mask of the paths
		self.background = pygame.image.load("lava-terrain.png").convert()
		self.gravel_path = pygame.image.load("gravel-path.png").convert()
		self.terrain_mask = pygame.mask.from_surface(self.gravel_path).invert()

		self.bullet_group1 = pygame.sprite.Group()
		self.bullet_group2 = pygame.sprite.Group()
		self.done = False
		self.fps = 30.0
		self.clock = pygame.time.Clock()

		#adding some tunes to the game so it's not so boring
		pygame.mixer.music.load('backgroundMusic.ogg')
		pygame.mixer.music.set_volume(0.4)
		pygame.mixer.music.play()
		self.swoosh = pygame.mixer.Sound('fireball.wav')
		self.swoosh.set_volume(.7)


	def event_loop(self):
		key = pygame.key.get_pressed()
		for i in range(2):
			if key[self.player1.move[i]]:
				self.player1.rect.x += self.player1.vx * [-1, 1][i]

		for i in range(2):
			if key[self.player1.move[2:4][i]]:
				self.player1.rect.y += self.player1.vy * [-1, 1][i]

		for i in range(2):
			if key[self.player2.move[i]]:
				self.player2.rect.x += self.player2.vx * [-1, 1][i]

		for i in range(2):
			if key[self.player2.move[2:4][i]]:
				self.player2.rect.y += self.player2.vy * [-1, 1][i]

		for event in pygame.event.get():
			key = pygame.key.get_pressed()
			if key[32] and self.player1.fBall >= self.player1.fBallCD:
				Fireball((self.player1.rect.x + 32,self.player1.rect.y + 32),RED,self.player1.direction,self.bullet_group1)
				print("x: ", self.player1.rect.x)
				print("y: ", self.player1.rect.y)
				self.player1.fBall = 0
				self.swoosh.play()
			if key[304] and self.player2.fBall >= self.player2.fBallCD:
				Fireball2((self.player2.rect.x + 32,self.player2.rect.y + 32),BLUE,self.player2.direction,self.bullet_group2)
				self.player2.fBall = 0
				self.swoosh.play()
			if key[109] and self.player1.tele > self.player1.teleCD:
				self.player1.teleport()
			if key[122] and self.player2.tele > self.player2.teleCD:
				self.player2.teleport()

#			m = 109
#			z = 122
#			up = 273
#			down = 274
#			Right = 275
#			left = 276
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				self.player2.speed = 0.3
				self.player1.speed = 0.3
				if event.key == pygame.K_LEFT:
					self.player1.facing = "left"
					if key[273]:
						self.player1.direction = 315
					elif key[274]:
						self.player1.direction = 225
					else:
						self.player1.direction = 270
				elif event.key == pygame.K_RIGHT:
					self.player1.facing = "right"
					if key[273]:
						self.player1.direction = 45
					elif key[274]:
						self.player1.direction = 135
					else:
						self.player1.direction = 90
				if event.key == pygame.K_UP:
					if key[275]:
						self.player1.direction = 45
					elif key[276]:
						self.player1.direction = 315
					else:
						self.player1.direction = 0
						self.player1.facing = "up"
				elif event.key == pygame.K_DOWN:
					if key[275]:
						self.player1.direction = 135
					elif key[276]:
						self.player1.direction = 225
					else:
						self.player1.direction = 180
						self.player1.facing = "down"
				if event.key == pygame.K_a:
					self.player2.facing = "left"
					if key[119]:
						self.player2.direction = 315
					elif key[115]:
						self.player2.direction = 225
					else:
						self.player2.direction = 270
				elif event.key == pygame.K_d:
					self.player2.facing = "right"
					if key[119]:
						self.player2.direction = 45
					elif key[115]:
						self.player2.direction = 135
					else:
						self.player2.direction = 90
				if event.key == pygame.K_w:
					if key[100]:
						self.player2.direction = 45
					elif key[97]:
						self.player2.direction = 315
					else:
						self.player2.direction = 0
						self.player2.facing = "up"
				elif event.key == pygame.K_s:
					if key[100]:
						self.player2.direction = 135
					elif key[97]:
						self.player2.direction = 225
					else:
						self.player2.direction = 180
						self.player2.facing = "down"
			elif event.type == pygame.KEYUP:
				if not key[275] and not key[276]:
					if key[273]:
						self.player1.facing = "up"
						self.player1.direction = 0
					elif key[274]:
						self.player1.facing = "down"
						self.player1.direction = 180
				if not key[273] and not key[274]:
					if key[275]:
						self.player1.facing = "right"
						self.player1.direction = 90
					elif key[276]:
						self.player1.facing = "left"
						self.player1.direction = 270
				if not key[100] and not key[97]:
					if key[119]:
						self.player2.facing = "up"
						self.player2.direction = 0
					elif key[115]:
						self.player2.facing = "down"
						self.player2.direction = 180
				if not key[119] and not key[115]:
					if key[100]:
						self.player2.facing = "right"
						self.player2.direction = 90
					elif key[97]:
						self.player2.facing = "left"
						self.player2.direction = 270

#			w 119 up
#			a 97  left
#			s 115 down
#			d 100 right
#			up = 273
#			down = 274
#			Right = 275
#			left = 276


#			for idx, k in enumerate(key):
#				if k != 0:
#					print(idx)

			if not key[273] and not key[274] and not key[275] and not key[276]:
				self.player1.speed = 0
				self.player1.frame = 0
			if not key[119] and not key[97] and not key[115] and not key[100]:
				self.player2.speed = 0
				self.player2.frame = 0

	def check_collide(self):
		p1Col = pygame.sprite.spritecollide(self.player1,self.bullet_group2,True,pygame.sprite.collide_mask)
		if p1Col:
			self.player1.pushX = p1Col[0].xDir
			self.player1.pushY = p1Col[0].yDir
			return False
		p2Col = pygame.sprite.spritecollide(self.player2,self.bullet_group1,True,pygame.sprite.collide_mask)
		if p2Col:
			self.player2.pushX = p2Col[0].xDir
			self.player2.pushY = p2Col[0].yDir
			return False

		# if (pygame.sprite.collide_mask(self.player1,self.terrain_mask)):
		# 	self.player1.health -= 2
		# 	if self.player1.health > 0:
		# 		return False
		# 	elif self.player1.health <= 0:
		# 		return True
		# elif(pygame.sprite.collide_mask(self.player2,self.terrain_mask)):
		# 	self.player2.health -= 2
		# 	if self.player2.health > 0:
		# 		return False
		# 	elif self.player2.health <= 0:
		# 		return True


	def draw(self):
		self.screen.blit(self.arena, (0, 00))
		self.screen.blit(self.stats, (0, HEIGHT - 100))
		self.arena.blit(self.background, (0,0))
		self.player1.draw(self.screen)
		self.player2.draw(self.screen)
		for bullet in self.bullet_group1:
			bullet.draw(self.screen)
		for bullet2 in self.bullet_group2:
			bullet2.draw(self.screen)

	def run(self):
		while not self.done:
			self.event_loop()
			self.player1.fBall += 1
			self.player2.fBall += 1
			self.player1.tele += 1
			self.player2.tele += 1
			self.draw()
			if self.check_collide():
				self.done = True
			pygame.display.update()
			self.clock.tick(self.fps)


if __name__ == '__main__':
	pygame.init()
	game = Game()
	game.run()
	pygame.mixer.music.stop()
	pygame.quit()
