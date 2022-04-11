class GameStats():
	"""Stores Alien Invasion statistics."""
	def __init__(self,ai_settings):
		"""initialize data statistics."""
		self.ai_settings = ai_settings
		self.reset_stats()
		#start the game in inative mode 
		self.game_active = False 
		# The maximum score should never be reset
		self.high_score = 0
		
	def reset_stats(self):
		"""Initializes statistical data that can change during the game."""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
		
		
		
		
