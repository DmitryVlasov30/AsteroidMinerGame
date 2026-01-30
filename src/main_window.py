from start_menu import MainMenu
from config import settings

import arcade


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        from utils import DataManager
        self.level = DataManager().get_data()
        config_data = settings.background_level[self.level]
        self.sound_background = arcade.load_sound("../Star Wars (Main Theme).m4a")
        arcade.play_sound(self.sound_background, loop=True)

        menu = MainMenu(
            *config_data,
            options=["НОВАЯ ИГРА", "ВЫХОД"],
            main_text="ASTEROID MINER"
        )
        self.show_view(menu)


def setup_game(width=settings.SCREEN_WIDTH, height=settings.SCREEN_HEIGHT, title=settings.TITLE):
    game = MyGame(width, height, title)
    return game


def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
