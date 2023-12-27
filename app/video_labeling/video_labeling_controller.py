from core.view import View
from core.controller import ControllerNavigator
from .video_labeling_view import LabelingView
import pandas as pd

class LabelingController(ControllerNavigator):
    
    def create_view(self) -> View:
        return LabelingView(self)
    
    def open_skeleton(self, file) -> pd.DataFrame:
        return pd.read_csv(file)