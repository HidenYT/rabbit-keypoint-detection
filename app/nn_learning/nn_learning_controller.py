from core.controller import Controller
from core.view import View
from .nn_learning_view import LearningView

class LearningController(Controller):
    def _create_view(self) -> View:
        return LearningView(self)
    
    def process(self, config: dict):
        print(config)