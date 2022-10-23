import pygame
from support import *
from timer import Timer
import random
from sprites import *
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, npc_sprites):
        super().__init__(group)
        self.status = "down_idle"
        self.frame_index = 0
        self.import_assets()
        self.z = LAYERS['main']
        self.win = False
        self.lose = False

        # collision
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.collision_sprites = collision_sprites
        self.npc_sprites = npc_sprites

        # create physical motion
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 200
        self.pos = pygame.math.Vector2(self.rect.center)

        # timers for game timers (Maybe more suitable in level)
        self.timers = {'game_Time': Timer(300, None)}

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
						   'right_idle':[], 'left_idle':[], 'up_idle':[], 'down_idle':[]
						  }

        for animation in self.animations.keys():
            full_path = 'asset/graphics/character/player/' + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
            self.status = 'down_idle'
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

    def move(self, dt):
        if self.direction.magnitude()>0:
            self.direction = self.direction.normalize()

        # horizontal movement:
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement:
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def collision(self, direction):
        # collision detect
        for sprite in self.npc_sprites:
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox) and type(sprite) == Enemy:
                    self.lose = True
                elif sprite.hitbox.colliderect(self.hitbox) and type(sprite) == Company:
                    self.win = True

        for sprite in self.collision_sprites:
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        if not (self.win or self.lose):
            self.input()
        else:
            self.direction.x = 0
            self.direction.y = 0
            if self.lose:
                self.status = 'down_idle'
            else:
                self.status = 'up_idle'
        self.move(dt)
        self.animate(dt)
        self.update_timer()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):  # set into this group
        super().__init__(group)

        self.status = "down_idle"
        self.frame_index = 0
        self.import_assets()
        self.z = LAYERS['main']

        # create a simple surface with collision(hitbox)
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate((-126, -70))
        # collision
        self.collision_sprites = collision_sprites

        # create physical motion
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 100
        self.pos = pygame.math.Vector2(self.rect.center)

        # timers for game timers (Maybe more suitable in level)
        self.timers = {'npc_time': Timer(1000, None)} # npc move 2s 1 time

    def import_assets(self):
        # this is important
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': []
                            }

        for animation in self.animations.keys():
            full_path = 'asset/graphics/character/enemy/' + animation
            self.animations[animation] = import_folder(
                full_path)

    def input(self):
        if not self.timers['npc_time'].active:
            self.timers['npc_time'].activate()
            self.direction.x = random.randint(-1, 1)  # AI move design
            self.direction.y = random.randint(-1, 1)  # AI move design
            sta_y = ['up', 'down_idle', 'down']
            self.status = sta_y[int(self.direction.y + 1)]
            sta_x = ['left', self.status, 'right']
            self.status = sta_x[int(self.direction.x + 1)]

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement:
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement:
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def collision(self, direction):
        # collision_detect
        for sprite in self.collision_sprites:
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.update_timer()


class Company(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):  # set into this group
        super().__init__(group)

        self.status = "down_idle"
        self.frame_index = 0
        self.import_assets()

        self.z = LAYERS['main']

        # collision
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate((-126, -70))
        # collision
        self.collision_sprites = collision_sprites

        # create physical motion
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 50
        self.pos = pygame.math.Vector2(self.rect.center)

        self.timers = {'npc_time': Timer(1000, None)} # npc move 2s one time

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': []
                            }

        for animation in self.animations.keys():
            full_path = 'asset/graphics/character/company/' + animation
            self.animations[animation] = import_folder(
                full_path)

    def input(self):
        if not self.timers['npc_time'].active:
            self.timers['npc_time'].activate()
            self.direction.x = random.randint(-1, 1) # AI move design
            self.direction.y = random.randint(-1, 1) # AI move design
            sta_y = ['up', 'down_idle', 'down']
            self.status = sta_y[int(self.direction.y + 1)]
            sta_x = ['left', self.status, 'right']
            self.status = sta_x[int(self.direction.x + 1)]

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement:
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement:
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.update_timer()


