import pygame 
from settings import *


class Sky:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.full_surf = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
		self.start_color = (39,101, 189)
		self.end_color = (38,101, 189)

	def display(self, dt):
		self.full_surf.fill(self.start_color)
		self.display_surface.blit(self.full_surf, (0,0), special_flags = pygame.BLEND_RGBA_MULT)


class Sky2:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.full_surf = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
		self.start_color = (90,121, 189)
		self.end_color = (90,121, 189)

	def display(self, dt):
		self.full_surf.fill(self.start_color)
		self.display_surface.blit(self.full_surf, (0,0), special_flags = pygame.BLEND_RGBA_MULT)

