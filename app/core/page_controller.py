from abc import ABC
import main_app

class PageController(ABC):
    def __init__(self, root: "main_app.MainApp"):
        self.root = root
