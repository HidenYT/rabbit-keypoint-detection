import core.view as view
from core.controller import Controller
from .nn_inference_view import InferenceView

class InferenceController(Controller):
    def _create_view(self) -> view.View:
        return InferenceView(self)
    
    def process(self, config: dict):
        print(config)
        