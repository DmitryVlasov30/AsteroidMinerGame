import arcade


class Settings:
    SCREEN_WIDTH: int = 1000
    SCREEN_HEIGHT: int = 1000
    ogr_x: int = 2000
    ogr_y: int = 2000
    speed_lasers: int = 800
    scale_enemy: float = 0.5
    TITLE: str = "ASTEROID MINER"
    path_to_data: str = r"C:\Users\diwex\PycharmProjects\ArcadeGame\data.txt"
    background_level: dict = {
        1: ("black.png",
            arcade.color.AMARANTH_PURPLE,
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\playerShip1_blue.png",
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\ufoYellow.png",
            5,
            10,
            0.7
            ),
        2: (
            "blue.png",
            arcade.color.AMARANTH_PURPLE,
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\playerShip1_green.png",
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\ufoRed.png",
            10,
            20,
            0.6
            ),
        3: (
            "darkPurple.png",
            arcade.color.BLACK,
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\playerShip1_orange.png",
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\ufoGreen.png",
            20,
            30,
            0.5
            ),
        4: (
            "purple.png",
            arcade.color.BLACK,
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\playerShip1_red.png",
            r"C:\Users\diwex\PycharmProjects\ArcadeGame\sprites\PNG\ufoBlue.png",
            30,
            40,
            0.4
            ),
    }


settings = Settings()
