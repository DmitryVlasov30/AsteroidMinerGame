import random
import arcade
from pyglet.graphics import Batch
from config import settings
from utils import DataManager

from game_objects import Spaceship, Laser, Enemy, Meteor, Number

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Asteroid Miner"
speed = 10


class GameView(arcade.View):
    def __init__(self, filename_image, filename_enemy, filename_spaceship, count_enemy, count_meteor, scale_enemy):
        super().__init__()
        self.number_1, self.number_2 = 0, 0
        self.number_3, self.number_4 = 0, 0
        self.numbers = None
        self.meteor_list = None
        self.bullet_list = None
        self.player_list = None
        self.enemy_list = None
        self.player = None
        self.broken_list = None
        self.count_enemy_kill = 0

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.sound = arcade.load_sound("../laser_sound.m4a")

        self.level = DataManager().get_data()
        self.filename_spaceship = filename_spaceship
        self.scale_enemy = scale_enemy
        self.count_meteor = count_meteor
        self.count_enemy = count_enemy
        self.texture = arcade.load_texture(filename_image)
        self.filename_enemy = filename_enemy
        self.key_pressed = set()
        self.setup()

        self.batch = Batch()
        self.text_info = arcade.Text(
            "WASD — движение • shift - стрельба • подстреливай инопланетные тарелки",
            20, 20, arcade.color.BLACK, 14, batch=self.batch
        )

        self.window.set_mouse_visible(True)

    def setup(self):
        self.player = Spaceship(x=500, y=500, image=self.filename_spaceship)
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.meteor_list = arcade.SpriteList()
        self.broken_list = arcade.SpriteList()
        self.numbers = arcade.SpriteList()
        self.create_number()

        path_meteors = [
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\Meteors\meteorGrey_med1.png",
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\Meteors\meteorBrown_small1.png",
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\Meteors\meteorGrey_big1.png",
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\Meteors\meteorGrey_med1.png",
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\Meteors\meteorGrey_small1.png",
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\Meteors\meteorBrown_big3.png"
        ]

        for _ in range(self.count_enemy):
            enemy = Enemy(
                filename=self.filename_enemy,
                scale=self.scale_enemy
            )
            self.enemy_list.append(enemy)

        for _ in range(self.count_meteor):
            interval_x = [el for el in range(0, SCREEN_WIDTH, 20) if abs(500 - el) > 100]
            interval_y = [el for el in range(0, SCREEN_HEIGHT, 20) if abs(500 - el) > 100]
            meteor = Meteor(
                image=random.choice(path_meteors),
                x=random.choice(interval_x),
                y=random.choice(interval_y),
                min_speed=1,
                max_speed=4,
            )
            self.meteor_list.append(meteor)
        self.player_list.append(self.player)

    def create_number(self):
        if self.count_enemy_kill < 10:
            self.number_1 = Number(800, 950, scale=2, number=0)
            self.number_2 = Number(840, 950, scale=2, number=self.count_enemy_kill)
        else:
            self.number_1 = Number(800, 950, scale=2, number=self.count_enemy_kill // 10)
            self.number_2 = Number(840, 950, scale=2, number=self.count_enemy_kill % 10)

        self.number_3 = Number(920, 950, scale=2, number=self.count_enemy // 10)
        self.number_4 = Number(960, 950, scale=2, number=self.count_enemy % 10)

        if not self.numbers:
            self.numbers.append(self.number_1)
            self.numbers.append(self.number_2)
            self.numbers.append(self.number_3)
            self.numbers.append(self.number_4)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.texture,
            arcade.rect.XYWH(
                self.width // 2,
                self.height // 2,
                self.width,
                self.height
            )
        )

        self.world_camera.use()
        self.enemy_list.draw()
        self.meteor_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.broken_list.draw()

        self.gui_camera.use()
        self.batch.draw()
        self.numbers.draw()

    def on_key_release(self, key: int, modifiers: int) -> bool | None:
        if key in self.key_pressed:
            self.key_pressed.remove(key)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RSHIFT:
            bullet = Laser(
                self.player.center_x,
                self.player.center_y,
                sprite_angle=self.player_list[0].angle,
                speed=800
            )
            self.bullet_list.append(bullet)
            self.sound.play(volume=2)
        self.key_pressed.add(key)
        if key == arcade.key.ESCAPE:
            self.window.close()
        if key == arcade.key.TAB:
            from start_menu import MainMenu
            pause = MainMenu(
                *settings.background_level[self.level],
                main_text="Пауза",
                options=["ИГРАТЬ ЗАНОВО", "ВЫХОД", "ПРОДОЛЖИТЬ"],
                pause=self
            )
            self.window.show_view(pause)

    def on_update(self, delta_time):
        for player in self.player_list:
            player.left_pressed = arcade.key.A in self.key_pressed
            player.right_pressed = arcade.key.D in self.key_pressed
            player.up_pressed = arcade.key.W in self.key_pressed
            player.down_pressed = arcade.key.S in self.key_pressed

        self.bullet_list.update()
        self.player_list.update()
        self.enemy_list.update()
        self.meteor_list.update()

        position = (
            self.player_list[0].center_x,
            self.player_list[0].center_y
        )

        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            position,
            0.12,
        )

        for bullet in self.bullet_list:
            enemies_hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if enemies_hit_list:
                for enemy in enemies_hit_list:
                    self.count_enemy_kill += 1
                    self.numbers.clear()
                    self.create_number()
                    enemy.remove_from_sprite_lists()
                    if self.count_enemy_kill == self.count_enemy:
                        from start_menu import MainMenu
                        if self.level != 4:
                            DataManager().update_data(level=self.level + 1)
                            win_menu = MainMenu(
                                *settings.background_level[self.level + 1],
                                main_text="Вы выиграли, поздравляю",
                                options=["ИГРАТЬ", "ВЫХОД"]
                            )
                        else:
                            win_menu = MainMenu(
                                *settings.background_level[self.level],
                                main_text="Вы выиграли, поздравляю",
                                options=["ИГРАТЬ", "ВЫХОД", "ПРОЙТИ ЗАНОВО"]
                            )
                        self.window.show_view(win_menu)

        meteor_hit = arcade.check_for_collision_with_list(self.player_list[0], self.meteor_list)
        if meteor_hit:
            for meteor in meteor_hit:
                from start_menu import MainMenu
                fail_menu = MainMenu(
                    *settings.background_level[self.level],
                    main_text="Вы проиграли",
                    options=["ИГРАТЬ СНОВА", "ВЫХОД"]
                )
                self.window.show_view(fail_menu)
