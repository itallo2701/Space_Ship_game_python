import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event,ai_settings,screen,ship,bullets):
	"""Responds to keystrokes."""
	if event.key == pygame.K_RIGHT:
		#Move a espaçonave para a direita.
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()



def fire_bullet(ai_settings,screen,ship,bullets):
	"""fire a projectile if the limit has not yet been reached."""
		#Create a new projectile and add it to the projectile group
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)
		
		
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""Updates the position of projectiles and gets rid of old projectiles."""
	#Update projectile positions
	bullets.update()
	#Get rid of missing projectiles
	for bullet in bullets.copy():
			if bullet.rect.bottom <= 0:
				bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)
	

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
	if len(aliens) == 0:
		#Destroys existing projectiles and iniciate a new level
		bullets.empty()
		#increase speed on the game
		ai_settings.increase_speed()
		#increase a level
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings,screen,ship,aliens)
		
def check_high_score(stats,sb):
	"""Checks for a new high score."""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
		

def check_keyup_events(event,ship):
	"""Responds to key releases."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	
	
def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
	"""Responds to key and mouse press events."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)			
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
			

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
	"""start a new game when player clicks Play."""
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		#Resets the settings match
		ai_settings.initialize_dynamic_settings()
		#Hide the mouse cursor
		pygame.mouse.set_visible(False)
		#Resets game stats
		stats.reset_stats()
		stats.game_active = True
		#Resets the scoreboard images
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		#Empty the list of aliens and projectiles
		aliens.empty()
		bullets.empty()
		#create a new fleet and centralized the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		

def get_number_alien_x(ai_settings,alien_width):
	"""Determines the number of aliens that can fit in a line."""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
	
def create_alien(ai_settings, screen, aliens, alien_number,row_number):
    """Create an alien, and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
	
	
def create_fleet(ai_settings,screen ,ship ,aliens):
	"""Create a complete fleet of aliens"""
	#Create an alien and calculate the number of aliens in a row
	#O spacing between aliens is equal to the width of an alien
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,alien.rect.height)
	
	for row_number in range(number_rows):		
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,row_number)
			
			
def get_number_rows(ai_settings,ship_height, alien_height):
	"""Determines the number of lines with aliens that fit on the screen."""
	available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
	number_rows = int(available_space_y / (2*alien_height))
	return number_rows 


def check_fleet_edges(ai_settings,aliens):
	"""respond appropriately if some alien has reached an edge."""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
			

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Checks if any aliens have reached the bottom of the screen."""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#Treat this case in the same way what is done when the spacecraft is hit
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
			break


def change_fleet_direction(ai_settings,aliens):
	"""Makes the whole fleet descend and changes its direction"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
	
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""It responds to the fact that the spacecraft has been hit by a alien."""
	"""Responds to the fact that the spacecraft was hit by a alien."""
	if stats.ships_left > 0:	
		#Decrease ships_left
		stats.ships_left -= 1
		#Updates the scoreboard
		sb.prep_ships()
		#Empty the list of aliens and projectiles
		aliens.empty()
		bullets.empty()
		#Create a new fleet and centralize the spacecraft
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		#take a break
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		
		
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
	"""Updates the images on the screen and switches to the new screen."""
	# Redraw the screen each time the loop passes
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	#Draw the score information
	sb.show_score()
	#draw the play button if the game inative
	if not stats.game_active:
		play_button.draw_button()
	#Makes the most recent screen visible
	pygame.display.flip()
	

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Updates the positions of all aliens in the fleet."""
	check_fleet_edges(ai_settings,aliens)
	#Checks for any aliens that have reached the bottom of the screen
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
	aliens.update()
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
	#Checks for any aliens that have reached the bottom of the screen
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,bullets)
