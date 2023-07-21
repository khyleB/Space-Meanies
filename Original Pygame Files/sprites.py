import pygame
import random
from settings import Settings
from settings import WebColours

# Useful commands: pygame.transform.scale(player_img, (x, y))

game_settings = Settings() 
wc = WebColours()
class PlayerSprite(pygame.sprite.Sprite):
	def __init__(self, screen):
		pygame.sprite.Sprite.__init__(self)
			#Calls 'sprite initializer'
		self.image = pygame.image.load('sprites/s2.bmp').convert()
		self.image_flip = pygame.transform.flip(self.image, True, False)
		# The True flips along one axis, False stops it from flipping on both axes
		self.image.set_colorkey(game_settings.BG)
		self.image_flip.set_colorkey(game_settings.BG)
			# Before you have an image, you can make a placeholder square with these:
			# self.sprite = pygame.Surface((50, 50))
			# self.sprite.fill(CYAN)
		self.rect = self.image.get_rect()
			# Looks at the dimensions of the image and determines the appropriate
			# 'hitbox' (rectangle) to define it by.
		self.radius = 45
		self.game_screen = screen
			#This has to do with putting your image in a rectangle, relatsing to its hitbox I assume
		self.screen_rect = screen.get_rect()
			#Oh ok this one is for the whole screen rectangle and the above was for the item rectangle I think
			#Also I don't remember us defining a screen class so...it just stores this on its own, or I missed something.
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
			#Vaguely confusing name structure but it's basically saying postion of ship = position of entire screen
			#Also: you  can do self.rect.center = (WIDTH / 2, HEIGHT / 2) if you have your
			#width and height stored in those variables, it divides the dimension of the screen
			#by 2, thus placing your sprite at the center.
		self.speedx = 0
		#self.speedy = 0
		self.y_speed = 1
		#self.shoot_delay = 250
		#self.last_shot = pygame.time.get_ticks()
		#self.shoot_sound = []
		#self.bullets = pygame.sprite.Group()
	
	def update(self):
		self.speedx = 0
		#self.speedy = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -10
		if keystate[pygame.K_RIGHT]:
			self.speedx = 10
		#if keystate[pygame.K_SPACE]:
		#	self.shoot
		#if keystate[pygame.K_UP]:
		#	self.speedy = -10
		#if keystate[pygame.K_DOWN]:
		#	self.speedy = 10
		if self.rect.right > game_settings.WIDTH:
			self.rect.right = game_settings.WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		#if self.rect.top > 635:
			#self.rect.top = 635
			#if you figure out how to refer to sprite dimensions,
			#this can be game_settings.HEIGHT - [sprite height dimension] instead.
		#if self.rect.bottom < 700:
			#self.rect.bottom = 700
		self.rect.x += self.speedx
		#self.rect.y += self.speedy
		self.rect.y += self.y_speed
		if self.rect.bottom > 790:
			self.y_speed = -1
		if self.rect.top < 670:
			self.y_speed = 1

	#def shoot(self):
	#	self.now = pygame.time.get_ticks()
	#	self.bullet = Bullet(self.rect.centerx, self.rect.top)
		#if self.now - self.last_shot > self.shoot_delay:
		#	self.last_shot = now
			
			#all_sprites.add(bullet)
				#if event.type == KEYDOWN:
		       #if event.key == K_ESCAPE:
		        #   pygame.quit()
		         #  return

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
			#x and y are so we can place the bullet on the ship
		pygame.sprite.Sprite.__init__(self)
		#self.bullets = pygame.sprite.Group()
		self.image = pygame.image.load('sprites/bullet2.bmp').convert()
		self.image.set_colorkey(game_settings.BG)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
			#speed will be used to add it along the y axis
			#adds self.rect.y to speedy
			#up and down movement - self.rect.y = self.speedy+self.rect.y
		if self.rect.bottom < 0:
			self.kill()
			#built-in function that gets rid of sprite

class Meanie(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		meanie_pics = []
		meanie_list = ['sprites/meanie.bmp', 'sprites/meanie2.bmp', 'sprites/meanie3.bmp']
		for img in meanie_list:
			meanie_pics.append(pygame.image.load(img).convert())
		self.image = random.choice(meanie_pics)
		self.image.set_colorkey(game_settings.BG)
		self.rect = self.image.get_rect()
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width / 2)
		self.rect.x = random.randrange(game_settings.WIDTH - self.rect.width)
			# Making them spawn somewhere off the screen (randomly spawning!)
			#Goes between 0 and the width (even if you don't write
			#"0, width"), minus the width of the sprite
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1,8)

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > game_settings.HEIGHT + 10:
			self.rect.x = random.randrange(game_settings.WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1,8)
				#Just puts it back to random top postion instead of making a new sprite

class Background(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('sprites/sky2.bmp')
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

class BackgroundDead(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('sprites/skydead.bmp')
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

	#OLD - revisit if needed:
	#def blitme(self):
		#self.game_screen.blit(self.sprite, self.rect)
		#Apparently this is for actually drawing the ship on the screen. Blit seems to be a built-in function
		#But I'm not sure what it stands for

		#if self.rect.left > game_settings.WIDTH - 735:
		#	self.x_speed = -3
		#if self.rect.right < 735:
		#	self.x_speed = 3
		#if self.rect.bottom < 0:
		#	self.rect.top = game_settings.HEIGHT