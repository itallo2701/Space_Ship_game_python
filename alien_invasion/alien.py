import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class that represents a single alien in the fleet."""
	def __init__(self,ai_settings, screen):
		"""Initializes the alien and sets your starting position."""
		super(Alien,self).__init__()
		self.screen = screen 
		self.ai_settings = ai_settings
		#Load the alien image and set its attribute
		self.image = pygame.image.load('img/alien.bmp')
		self.rect = self.image.get_rect()
		#Starts each new alien near the top left of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		#Stores the exact position of the alien
		self.x = float(self.rect.x)
		
	
	def check_edges(self):
		"""Returns true if alien is at the edge of the screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True 
	
	
	def update(self):
		"""Move the alien to right"""
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x
		
		
	def blitme(self):
		"""Draw the alien in its current position."""
		self.screen.blit(self.image, self.rect)
		

