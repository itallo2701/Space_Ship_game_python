import pygame

from pygame.sprite import Sprite

class Ship(Sprite):
	def __init__(self,ai_settings,screen):
		"""Initializes the spacecraft and sets its starting position."""
		super(Ship,self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		#Load the spacecraft image and get its rect
		self.image = pygame.image.load('img/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		#Starts each new spaceship at the bottom center of the screen
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		#Stores a decimal value for the center of the spacecraft
		self.center = float(self.rect.centerx)
		self.moving_right = False
		self.moving_left = False
	
	
	def update(self):
		"""Updates the spaceship's position according to the movement flag."""
		#Updates the value of the spaceship center, not the rectangle
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
		#Updates rect object according to self.center
		self.rect.centerx = self.center
 
 
	def blitme(self):
		"""Draw the spacecraft in its current position."""
		self.screen.blit(self.image, self.rect)
	
	
	def center_ship(self):
		"""Centers the spacecraft on the screen."""
		self.center = self.screen_rect.centerx
		
	
	
