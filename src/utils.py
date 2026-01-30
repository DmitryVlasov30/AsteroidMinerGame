from config import settings


class DataManager:
    def __init__(self):
        self.path = settings.path_to_data

    def get_data(self):
        with open(self.path, "r") as file:
            level = int(file.read().strip())
        return level

    def update_data(self, level):
        with open(self.path, "w") as file:
            file.write(str(level))
