import os

class system():
    def __init__(self):
        pass

    def current_directory(self):
        return os.path.dirname(os.path.realpath(__file__))  

    def path_exists(self, file):
        return os.path.exists(file)