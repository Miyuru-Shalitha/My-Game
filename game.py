import json
import pygame
import sys
from config import *
from game_objects.player.player import Player
from game_objects.level_1.blocks.block import Block
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

        # DEV ONLY ###########
        self.key_presses = {
            "s": False,
            "1": False,
            "0": False
        }
        self.mouse_clicks = {}
        ######################

    def show_menu(self):
        self.game_is_running = False
        self.menu_is_running = True

    def start_level_one(self):
        self.menu_is_running = False
        self.game_is_running = True

        player = Player(
            name="Player",
            image_path="images/player-spritesheet.png",
            width=200,
            height=200
        )

        outer_blocks = pygame.sprite.Group()

        with open("data/level_1.json", "r") as map_file:
            map_data = json.load(map_file)

            for sprite_data in map_data:
                block = Block(
                    name=["name"],
                    image_path=sprite_data["image_path"],
                    width=sprite_data["width"],
                    height=sprite_data["height"]
                )
                block.rect.x = sprite_data["x_coord"]
                block.rect.y = sprite_data["y_coord"]
                outer_blocks.add(block)

        all_sprites = pygame.sprite.Group()
        all_sprites.add(outer_blocks, player)

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
                    # DEV ONLY #####################
                    if event.key == K_s:
                        self.key_presses["s"] = True
                    if event.key == K_1:
                        self.key_presses["1"] = True
                    if event.key == K_0:
                        self.key_presses["0"] = True
                    ################################

                if event.type == KEYUP:
                    # DEV ONLY ######################
                    if event.key == K_s:
                        self.key_presses["s"] = False
                    if event.key == K_1:
                        self.key_presses["1"] = False
                    if event.key == K_0:
                        self.key_presses["0"] = False
                    #################################

            pressed_keys = pygame.key.get_pressed()

            for entity in all_sprites:
                if entity.name == "Player":
                    entity.update(pressed_keys)
                else:
                    entity.update()

                self.game_surf.blit(entity.image, entity.rect)

            # DEV ONLY ####################
            self.level_editor(1, all_sprites)
            ###############################

            # FPS TEXT #############################################################################
            fps_text_surface = self.font.render(f"FPS: {round(self.clock.get_fps())}", False, WHITE)
            self.game_surf.blit(fps_text_surface, (10, 10))
            ########################################################################################

            self.screen.blit(pygame.transform.scale(self.game_surf, (self.screen_width, self.screen_height)), (0, 0))

            pygame.display.flip()
            self.clock.tick(FPS)

    # def start_level_two(self):
    #     self.menu_is_running = False
    #     self.game_is_running = True
    #
    #     player = Player()
    #
    #     all_sprites = pygame.sprite.Group()
    #     all_sprites.add(player)
    #
    #     while self.game_is_running:
    #         self.game_surf.fill(BLACK)
    #
    #         for event in pygame.event.get():
    #             if event.type == QUIT:
    #                 self.game_is_running = False
    #                 pygame.quit()
    #                 sys.exit()
    #
    #             if event.type == KEYDOWN:
    #                 if event.key == K_ESCAPE:
    #                     self.game_is_running = False
    #                     pygame.quit()
    #                     sys.exit()
    #
    #         pressed_keys = pygame.key.get_pressed()
    #
    #         for entity in all_sprites:
    #             if entity is player:
    #                 entity.update(pressed_keys)
    #             else:
    #                 entity.update()
    #
    #             self.game_surf.blit(player.image, player.rect)
    #
    #         # FPS TEXT #############################################################################
    #         fps_text_surface = self.font.render(f"FPS: {round(self.clock.get_fps())}", False, WHITE)
    #         self.game_surf.blit(fps_text_surface, (10, 10))
    #         ########################################################################################
    #
    #         self.screen.blit(pygame.transform.scale(self.game_surf, (self.screen_width, self.screen_height)),
    #                          (0, 0))
    #
    #         pygame.display.flip()
    #         self.clock.tick(FPS)

    def level_editor(self, level, all_sprites):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = mouse_x * (SCREEN_SIZE[0] / self.screen.get_width())
        mouse_y = mouse_y * (SCREEN_SIZE[1] / self.screen.get_height())
        pressed_mouse_buttons = pygame.mouse.get_pressed()
        pressed_keys = pygame.key.get_pressed()

        if pressed_mouse_buttons[0]:
            for entity in all_sprites:
                if entity.rect.collidepoint(mouse_x, mouse_y):
                    entity.rect.centerx = mouse_x
                    entity.rect.centery = mouse_y

        if pressed_mouse_buttons[2]:
            for entity in all_sprites:
                if entity.rect.collidepoint(mouse_x, mouse_y):
                    entity.kill()

        if self.key_presses["1"]:
            self.key_presses["1"] = False
            grass = Block(
                name="Grass",
                image_path="images/grass-side.png"
            )
            grass.rect.centerx = mouse_x
            grass.rect.centery = mouse_y
            all_sprites.add(grass)

        if self.key_presses["0"]:
            self.key_presses["0"] = False
            player = Player(
                name="Player",
                image_path="images/player-spritesheet.png",
                width=200,
                height=200
            )
            player.rect.centerx = mouse_x
            player.rect.centery = mouse_y
            all_sprites.add(player)

        if self.key_presses["s"]:
            self.key_presses["s"] = False
            new_map_data = []

            for entity in all_sprites:
                new_map_data.append({
                    "image_path": entity.image_path,
                    "width": entity.width,
                    "height": entity.height,
                    "x_coord": entity.rect.x,
                    "y_coord": entity.rect.y
                })

            new_map_json_data = json.dumps(new_map_data)

            with open(f"data/level_{level}.json", "w") as map_file:
                map_file.write(new_map_json_data)
