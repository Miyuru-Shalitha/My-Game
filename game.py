import json
import pygame
import sys
import time
from camera import *
from config import *
from game_objects.level_1.blocks.block import Block
from game_objects.enemies.enemy_auto_gun import EnemyAutoGun
from game_objects.player.player import Player
from game_objects.level_1.river import River
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
            "0": False,
            "1": False,
            "2": False,
            "3": False,
            "4": False,
            "5": False,
            "6": False,
            "7": False,
            "8": False,
            "9": False,
            "d": False,
            "a": False,
            "w": False,
            "s": False,
            "b": False,
            "z": False,
            "e": False,
            "r": False,
            "t": False,
            "q": False
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
            mouse_x = mouse_x * (SCREEN_SIZE[0] / self.screen_width)
            mouse_y = mouse_y * (SCREEN_SIZE[1] / self.screen_height)

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
        background_sprites = pygame.sprite.Group()
        foreground_sprites = pygame.sprite.Group()
        players = pygame.sprite.Group()

        all_sprites_list = []

        # particles = {
        #     "river_water_particles": []
        # }

        with open("data/level_1.json", "r") as map_file:
            map_data = json.load(map_file)

            for sprite_data in map_data:
                if sprite_data["name"] == "dirt":
                    dirt = Block(
                        name=sprite_data["name"],
                        group=sprite_data["group"],
                        image_path=sprite_data["image_path"],
                        width=sprite_data["width"],
                        height=sprite_data["height"]
                    )
                    dirt.rect.x = sprite_data["x_coord"]
                    dirt.rect.y = sprite_data["y_coord"]
                    inner_blocks.add(dirt)
                elif (sprite_data["name"] == "grass-top") or \
                        (sprite_data["name"] == "grass-right") or \
                        (sprite_data["name"] == "grass-bottom") or \
                        (sprite_data["name"] == "grass-left"):
                    grass = Block(
                        name=sprite_data["name"],
                        group=sprite_data["group"],
                        image_path=sprite_data["image_path"],
                        width=sprite_data["width"],
                        height=sprite_data["height"],
                        angle=sprite_data["angle"]
                    )
                    grass.rect.x = sprite_data["x_coord"]
                    grass.rect.y = sprite_data["y_coord"]
                    outer_blocks.add(grass)
                elif (sprite_data["name"] == "grass-corner-top-right") or \
                        (sprite_data["name"] == "grass-corner-top-left") or \
                        (sprite_data["name"] == "grass-corner-bottom-right") or \
                        (sprite_data["name"] == "grass-corner-bottom-left"):
                    grass_corner = Block(
                        name=sprite_data["name"],
                        group=sprite_data["group"],
                        image_path=sprite_data["image_path"],
                        width=sprite_data["width"],
                        height=sprite_data["height"],
                        angle=sprite_data["angle"]
                    )
                    grass_corner.rect.x = sprite_data["x_coord"]
                    grass_corner.rect.y = sprite_data["y_coord"]
                    outer_blocks.add(grass_corner)
                elif sprite_data["name"] == "spikes":
                    spikes = Block(
                        name=sprite_data["name"],
                        group=sprite_data["group"],
                        image_path=sprite_data["image_path"],
                        width=sprite_data["width"],
                        height=sprite_data["height"]
                    )
                    spikes.rect.x = sprite_data["x_coord"]
                    spikes.rect.y = sprite_data["y_coord"]
                    outer_blocks.add(spikes)
                elif sprite_data["name"] == "river":
                    river = River(
                        name=sprite_data["name"],
                        group=sprite_data["group"],
                        image_path=sprite_data["image_path"],
                        width=sprite_data["width"],
                        height=sprite_data["height"]
                    )
                    river.rect.x = sprite_data["x_coord"]
                    river.rect.y = sprite_data["y_coord"]
                    background_sprites.add(river)
                elif sprite_data["name"] == "coin":
                    coin = Block(
                        name=sprite_data["name"],
                        group=sprite_data["group"],
                        image_path=sprite_data["image_path"],
                        width=sprite_data["width"],
                        height=sprite_data["height"]
                    )
                    coin.rect.x = sprite_data["x_coord"]
                    coin.rect.y = sprite_data["y_coord"]
                    inner_blocks.add(coin)
                elif sprite_data["name"] == "auto-gun":
                    auto_gun = EnemyAutoGun(
                        name=sprite_data["name"],
                        group=sprite_data["group"],
                        images_paths=sprite_data["images_paths"],
                        width=sprite_data["width"],
                        height=sprite_data["height"],
                        players=players,
                        game_surf=self.game_surf,
                        all_sprites_list=all_sprites_list
                    )
                    auto_gun.rect.x = sprite_data["x_coord"]
                    auto_gun.rect.y = sprite_data["y_coord"]
                    outer_blocks.add(auto_gun)
                elif sprite_data["name"] == "player":
                    player = Player(
                        name=sprite_data["name"],
                        group=sprite_data["group"],
                        image_path="images/player-spritesheet.png",
                        width=sprite_data["width"],
                        height=sprite_data["height"],
                        rigid_objects_groups=[outer_blocks],
                    )
                    player.rect.x = sprite_data["x_coord"]
                    player.rect.y = sprite_data["y_coord"]
                    players.add(player)

        all_sprites.add(background_sprites, inner_blocks, outer_blocks, players, foreground_sprites)
        all_sprites_list += [background_sprites, outer_blocks, inner_blocks, players, foreground_sprites]
        camera = Camera(all_sprites_list=all_sprites_list, player=player)

        prev_time = time.time()

        while self.game_loops_running["level_one"]:
            # Delta time #########
            now = time.time()
            dt = now - prev_time
            dt *= FPS
            prev_time = now
            ######################

            self.game_surf.fill(COLOR_SKY)

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

            # Update and draw sprites ###############################################
            for background_sprite in background_sprites:
                if self.is_out_of_screen(background_sprite):
                    continue

                background_sprite.update(dt)
                self.game_surf.blit(background_sprite.image, background_sprite.rect)

            for inner_block in inner_blocks:
                if self.is_out_of_screen(inner_block):
                    continue

                inner_block.update(dt)
                self.game_surf.blit(inner_block.image, inner_block.rect)

            for outer_block in outer_blocks:
                if self.is_out_of_screen(outer_block):
                    continue

                outer_block.update(dt)
                self.game_surf.blit(outer_block.image, outer_block.rect)

            for player in players:
                player.update(dt, pressed_keys)
                self.game_surf.blit(player.image, player.rect)

            for foreground_sprite in foreground_sprites:
                if self.is_out_of_screen(foreground_sprite):
                    continue

                foreground_sprite.update(dt)
                self.game_surf.blit(foreground_sprite.image, foreground_sprite.rect)

            camera.update(dt)
            #########################################################################

            # DEV ONLY ######################
            try:
                self.level_editor(
                    level=1,
                    inner_blocks=inner_blocks,
                    outer_blocks=outer_blocks,
                    players=players,
                    all_sprites=all_sprites,
                    background_sprites=background_sprites,
                    foreground_sprites=foreground_sprites,
                    all_sprites_list=all_sprites_list
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

    def start_level_two(self):
        pass

    def is_out_of_screen(self, sprite):
        return (sprite.rect.right < 0) or (
                sprite.rect.left > SCREEN_SIZE[0] or (sprite.rect.bottom < 0) or (sprite.rect.top > SCREEN_SIZE[1]))

    def level_editor(self, level, **kwargs):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = mouse_x * (SCREEN_SIZE[0] / self.screen.get_width())
        mouse_y = mouse_y * (SCREEN_SIZE[1] / self.screen.get_height())
        pressed_mouse_buttons = pygame.mouse.get_pressed()
        # pressed_keys = pygame.key.get_pressed()

        if pressed_mouse_buttons[0]:
            for entity in kwargs["all_sprites"]:
                if entity.rect.collidepoint(mouse_x, mouse_y):
                    entity.rect.centerx = mouse_x
                    entity.rect.centery = mouse_y

        if pressed_mouse_buttons[2]:
            for entity in kwargs["all_sprites"]:
                if entity.rect.collidepoint(mouse_x, mouse_y):
                    entity.kill()

        if self.key_presses["0"]:
            self.key_presses["0"] = False
            player = Player(
                name="player",
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

        if self.key_presses["1"]:
            self.key_presses["1"] = False
            dirt = Block(
                name="dirt",
                group="inner_blocks",
                image_path="images/dirt.png",
                width=100,
                height=100,
                angle=-90
            )
            dirt.rect.centerx = mouse_x
            dirt.rect.centery = mouse_y
            kwargs["outer_blocks"].add(dirt)
            kwargs["all_sprites"].add(dirt)

        if self.key_presses["2"]:
            self.key_presses["2"] = False
            grass_top = Block(
                name="grass-top",
                group="outer_blocks",
                image_path="images/grass-side.png",
                width=100,
                height=100
            )
            grass_top.rect.centerx = mouse_x
            grass_top.rect.centery = mouse_y
            kwargs["outer_blocks"].add(grass_top)
            kwargs["all_sprites"].add(grass_top)

        if self.key_presses["3"]:
            self.key_presses["3"] = False
            grass_left = Block(
                name="grass-left",
                group="outer_blocks",
                image_path="images/grass-side.png",
                width=100,
                height=100,
                angle=90
            )
            grass_left.rect.centerx = mouse_x
            grass_left.rect.centery = mouse_y
            kwargs["outer_blocks"].add(grass_left)
            kwargs["all_sprites"].add(grass_left)

        if self.key_presses["4"]:
            self.key_presses["4"] = False
            grass_right = Block(
                name="grass-right",
                group="outer_blocks",
                image_path="images/grass-side.png",
                width=100,
                height=100,
                angle=-90
            )
            grass_right.rect.centerx = mouse_x
            grass_right.rect.centery = mouse_y
            kwargs["outer_blocks"].add(grass_right)
            kwargs["all_sprites"].add(grass_right)

        if self.key_presses["5"]:
            self.key_presses["5"] = False
            grass_bottom = Block(
                name="grass-bottom",
                group="outer_blocks",
                image_path="images/grass-side.png",
                width=100,
                height=100,
                angle=180
            )
            grass_bottom.rect.centerx = mouse_x
            grass_bottom.rect.centery = mouse_y
            kwargs["outer_blocks"].add(grass_bottom)
            kwargs["all_sprites"].add(grass_bottom)

        if self.key_presses["6"]:
            self.key_presses["6"] = False
            grass_corner_top_right = Block(
                name="grass-corner-top-right",
                group="outer_blocks",
                image_path="images/grass-corner.png",
                width=100,
                height=100
            )
            grass_corner_top_right.rect.centerx = mouse_x
            grass_corner_top_right.rect.centery = mouse_y
            kwargs["outer_blocks"].add(grass_corner_top_right)
            kwargs["all_sprites"].add(grass_corner_top_right)

        if self.key_presses["7"]:
            self.key_presses["7"] = False
            print("grass_corner_top_left")
            grass_corner_top_left = Block(
                name="grass-corner-top-left",
                group="outer_blocks",
                image_path="images/grass-corner.png",
                width=100,
                height=100,
                angle=-90
            )
            grass_corner_top_left.rect.centerx = mouse_x
            grass_corner_top_left.rect.centery = mouse_y
            kwargs["outer_blocks"].add(grass_corner_top_left)
            kwargs["all_sprites"].add(grass_corner_top_left)

        if self.key_presses["8"]:
            self.key_presses["8"] = False
            grass_corner_bottom_left = Block(
                name="grass-corner-bottom-left",
                group="outer_blocks",
                image_path="images/grass-corner.png",
                width=100,
                height=100,
                angle=-180
            )
            grass_corner_bottom_left.rect.centerx = mouse_x
            grass_corner_bottom_left.rect.centery = mouse_y
            kwargs["outer_blocks"].add(grass_corner_bottom_left)
            kwargs["all_sprites"].add(grass_corner_bottom_left)

        if self.key_presses["9"]:
            self.key_presses["9"] = False
            grass_corner_bottom_right = Block(
                name="grass-corner-bottom-right",
                group="outer_blocks",
                image_path="images/grass-corner.png",
                width=100,
                height=100,
                angle=90
            )
            grass_corner_bottom_right.rect.centerx = mouse_x
            grass_corner_bottom_right.rect.centery = mouse_y
            kwargs["outer_blocks"].add(grass_corner_bottom_right)
            kwargs["all_sprites"].add(grass_corner_bottom_right)

        if self.key_presses["e"]:
            self.key_presses["e"] = False
            spikes = Block(
                name="spikes",
                group="outer_blocks",
                image_path="images/spikes.png",
                width=100,
                height=50
            )
            spikes.rect.centerx = mouse_x
            spikes.rect.centery = mouse_y
            kwargs["outer_blocks"].add(spikes)
            kwargs["all_sprites"].add(spikes)

        if self.key_presses["r"]:
            self.key_presses["r"] = False
            river = River(
                name="river",
                group="background_sprites",
                image_path="images/river.png",
                width=1200,
                height=300
            )
            river.rect.centerx = mouse_x
            river.rect.centery = mouse_y
            kwargs["background_sprites"].add(river)
            kwargs["all_sprites"].add(river)

        if self.key_presses["t"]:
            self.key_presses["t"] = False
            coin = Block(
                name="coin",
                group="inner_blocks",
                image_path="images/coin.png",
                width=50,
                height=50
            )
            coin.rect.centerx = mouse_x
            coin.rect.centery = mouse_y
            kwargs["inner_blocks"].add(coin)
            kwargs["all_sprites"].add(coin)

        if self.key_presses["q"]:
            self.key_presses["q"] = False
            auto_gun = EnemyAutoGun(
                name="auto-gun",
                group="outer_blocks",
                images_paths=["images/enemies/auto-gun/stand.png", "images/enemies/auto-gun/gun.png"],
                width=100,
                height=100,
                players=kwargs["players"],
                game_surf=self.game_surf,
                all_sprites_list=kwargs["all_sprites_list"]
            )
            auto_gun.rect.centerx = mouse_x
            auto_gun.rect.centery = mouse_y
            kwargs["outer_blocks"].add(auto_gun)
            kwargs["all_sprites"].add(auto_gun)

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
            print("SAVED")
            new_map_data = []

            for entity in kwargs["all_sprites"]:
                if entity.name == "dirt":
                    new_map_data.append({
                        "name": entity.name,
                        "group": entity.group,
                        "image_path": entity.image_path,
                        "width": entity.width,
                        "height": entity.height,
                        "x_coord": entity.rect.x,
                        "y_coord": entity.rect.y,
                    })
                elif (entity.name == "grass-top") or \
                        (entity.name == "grass-right") or \
                        (entity.name == "grass-bottom") or \
                        (entity.name == "grass-left"):
                    new_map_data.append({
                        "name": entity.name,
                        "group": entity.group,
                        "image_path": entity.image_path,
                        "width": entity.width,
                        "height": entity.height,
                        "x_coord": entity.rect.x,
                        "y_coord": entity.rect.y,
                        "angle": entity.angle
                    })
                elif (entity.name == "grass-corner-top-right") or \
                        (entity.name == "grass-corner-top-left") or \
                        (entity.name == "grass-corner-bottom-right") or \
                        (entity.name == "grass-corner-bottom-left"):
                    new_map_data.append({
                        "name": entity.name,
                        "group": entity.group,
                        "image_path": entity.image_path,
                        "width": entity.width,
                        "height": entity.height,
                        "x_coord": entity.rect.x,
                        "y_coord": entity.rect.y,
                        "angle": entity.angle
                    })
                elif entity.name == "spikes":
                    new_map_data.append({
                        "name": entity.name,
                        "group": entity.group,
                        "image_path": entity.image_path,
                        "width": entity.width,
                        "height": entity.height,
                        "x_coord": entity.rect.x,
                        "y_coord": entity.rect.y,
                    })
                elif entity.name == "river":
                    new_map_data.append({
                        "name": entity.name,
                        "group": entity.group,
                        "image_path": entity.image_path,
                        "width": entity.width,
                        "height": entity.height,
                        "x_coord": entity.rect.x,
                        "y_coord": entity.rect.y,
                    })
                elif entity.name == "coin":
                    new_map_data.append({
                        "name": entity.name,
                        "group": entity.group,
                        "image_path": entity.image_path,
                        "width": entity.width,
                        "height": entity.height,
                        "x_coord": entity.rect.x,
                        "y_coord": entity.rect.y,
                    })
                elif entity.name == "auto-gun":
                    new_map_data.append({
                        "name": entity.name,
                        "group": entity.group,
                        "images_paths": entity.images_paths,
                        "width": entity.width,
                        "height": entity.height,
                        "x_coord": entity.rect.x,
                        "y_coord": entity.rect.y,
                    })
                elif entity.name == "player":
                    new_map_data.append({
                        "name": entity.name,
                        "group": entity.group,
                        "image_path": entity.image_path,
                        "width": entity.width,
                        "height": entity.height,
                        "x_coord": entity.rect.x,
                        "y_coord": entity.rect.y,
                    })

            new_map_json_data = json.dumps(new_map_data, indent=2)  # DEV ONLY
            # new_map_json_data = json.dumps(new_map_data)

            if type(level) is int:
                with open(f"data/level_{level}.json", "w") as map_file:
                    map_file.write(new_map_json_data)
            elif type(level) is str:
                with open(f"data/{level}.json", "w") as map_file:
                    map_file.write(new_map_json_data)

    def level_editor_controls(self, event):
        if event.type == KEYDOWN:
            if event.key == K_0:
                self.key_presses["0"] = True
            if event.key == K_1:
                self.key_presses["1"] = True
            if event.key == K_2:
                self.key_presses["2"] = True
            if event.key == K_3:
                self.key_presses["3"] = True
            if event.key == K_4:
                self.key_presses["4"] = True
            if event.key == K_5:
                self.key_presses["5"] = True
            if event.key == K_6:
                self.key_presses["6"] = True
            if event.key == K_7:
                self.key_presses["7"] = True
            if event.key == K_8:
                self.key_presses["8"] = True
            if event.key == K_9:
                self.key_presses["9"] = True
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
            if event.key == K_z:
                self.key_presses["z"] = True
            if event.key == K_e:
                self.key_presses["e"] = True
            if event.key == K_r:
                self.key_presses["r"] = True
            if event.key == K_t:
                self.key_presses["t"] = True
            if event.key == K_q:
                self.key_presses["q"] = True

        if event.type == KEYUP:
            if event.key == K_0:
                self.key_presses["0"] = False
            if event.key == K_1:
                self.key_presses["1"] = False
            if event.key == K_2:
                self.key_presses["2"] = False
            if event.key == K_3:
                self.key_presses["3"] = False
            if event.key == K_4:
                self.key_presses["4"] = False
            if event.key == K_5:
                self.key_presses["5"] = False
            if event.key == K_6:
                self.key_presses["6"] = False
            if event.key == K_7:
                self.key_presses["7"] = False
            if event.key == K_8:
                self.key_presses["8"] = False
            if event.key == K_9:
                self.key_presses["9"] = False
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
            if event.key == K_z:
                self.key_presses["z"] = False
            if event.key == K_e:
                self.key_presses["e"] = False
            if event.key == K_r:
                self.key_presses["r"] = False
            if event.key == K_t:
                self.key_presses["t"] = False
            if event.key == K_q:
                self.key_presses["q"] = False
