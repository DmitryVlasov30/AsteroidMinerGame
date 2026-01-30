from config import settings
from src.game_view import GameView
from src.game_objects import Meteor

import arcade
from random import randint, choice


class MainMenu(arcade.View):
    def __init__(self,
                 filename_background: str,
                 arcade_color_text,
                 space_ship_path,
                 enemy_filename,
                 count_enemy,
                 count_meteor,
                 scale_enemy,
                 options: list,
                 main_text: str,
                 pause=None
                 ):

        super().__init__()
        self.asteroids = None
        self.pause = pause

        self.space_ship_path = space_ship_path
        self.scale_enemy = scale_enemy
        self.texture = arcade.load_texture(f"../Backgrounds/{filename_background}")
        self.filename_background = f"../Backgrounds/{filename_background}"
        self.color_text = arcade_color_text
        self.selected_option = 0
        self.enemy_filename = enemy_filename
        self.options = options
        self.main_text = main_text
        self.count_meteor = count_meteor
        self.count_enemy = count_enemy
        self.setup()

    def setup(self):
        self.asteroids = arcade.SpriteList()
        path_meteors = [
            r"..\sprites\PNG\Meteors\meteorGrey_tiny1.png",
            r"..\sprites\PNG\Meteors\meteorGrey_med1.png",
            r"..\sprites\PNG\Meteors\meteorBrown_small1.png",
            r"..\sprites\PNG\Meteors\meteorGrey_big1.png",
            r"..\sprites\PNG\Meteors\meteorGrey_med1.png",
            r"..\sprites\PNG\Meteors\meteorGrey_small1.png",
            r"..\sprites\PNG\Meteors\meteorGrey_tiny2.png",
        ]
        interval_x = [el for el in range(0, self.window.width, 12)]
        interval_y = [el for el in range(0, self.window.height, 12)]
        for _ in range(10):
            meteor = Meteor(
                image=choice(path_meteors),
                x=choice(interval_x),
                y=choice(interval_y),
                min_speed=1,
                max_speed=3,
                flag=True
            )
            self.asteroids.append(meteor)

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

        self.asteroids.draw()

        title = arcade.Text(
            self.main_text,
            self.window.width // 2,
            self.window.height * 0.7,
            self.color_text,
            anchor_x="center",
            font_size=48
        )

        title.draw()

        for i, option in enumerate(self.options):
            color = arcade.color.WHITE if i == self.selected_option else arcade.color.GRAY
            text_option = arcade.Text(
                option,
                self.window.width // 2,
                self.window.height * 0.5 - i * 50,
                color, 32,
                anchor_x="center"
            )
            text_option.draw()

        hint_move_menu = arcade.Text(
            "↑↓ - выбор, ENTER - подтвердить, ESC - выход",
            self.window.width // 2, 50,
            arcade.color.LIGHT_GRAY, 16,
            anchor_x="center"
        )
        hint_move_menu.draw()

    @staticmethod
    def check_collisions_in_list(sprite_list):
        for i, sprite1 in enumerate(sprite_list):
            for sprite2 in sprite_list[i + 1:]:
                if arcade.check_for_collision(sprite1, sprite2):
                    sprite1.change_x *= -1
                    sprite1.change_y *= -1
                    sprite2.change_x *= -1
                    sprite2.change_y *= -1

    def on_update(self, delta_time: float):
        self.asteroids.update()
        self.check_collisions_in_list(self.asteroids)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif key == arcade.key.DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif key == arcade.key.ENTER or key == arcade.key.SPACE:
            self.select_option()
        elif key == arcade.key.ESCAPE:
            self.window.close()

    def select_option(self):
        if self.selected_option == 0:
            game = GameView(
                self.filename_background,
                self.enemy_filename,
                self.space_ship_path,
                self.count_enemy,
                self.count_meteor,
                self.scale_enemy
            )
            self.window.show_view(game)
        elif self.selected_option == 1:
            self.window.close()
        else:
            if self.pause is None:
                from utils import DataManager
                DataManager().update_data(1)
                info_level = settings.background_level[1]

                game = GameView(
                    f"../Backgrounds/{info_level[0]}",
                    info_level[3],
                    info_level[2],
                    info_level[4],
                    info_level[5],
                    info_level[6],
                )
                self.window.show_view(game)
            else:
                self.window.show_view(self.pause)