from src.main_window import MyGame
from config import settings


def main():
    MyGame(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE).run()


if __name__ == '__main__':
    main()