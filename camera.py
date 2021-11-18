from config import *


class Camera:
    def __init__(self, all_sprites_list, player):
        self.all_sprites_list = all_sprites_list
        self.player = player
        self.speed = player.speed
        self.offset = 200
        self.screen_center_pos = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

    def update(self):
        for sprite_group in self.all_sprites_list:
            for sprite in sprite_group:
                if self.player.rect.centerx > (self.screen_center_pos[0] + self.offset):
                    sprite.rect.x -= self.speed

                if self.player.rect.centerx < (self.screen_center_pos[0] - self.offset):
                    sprite.rect.x += self.speed

                if self.player.rect.centery > (self.screen_center_pos[1] + self.offset):
                    sprite.rect.y -= self.speed

                if self.player.rect.centery < (self.screen_center_pos[1] - self.offset):
                    sprite.rect.y += self.speed
