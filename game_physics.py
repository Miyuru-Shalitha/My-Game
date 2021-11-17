import pygame


class GravityMixin:
    def __init__(self, game_object):
        self.game_object = game_object
        self.gravity = 0.2
        self.y_change = 0

    def apply_gravity(self):
        self.game_object.rect.y += self.y_change
        self.y_change += self.gravity


class ColliderMixin:
    def __init__(self, game_object, other_objects_groups, y_change):
        self.game_object = game_object
        self.other_objects_groups = other_objects_groups
        self.y_change = y_change
        self.moving_direction = {"horizontal": "stopped", "vertical": "stopped"}
        self.prev_location = None
        self.is_collided_horizontally = False
        self.is_collided_vertically = False

    def apply_collisions(self):
        if self.prev_location:
            moving_x_direction = self.game_object.rect.x - self.prev_location[0]
            moving_y_direction = self.game_object.rect.y - self.prev_location[1]

            if (moving_x_direction > 0) and (not self.is_collided_horizontally):
                self.moving_direction["horizontal"] = "right"
            elif (moving_x_direction < 0) and (not self.is_collided_horizontally):
                self.moving_direction["horizontal"] = "left"
            elif not self.is_collided_horizontally:
                self.moving_direction["horizontal"] = "stopped"

            if (moving_y_direction > 0) and (not self.is_collided_vertically):
                self.moving_direction["vertical"] = "down"
            elif (moving_y_direction < 0) and (not self.is_collided_vertically):
                self.moving_direction["vertical"] = "up"
            elif not self.is_collided_vertically:
                self.moving_direction["vertical"] = "stopped"

        self.prev_location = [self.game_object.rect.x, self.game_object.rect.y]

        self.is_collided_horizontally = False
        self.is_collided_vertically = False

        for objs in self.other_objects_groups:
            collided_sprites = pygame.sprite.spritecollide(self.game_object, objs, False)

            if self.moving_direction["horizontal"] == "right":
                for obj in collided_sprites:
                    if self.game_object.rect.right > obj.rect.left:
                        self.is_collided_horizontally = True
                        self.game_object.rect.right = obj.rect.left

            elif self.moving_direction["horizontal"] == "left":
                for obj in collided_sprites:
                    if self.game_object.rect.left < obj.rect.right:
                        self.is_collided_horizontally = True
                        self.game_object.rect.left = obj.rect.right

            if self.moving_direction["vertical"] == "up":
                for obj in collided_sprites:
                    if self.game_object.rect.top < obj.rect.bottom:
                        self.is_collided_vertically = True
                        self.game_object.rect.top = obj.rect.bottom

            elif self.moving_direction["vertical"] == "down":
                for obj in collided_sprites:
                    if self.game_object.rect.bottom > obj.rect.top:
                        self.is_collided_vertically = True
                        self.game_object.rect.bottom = obj.rect.top
