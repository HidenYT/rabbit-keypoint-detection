import core.view as view
from core.controller import Controller
from .video_labeling_view import LabelingView

class LabelingController(Controller):
    def _create_view(self) -> view.View:
        return LabelingView(self)
    
    def process(self, data: dict):
        print(data)