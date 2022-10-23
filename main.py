import pygame, sys
from settings import *
from level import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Navajo')
        icon = pygame.image.load("asset/graphics/manu/icon.png")
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.level_choose = 0
        self.level = [Manu(), Level_manu(), Level(0), Level(1), Level(2), Level(3)]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

            dt = self.clock.tick(144) / 1000  # dt for whole game

            # level choose
            self.level_choose += self.level[self.level_choose].run(dt)
            if self.level_choose < 0:
                self.level_choose = 0
            elif self.level_choose >= len(self.level):
                self.level_choose = 0
                self.level = [Manu(), Level_manu(), Level(0), Level(1), Level(2), Level(3)]
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()

