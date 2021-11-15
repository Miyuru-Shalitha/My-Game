import pygame
import sys
from config import *
from game_objects.player import Player
from pygame.locals import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.monitor_size = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.monitor_size.current_w, self.monitor_size.current_h),
                                              pygame.FULLSCREEN)
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.game_surf = pygame.Surface(SCREEN_SIZE)
        self.font = pygame.font.SysFont("fonts/PermanentMarker-Reguler.ttf", 32)
        self.menu_is_running = False
        self.game_is_running = False

    def show_menu(self):
        self.game_is_running = False
        self.menu_is_running = True

    def start_game(self):
        self.menu_is_running = False
        self.game_is_running = True

        player = Player()

        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)

        while self.game_is_running:
            self.game_surf.fill(BLACK)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_is_running = False
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.game_is_running = False
                        pygame.quit()
                        sys.exit()

            pressed_keys = pygame.key.get_pressed()

            for entity in all_sprites:
                if entity is player:
                    entity.update(pressed_keys)
                else:
                    entity.update()

                self.game_surf.blit(player.image, player.rect)

            # FPS TEXT #############################################################################
            fps_text_surface = self.font.render(f"FPS: {round(self.clock.get_fps())}", False, WHITE)
            self.game_surf.blit(fps_text_surface, (10, 10))
            ########################################################################################

            self.screen.blit(pygame.transform.scale(self.game_surf, (self.screen_width, self.screen_height)), (0, 0))

            pygame.display.flip()
            self.clock.tick(FPS)
