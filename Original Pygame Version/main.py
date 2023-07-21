import sys
import pygame
import random
from settings import WebColours
from settings import Settings
from sprites import Background
from sprites import BackgroundDead
from sprites import PlayerSprite
from sprites import Meanie
from sprites import Bullet

game_settings = Settings()
wc = WebColours() 
screen = pygame.display.set_mode((game_settings.WIDTH,game_settings.HEIGHT))
bg = Background('sprites/sky2.bmp', [0,0])

font_name = pygame.font.match_font('arial')
score = 0
hit_count = 0

all_sprites = pygame.sprite.Group()
meanies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for i in range(8):
	meanie = Meanie()
	all_sprites.add(meanie)
	meanies.add(meanie)

def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, False, wc.WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)
	
# Initialize game and create a screen object.
pygame.init()
pygame.mixer.init()
	#NOTE - This is where we define a "screen" variable and this is why that's the variable name he used in the ship file
pygame.display.set_caption("Intergalactic Turboviolence")
clock = pygame.time.Clock()
	#Good luck having fps without calling THIS bad boy!!!

pygame.mixer.music.load('sounds/eggy_toast.wav')
pygame.mixer.music.set_volume(0.2)

shoot_sound = []
for snd in ['sounds/zap1.wav', 'sounds/zap2.wav']:
	shoot_sound.append(pygame.mixer.Sound(snd))
hit_sound = pygame.mixer.Sound('sounds/success.wav')

class SpaceShip(pygame.sprite.Sprite):
	def __init__(self, screen):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('sprites/s2.bmp').convert()
		self.image_flip = pygame.transform.flip(self.image, True, False)
		self.image.set_colorkey(game_settings.BG)
		self.image_flip.set_colorkey(game_settings.BG)
		self.rect = self.image.get_rect()
		self.radius = 45
		self.game_screen = screen
		self.screen_rect = screen.get_rect()
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		self.speedx = 0
		self.y_speed = 1
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
	
	def update(self):
		self.speedx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -10
		if keystate[pygame.K_RIGHT]:
			self.speedx = 10
		if keystate[pygame.K_SPACE]:
			self.shoot()
		if self.rect.right > game_settings.WIDTH:
			self.rect.right = game_settings.WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		self.rect.x += self.speedx
		self.rect.y += self.y_speed
		if self.rect.bottom > 790:
			self.y_speed = -1
		if self.rect.top < 670:
			self.y_speed = 1

	def shoot(self):
		global shoot_sound
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			random.choice(shoot_sound).play()
			bullet = Bullet(self.rect.centerx, self.rect.top)
			bullets.add(bullet)
			all_sprites.add(bullet)

space_ship = SpaceShip(screen)
all_sprites.add(space_ship)

def run_game():
	# Start the main loop for the game.
	global hit_count
	global score
	global bg
	pygame.mixer.music.play(loops=-1)
	running = True
	while running:
		clock.tick(game_settings.FPS)
		#manages timing of loop so it's evens out to 1 loop every 1/30th of a second

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					space_ship.image = space_ship.image_flip
				if event.key == pygame.K_LEFT:
					space_ship.image = pygame.image.load('sprites/s2.bmp').convert()
					space_ship.image.set_colorkey(game_settings.BG)
				if event.type == pygame.K_SPACE:
					shoot()
				if event.key == pygame.K_ESCAPE:
						running = False

		#Update step
		all_sprites.update()
		mean_hits = pygame.sprite.groupcollide(meanies, bullets, True, True)
		#True = deletes both the bullets and the mobs
		for hit in mean_hits:
			score += 1
			hit_sound.play()
			meanie = Meanie()
			all_sprites.add(meanie)
			meanies.add(meanie)
		hits = pygame.sprite.spritecollide(space_ship, meanies, False, pygame.sprite.collide_circle)
		#False = the mobs don't despawn when you hit them

		if hits:
			running = False

		# Draw step: redraw the screen during each pass through the loop
		screen.fill(game_settings.SPACE)
		screen.blit(bg.image, bg.rect)

		all_sprites.draw(screen)
		draw_text(screen, str(score), 24, game_settings.WIDTH / 2, 10)
			# Still fuzzy on the 'screen' relationship w sprites but I assume this is for
			# calculating their position within the screen's dimensions

		pygame.display.flip()
			# Make the most recently drawn screen visible.

def game_over():
	# Start the main loop for the game.
	global hit_count
	global score
	global bg
	pygame.mixer.music.play(loops=-1)
	running = True
	while running:
		clock.tick(game_settings.FPS)
		for bullet in bullets:
			bullet.kill()
		for meanie in meanies:
			meanie.kill()
		space_ship.kill()
		bg = BackgroundDead('sprites/skydead.bmp', [0,0])

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				running = False

		screen.fill(game_settings.SPACE)
		screen.blit(bg.image, bg.rect)
		draw_text(screen, str(score), 24, game_settings.WIDTH / 2, 10)
		pygame.display.flip()

start_noise = pygame.mixer.Sound('sounds/game_start.wav')
start_noise.play()
run_game()
game_over()
sys.exit()
# Goes after the game loop, bc game must exit the loop to quit. 
# Refer to running = False condition in game_functions.py