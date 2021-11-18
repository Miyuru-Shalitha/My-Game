import json
import pygame
import sys
import time
from camera import *
from config import *
from game_objects.player.player import Player
from game_objects.level_1.blocks.block import Block
from menu.button import Button
from pygame.locals import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.monitor_size = pygame.display.Info()
        # self.screen = pygame.display.set_mode((self.monitor_size.current_w, self.monitor_size.current_h),
        #                                       pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(SCREEN_SIZE)  # DEV ONLY
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.game_surf = pygame.Surface(SCREEN_SIZE)
        self.font = pygame.font.SysFont("fonts/PermanentMarker-Reguler.ttf", 32)
        self.game_loops_running = {
            "menu": False,
            "level_one": False,
            "level_two": False,
            "level_three": False,
            "level_four": False,
            "level_five": False,
            "level_six": False,
            "level_seven": False,
            "level_eight": False,
            "level_nine": False,
            "level_ten": False
        }

        # DEV ONLY ###########
        self.key_presses = {
            "z": False,
            "1": False,
            "2": False,
            "0": False,
            "d": False,
            "a": False,
            "w": False,
            "s": False,
            "b": False
        }
        self.mouse_clicks = {}
        ######################

    def run_game_loop(self, game_loop_to_run):
        for game_loop in self.game_loops_running:
            if game_loop == game_loop_to_run:
                self.game_loops_running[game_loop] = True
            else:
                self.game_loops_running[game_loop] = False

    def show_menu(self):
        self.run_game_loop("menu")

        all_sprites = pygame.sprite.Group()
        buttons = pygame.sprite.Group()

        screen_center_pos = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

        start_button = Button(
            group=buttons,
            image_path="images/start-button.png",
            width=300,
            height=50,
            func=self.start_level_one
        )
        start_button.rect.centerx = screen_center_pos[0]
        start_button.rect.centery = screen_center_pos[1]
        buttons.add(start_button)

        levels_button = Button(
            group=buttons,
            image_path="images/levels-button.png",
            width=300,
            height=50,
            func=self.start_level_one
        )
        levels_button.rect.centerx = screen_center_pos[0]
        levels_button.rect.centery = start_button.rect.centery + 60
        buttons.add(levels_button)

        all_sprites.add(buttons)

        while self.game_loops_running["menu"]:
            self.game_surf.fill(BLACK)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_loops_running["menu"] = False
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.game_loops_running["menu"] = False
                        pygame.quit()
                        sys.exit()

                self.level_editor_controls(event=event)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            clicked_mouse_buttons = pygame.mouse.get_pressed()

            buttons.update(mouse_x, mouse_y, clicked_mouse_buttons)

            buttons.draw(self.game_surf)

            # FPS TEXT #############################################################################
            fps_text_surface = self.font.render(f"FPS: {round(self.clock.get_fps())}", False, WHITE)
            self.game_surf.blit(fps_text_surface, (10, 10))
            ########################################################################################

            # self.screen.blit(pygame.transform.scale(self.game_surf, (self.screen_width, self.screen_height)), (0, 0))
            self.screen.blit(self.game_surf, (0, 0))  # DEV ONLY

            pygame.display.flip()
            self.clock.tick(FPS)

    def start_level_one(self):
        self.run_game_loop("level_one")

        all_sprites = pygame.sprite.Group()
        outer_blocks = pygame.sprite.Group()
        inner_blocks = pygame.sprite.Group()
        players = pygame.sprite.Group()

        with open("data/level_1.json", "r") as map_file:
            map_data = json.load(map_file)

            for sprite_data in map_data:
                if sprite_data["group"] == "outer_blocks":
                    block = Block(
                        group="outer_blocks",
                        image_path=sprite_data["image_path"],
                        width=sprite_data["width"],
                        height=sprite_data["height"]
                    )
                    block.rect.x = sprite_data["x_coord"]
                    block.rect.y = sprite_data["y_coord"]
                    outer_blocks.add(block)
                if sprite_data["group"] == "inner_blocks":
                    block = Block(
                        group="inner_blocks",
                        image_path=sprite_data["image_path"],
                        width=sprite_data["width"],
                        height=sprite_data["height"]
                    )
                    block.rect.x = sprite_data["x_coord"]
                    block.rect.y = sprite_data["y_coord"]
                    inner_blocks.add(block)
                elif sprite_data["group"] == "players":
                    player = Player(
                        group="players",
                        image_path="images/player-spritesheet.png",
                        width=sprite_data["width"],
                        height=sprite_data["height"],
                        rigid_objects_groups=[outer_blocks]
                    )
                    player.rect.x = sprite_data["x_coord"]
                    player.rect.y = sprite_data["y_coord"]
                    players.add(player)

        all_sprites.add(inner_blocks, outer_blocks, players)
        all_sprites_list = [outer_blocks, inner_blocks, players]
        camera = Camera(all_sprites_list=all_sprites_list, player=player)

        while self.game_loops_running["level_one"]:
            self.game_surf.fill(BLACK)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_loops_running["level_one"] = False
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.game_loops_running["level_one"] = False
                        self.show_menu()

                self.level_editor_controls(event=event)

            pressed_keys = pygame.key.get_pressed()

            inner_blocks.update()
            outer_blocks.update()
            players.update(pressed_keys)
            camera.update()

            inner_blocks.draw(self.game_surf)
            outer_blocks.draw(self.game_surf)
            players.draw(self.game_surf)

            # DEV ONLY ######################
            try:
                self.level_editor(
                    level=1,
                    inner_blocks=inner_blocks,
                    outer_blocks=outer_blocks,
                    players=players,
                    all_sprites=all_sprites,
                )
            except KeyError:
                print("Invalid command!")
            #################################

            # FPS TEXT #############################################################################
            fps_text_surface = self.font.render(f"FPS: {round(self.clock.get_fps())}", False, WHITE)
            self.game_surf.blit(fps_text_surface, (10, 10))
            ########################################################################################

            # self.screen.blit(pygame.transform.scale(self.game_surf, (self.screen_width, self.screen_height)), (0, 0))
            self.screen.blit(self.game_surf, (0, 0))  # DEV ONLY

            pygame.display.flip()
            self.clock.tick(FPS)

    def level_editor(self, level, **kwargs):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = mouse_x * (SCREEN_SIZE[0] / self.screen.get_width())
        mouse_y = mouse_y * (SCREEN_SIZE[1] / self.screen.get_height())
        pressed_mouse_buttons = pygame.mouse.get_pressed()
        pressed_keys = pygame.key.get_pressed()

        if pressed_mouse_buttons[0]:
            for entity in kwargs["all_sprites"]:
                if entity.rect.collidepoint(mouse_x, mouse_y):
                    entity.rect.centerx = mouse_x
                    entity.rect.centery = mouse_y

        if pressed_mouse_buttons[2]:
            for entity in kwargs["all_sprites"]:
                if entity.rect.collidepoint(mouse_x, mouse_y):
                    entity.kill()

        if self.key_presses["1"]:
            self.key_presses["1"] = False
            grass = Block(
                group="outer_blocks",
                image_path="images/grass-side.png",
                width=100,
                height=100
            )
            grass.rect.centerx = mouse_x
            grass.rect.centery = mouse_y
            kwargs["outer_blocks"].add(grass)
            kwargs["all_sprites"].add(grass)

        if self.key_presses["2"]:
            self.key_presses["2"] = False
            dirt = Block(
                group="inner_blocks",
                image_path="images/dirt.png",
                width=100,
                height=100
            )
            dirt.rect.centerx = mouse_x
            dirt.rect.centery = mouse_y
            kwargs["inner_blocks"].add(dirt)
            kwargs["all_sprites"].add(dirt)

        if self.key_presses["0"]:
            self.key_presses["0"] = False
            player = Player(
                group="players",
                image_path="images/player-spritesheet.png",
                width=75,
                height=150,
                rigid_objects_groups=[kwargs["outer_blocks"]]
            )
            player.rect.centerx = mouse_x
            player.rect.centery = mouse_y
            kwargs["players"].add(player)
            kwargs["all_sprites"].add(player)

        if self.key_presses["d"]:
            self.key_presses["d"] = False
            for entity in kwargs["all_sprites"]:
                if entity.rect.collidepoint(mouse_x, mouse_y):
                    entity.rect.x += 1

        if self.key_presses["a"]:
            self.key_presses["a"] = False
            for entity in kwargs["all_sprites"]:
                if entity.rect.collidepoint(mouse_x, mouse_y):
                    entity.rect.x -= 1

        if self.key_presses["w"]:
            self.key_presses["w"] = False
            for entity in kwargs["all_sprites"]:
                if entity.rect.collidepoint(mouse_x, mouse_y):
                    entity.rect.y -= 1

        if self.key_presses["s"]:
            self.key_presses["s"] = False
            for entity in kwargs["all_sprites"]:
                if entity.rect.collidepoint(mouse_x, mouse_y):
                    entity.rect.y += 1

        if self.key_presses["z"]:
            self.key_presses["z"] = False
            print("SAVE")
            new_map_data = []

            for entity in kwargs["all_sprites"]:
                new_map_data.append({
                    "group": entity.group,
                    "image_path": entity.image_path,
                    "width": entity.width,
                    "height": entity.height,
                    "x_coord": entity.rect.x,
                    "y_coord": entity.rect.y
                })

            new_map_json_data = json.dumps(new_map_data, indent=4)  # DEV ONLY
            # new_map_json_data = json.dumps(new_map_data)

            if type(level) is int:
                with open(f"data/level_{level}.json", "w") as map_file:
                    map_file.write(new_map_json_data)
            elif type(level) is str:
                with open(f"data/{level}.json", "w") as map_file:
                    map_file.write(new_map_json_data)

    def level_editor_controls(self, event):
        if event.type == KEYDOWN:
            if event.key == K_z:
                self.key_presses["z"] = True
            if event.key == K_1:
                self.key_presses["1"] = True
            if event.key == K_2:
                self.key_presses["2"] = True
            if event.key == K_0:
                self.key_presses["0"] = True
            if event.key == K_d:
                self.key_presses["d"] = True
            if event.key == K_a:
                self.key_presses["a"] = True
            if event.key == K_w:
                self.key_presses["w"] = True
            if event.key == K_s:
                self.key_presses["s"] = True
            if event.key == K_b:
                self.key_presses["b"] = True

        if event.type == KEYUP:
            if event.key == K_z:
                self.key_presses["z"] = False
            if event.key == K_1:
                self.key_presses["1"] = False
            if event.key == K_2:
                self.key_presses["2"] = False
            if event.key == K_0:
                self.key_presses["0"] = False
            if event.key == K_d:
                self.key_presses["d"] = False
            if event.key == K_a:
                self.key_presses["a"] = False
            if event.key == K_w:
                self.key_presses["w"] = False
            if event.key == K_s:
                self.key_presses["s"] = False
            if event.key == K_b:
                self.key_presses["b"] = False
