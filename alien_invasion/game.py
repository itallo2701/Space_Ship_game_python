import sys
import pygame

from pygame.sprite import Group  
from settings import Settings
from game_stats import GameStats
from ship import Ship
from alien import Alien
from button import Button
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
	"""Starts the game and creates an object for the screen"""
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	#create the player button
	play_button = Button(ai_settings,screen,"Play")
	#Create instance to store game statistics and create dashboard punctuation
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings,screen,stats)
	#create a spaceship
	ship = Ship(ai_settings,screen)
	#create a group in which the projectiles will be stored
	bullets = Group()
	aliens =  Group()
	#create a fleet of aliens
	gf.create_fleet(ai_settings,screen,ship,aliens)
	
	
	#Start the main game loop
	while True:
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship , aliens, bullets)
			gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
			
		#Redraw the screen with each pass through the loop
		gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)

run_game()
