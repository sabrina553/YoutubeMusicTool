import os

class system():
    def __init__(self):
        pass

    def current_directory(self):
        return os.path.dirname(os.path.realpath(__file__))  

    def path_exists(self, file):
        return os.path.exists(file)
    
    def folder_check(self, file):
        if not os.path.exists(file):
            os.makedirs(file)        
        if not os.path.exists(file+"/auth"):
            os.makedirs(file+"/auth")
        if not os.path.exists(file+"/cache"):
            os.makedirs(file+"/cache")