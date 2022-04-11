import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
	"""A class that manages projectiles fired by the spaceship"""
	def __init__(self, ai_settings, screen, ship):
		"""Create an object for the projectile at the spacecraft's current position."""
		super(Bullet,self).__init__()
		self.screen = screen
		
		
		# Creates a rectangle for the projectile at (0, 0) and then sets the
		# correct position
		self.rect = pygame.Rect(0,0, ai_settings.bullet_width, ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		
		# Stores projectile position as a decimal value
		self.y = float(self.rect.y)
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor
		
		
	def update(self):
		"""move the projectile up on the screen."""
		# Updates the projectile decimal position
		self.y -= self.speed_factor
		# Updates the rect position
		self.rect.y = self.y
		
		
	def draw_bullet(self):
		"""Drawn the project on the screen"""
		pygame.draw.rect(self.screen,self.color,self.rect)
		
