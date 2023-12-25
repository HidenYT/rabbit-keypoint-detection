from core.controller import ControllerNavigator
from core.view import View
from .nn_inference_view import InferenceView

class InferenceController(ControllerNavigator):

    def create_view(self) -> View:
        return InferenceView(self)

    def process(self, data: dict):
        print(data)    
        