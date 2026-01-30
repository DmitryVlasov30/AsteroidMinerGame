import math
from pathlib import Path
import arcade
import random
from config import settings


class Meteor(arcade.Sprite):
    def __init__(self, image: str, x: int, y: int, min_speed: int, max_speed: int, flag=False):
        super().__init__(image)

        self.center_x = x
        self.center_y = y
        self.speed = random.uniform(min_speed, max_speed)

        angel = random.uniform(0, 2 * math.pi)
        self.change_x = math.cos(angel) * self.speed
        self.change_y = math.sin(angel) * self.speed
        self.elast = 0.7
        if flag:
            self.ogr_x = settings.SCREEN_WIDTH
            self.ogr_y = settings.SCREEN_HEIGHT
        else:
            self.ogr_x = settings.ogr_x
            self.ogr_y = settings.ogr_y

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        super().update()
        self.center_x += self.speed * delta_time
        self.center_y += self.speed * delta_time

        bounced = False
        if self.left <= 0:
            self.left = 0
            self.change_x = abs(self.change_x) * self.elast
            bounced = True
        elif self.right >= self.ogr_x:
            self.right = self.ogr_x
            self.change_x = -abs(self.change_x) * self.elast
            bounced = True

        if self.bottom <= 0:
            self.bottom = 0
            self.change_y = abs(self.change_y) * self.elast
            bounced = True
        elif self.top >= self.ogr_y:
            self.top = self.ogr_y
            self.change_y = -abs(self.change_y) * self.elast
            bounced = True

        if bounced:
            self.speed *= 0.99


class Spaceship(arcade.Sprite):
    def __init__(self, image: str, x: int = 0, y: int = 0):
        super().__init__()
        self.right_pressed = False
        self.left_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.center_x = x
        self.scale = 0.8
        self.center_y = y
        self.speed = 10
        self.idle_texture = arcade.load_texture(image)
        self.texture = self.idle_texture

        self.rotation_speed = 250
        self.movement_speed = 360
        self.facing_angle = 0
        self.is_broken = False
        self.timer_animation = 0
        self.interval = 0.1
        self.current_texture = 0

        self.sprite_width = 64
        self.sprite_height = 64

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        dx, dy = 0, 0
        if self.right_pressed:
            self.angle += self.rotation_speed * delta_time
            self.facing_angle += math.radians(self.rotation_speed * delta_time)
        if self.left_pressed:
            self.angle -= self.rotation_speed * delta_time
            self.facing_angle -= math.radians(self.rotation_speed * delta_time)

        if self.up_pressed:
            dx += math.sin(self.facing_angle) * self.movement_speed * delta_time
            dy += math.cos(self.facing_angle) * self.movement_speed * delta_time
        if self.down_pressed:
            dx -= math.sin(self.facing_angle) * self.movement_speed * delta_time * 0.5
            dy -= math.cos(self.facing_angle) * self.movement_speed * delta_time * 0.5

        new_x = self.center_x + dx
        new_y = self.center_y + dy

        half_width = self.sprite_width / 2
        half_height = self.sprite_height / 2

        if new_x - half_width < 0:
            new_x = half_width
        elif new_x + half_width > settings.ogr_x:
            new_x = settings.ogr_x - half_width

        if new_y - half_height < 0:
            new_y = half_height
        elif new_y + half_height > settings.ogr_y:
            new_y = settings.ogr_y - half_height

        self.center_x = new_x
        self.center_y = new_y


class Laser(arcade.Sprite):
    def __init__(self, start_x, start_y, sprite_angle, speed=settings.speed_lasers):
        super().__init__()
        self.texture = arcade.load_texture(
            r"..\sprites\PNG\Lasers\laserBlue01.png"
        )

        self.center_x = start_x
        self.center_y = start_y
        self.speed = speed
        angle_rad = math.radians(sprite_angle)

        self.change_x = math.sin(angle_rad) * speed
        self.change_y = math.cos(angle_rad) * speed

        self.angle = sprite_angle

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        if (self.center_x < 0 or self.center_x > settings.ogr_x + 2000 or
                self.center_y < 0 or self.center_y > settings.ogr_y + 2000):
            self.remove_from_sprite_lists()


class Enemy(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.center_x = random.randint(0, settings.ogr_x)
        self.center_y = random.randint(0, settings.ogr_y)
        self.target_x = random.randint(50, settings.ogr_x)
        self.target_y = random.randint(50, settings.ogr_y)
        self.speed = 2

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        dx = self.target_x - self.center_x
        dy = self.target_y - self.center_y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 5:
            self.change_x = (dx / distance) * self.speed
            self.change_y = (dy / distance) * self.speed
        else:
            self.target_x = random.randint(50, settings.SCREEN_WIDTH)
            self.target_y = random.randint(50, settings.SCREEN_HEIGHT)

        super().update()


class Number(arcade.Sprite):
    def __init__(self, x: int, y: int, number: int, scale):
        super().__init__(self, scale)
        path = rf"..\sprites\PNG\UI\numeral{number}.png"
        self.texture = arcade.load_texture(path)
        self.center_x = x
        self.center_y = y
