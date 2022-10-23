import pygame
from settings import *
# sprites define level sprites with collision and without collision

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.2, -self.rect.height*0.75) # 为物体创建碰撞
