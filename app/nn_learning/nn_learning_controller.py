from core.view import View
from core.controller import ControllerNavigator
from .nn_learning_view import LearningView

class LearningController(ControllerNavigator):
    
    def create_view(self) -> View:
        view = LearningView(self)
        view.create_frame()
        return view