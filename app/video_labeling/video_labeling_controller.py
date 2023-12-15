from core.view import View
from core.controller import ControllerNavigator
from .video_labeling_view import LabelingView

class LabelingController(ControllerNavigator):
    
    def create_view(self) -> View:
        view = LabelingView(self)
        view.create_frame()
        return view