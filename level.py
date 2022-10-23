import pygame, sys
from settings import *
from player import Player, Enemy, Company
from sprites import Generic
from sky import Sky, Sky2
from timer import Timer

from pytmx.util_pygame import load_pygame

class Manu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        # sound choose
        self.manu_sound = pygame.mixer.Sound('asset/audio/manu_sound.wav')
        self.manu_sound.set_volume(0.8)
        self.playsound = False
        self.button_sound = pygame.mixer.Sound('asset/audio/button.wav')


    def run(self, dt):
        if self.playsound == False:
            self.manu_sound.play(loops=True)
            self.playsound = True
        self.display_surface.fill('blue')

        # my sound is:
        background = pygame.image.load("asset/graphics/manu/background.png")
        backgroundrect = background.get_rect(top=0, bottom=600, left=0, right=800, width=800, height=600)
        self.display_surface.blit(background, backgroundrect)

        self.r1rect = pygame.draw.rect(self.display_surface, (0, 255, 0), (300, 100, 200, 100), 3)
        self.r2rect = pygame.draw.rect(self.display_surface, (0, 255, 0), (300, 250, 200, 100), 3)
        self.r3rect = pygame.draw.rect(self.display_surface, (0, 255, 0), (300, 400, 200, 100), 3)
        startgame = pygame.image.load("asset/graphics/manu/start.png", )
        levelgame =  pygame.image.load("asset/graphics/manu/level.png")
        exitgame = pygame.image.load("asset/graphics/manu/exit.png")
        self.display_surface.blit(startgame, self.r1rect)
        self.display_surface.blit(levelgame, self.r2rect)
        self.display_surface.blit(exitgame, self.r3rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.r1rect.collidepoint(event.pos):
                    self.button_sound.play(loops=False)
                    self.manu_sound.stop()
                    self.playsound = False
                    return 2
                elif self.r2rect.collidepoint(event.pos):
                    self.button_sound.play(loops=False)
                    self.manu_sound.stop()
                    self.playsound = False
                    return 1
                elif self.r3rect.collidepoint(event.pos):
                    self.button_sound.play(loops=False)
                    sys.exit()
        return 0



class Level_manu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        # sound choose
        self.manu_sound = pygame.mixer.Sound('asset/audio/manu_sound.wav')
        self.manu_sound.set_volume(0.8)
        self.playsound = False
        self.button_sound = pygame.mixer.Sound('asset/audio/button.wav')

    def run(self, dt):
        # my sound is:
        if self.playsound == False:
            self.manu_sound.play(loops=True)
            self.playsound = True
        self.display_surface.fill('blue')
        background = pygame.image.load("asset/graphics/manu/background.png")
        backgroundrect = background.get_rect(top=0, bottom=600, left=0, right=800, width=800, height=600)
        self.display_surface.blit(background, backgroundrect)

        self.r1rect = pygame.draw.rect(self.display_surface, (250, 31, 151), (300, 100, 200, 50), 3)
        self.r2rect = pygame.draw.rect(self.display_surface, (250, 31, 151), (300, 200, 200, 50), 3)
        self.r3rect = pygame.draw.rect(self.display_surface, (250, 31, 151), (300, 300, 200, 50), 3)
        self.r4rect = pygame.draw.rect(self.display_surface, (250, 31, 151), (300, 400, 200, 50), 3)
        self.r5rect = pygame.draw.rect(self.display_surface, (250, 31, 151), (300, 500, 200, 50), 3)
        level1 = pygame.image.load("asset/graphics/manu/level1.png")
        level2 = pygame.image.load("asset/graphics/manu/level2.png")
        level3 = pygame.image.load("asset/graphics/manu/level3.png")
        level4 = pygame.image.load("asset/graphics/manu/level4.png")
        levelr = pygame.image.load("asset/graphics/manu/levelreturn.png")
        self.display_surface.blit(level1, self.r1rect)
        self.display_surface.blit(level2, self.r2rect)
        self.display_surface.blit(level3, self.r3rect)
        self.display_surface.blit(level4, self.r4rect)
        self.display_surface.blit(levelr, self.r5rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.r1rect.collidepoint(event.pos):
                    self.button_sound.play(loops=False)
                    self.manu_sound.stop()
                    self.playsound = False
                    return 1
                elif self.r2rect.collidepoint(event.pos):
                    self.button_sound.play(loops=False)
                    self.manu_sound.stop()
                    self.playsound = False
                    return 2
                elif self.r3rect.collidepoint(event.pos):
                    self.button_sound.play(loops=False)
                    self.manu_sound.stop()
                    self.playsound = False
                    return 3
                elif self.r4rect.collidepoint(event.pos):
                    self.button_sound.play(loops=False)
                    self.manu_sound.stop()
                    self.playsound = False
                    return 4
                elif self.r5rect.collidepoint(event.pos):
                    self.button_sound.play(loops=False)
                    self.manu_sound.stop()
                    self.playsound = False
                    return -10
        return 0


class Level:
    def __init__(self, index):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.npc_sprite = pygame.sprite.Group()
        self.player = None
        self.enemy1 = None
        self.enemy2 = None
        self.enemy3 = None
        self.enemy4 = None
        self.company = None

        self.level_index = index
        self.setup()
        time_delay = 1000
        self.time_event = pygame.USEREVENT + 1
        self.timer = pygame.time.set_timer(self.time_event, time_delay)
        self.counter = 30
        self.win = False
        self.lose = False
        self.sky = Sky()
        self.sky2 = Sky2()
        self.success_sound = pygame.mixer.Sound('asset/audio/win_dump.wav')
        self.success = True
        self.fail_sound = pygame.mixer.Sound('asset/audio/lose_sound.wav')
        self.fail = True
        self.manu_sound = pygame.mixer.Sound('asset/audio/background.wav')
        self.manu_sound.set_volume(0.5)
        self.playsound = False
        self.button_sound = pygame.mixer.Sound('asset/audio/button.wav')

    def setup(self):
        level_map = ['asset/map/map1.tmx', 'asset/map/map2.tmx', 'asset/map/map3.tmx', 'asset/map/map4.tmx']
        tmx_data = load_pygame(level_map[self.level_index])  # load tmx map

        # load_ground_layer
        for x, y, surf in tmx_data.get_layer_by_name('ground').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # load_collision_layer
        for x, y, surf in tmx_data.get_layer_by_name('collision').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.collision_sprites)

        # load model start from tmx
        for obj in tmx_data.get_layer_by_name('player'):
            if obj.name == 'start':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.npc_sprite)

        for obj in tmx_data.get_layer_by_name('enemy'):
            if obj.name == 'enemy1':
                self.enemy1 = Enemy((obj.x, obj.y), self.all_sprites, self.collision_sprites)
            if obj.name == 'enemy2':
                self.enemy2 = Enemy((obj.x, obj.y), self.all_sprites, self.collision_sprites)
            if obj.name == 'enemy3':
                self.enemy3 = Enemy((obj.x, obj.y), self.all_sprites, self.collision_sprites)
            if obj.name == 'enemy4':
                self.enemy4 = Enemy((obj.x, obj.y), self.all_sprites, self.collision_sprites)

        for obj in tmx_data.get_layer_by_name('company'):
            if obj.name == 'success':
                self.company = Company((obj.x, obj.y), self.all_sprites, self.collision_sprites)

        self.npc_sprite.add(self.enemy1, self.enemy2, self.enemy3, self.enemy4, self.company)
        # self.player = Player((800, 600), self.all_sprites, self.collision_sprites, self.npc_sprite)

    def run(self, dt):
        if self.playsound == False:
            self.manu_sound.play(loops=True)
            self.playsound = True

        self.display_surface.fill('black')
        self.all_sprites.customize_draw(self.player)
        self.all_sprites.update(dt)
        if self.level_index == 2 or self.level_index == 3:
            self.sky.display(dt)
        if self.level_index == 1 or self.level_index == 3:
            self.sky2.display(dt)
        font = pygame.font.Font("asset/font/chinese_font.ttf", 50)

        levelbuttondraw1 = pygame.image.load("asset/graphics/manu/gamereturn.png")
        self.levelbutton1 = pygame.draw.rect(self.display_surface, (250, 31, 151), (560, 530, 100, 50), 3)
        self.display_surface.blit(levelbuttondraw1, self.levelbutton1)
        if self.win or self.lose:
            levelbuttondraw2 = pygame.image.load("asset/graphics/manu/gamefailed.png")
            if self.win:
                levelbuttondraw2 = pygame.image.load("asset/graphics/manu/gamenext.png")
                if self.success == True:
                    self.success_sound.play(loops=False)
                    self.success = False
            else:
                if self.fail == True:
                    self.fail_sound.play(loops=False)
                    self.fail = False

            self.levelbutton2 = pygame.draw.rect(self.display_surface, (250, 31, 151), (680, 530, 100, 50), 3)
            self.display_surface.blit(levelbuttondraw2, self.levelbutton2)
        else:
            self.levelbutton2 = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.levelbutton1.collidepoint(event.pos):
                    self.button_sound.play()
                    return int(1e9)
                if self.levelbutton2 != None:
                    if self.levelbutton2.collidepoint(event.pos) and self.win:
                        self.button_sound.play()
                        return 1
                    if self.levelbutton2.collidepoint(event.pos) and self.lose:
                        self.button_sound.play()
                        return int(1e9)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

            elif event.type == self.time_event:
                self.counter -= 1
                if (self.counter<=0):
                    self.lose = True
                    self.player.lose = True
        self.win = self.player.win
        self.lose = (self.player.lose | self.lose)

        if self.lose and not self.win:
            text = font.render(str("任务失败"), True, (25, 64, 12))
            text_rect = text.get_rect(
            center=(self.display_surface.get_rect().centerx, self.display_surface.get_rect().centery - 200))
            self.display_surface.blit(text, text_rect)
        elif self.win:
            text = font.render(str("任务成功"), True, (128, 128, 0))
            text_rect = text.get_rect(
            center=(self.display_surface.get_rect().centerx, self.display_surface.get_rect().centery - 200))
            self.display_surface.blit(text, text_rect)
        else:
            # self.overlay.display() # now don't need complex overlay, latter timer and latter
            text = font.render(str(self.counter), True, (25, 64, 12))
            text_rect = text.get_rect(center=(self.display_surface.get_rect().centerx, self.display_surface.get_rect().centery-200))
            self.display_surface.blit(text, text_rect)

        return 0


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def customize_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)


