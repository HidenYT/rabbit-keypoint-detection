from core.mvc.view import View
from core.mvc.controller import ControllerNavigator
from .nn_learning_view import LearningView

class LearningController(ControllerNavigator):
    
    def create_view(self) -> View:
        return LearningView(self)