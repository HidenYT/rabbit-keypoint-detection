from abc import ABC, abstractmethod
import os
from typing import List
from core.models.skeleton import Skeleton
from video_labeling.labeling_canvas import LabelingCanvas

class SaverSelector(ABC):
    def __init__(self, file_path: str):
        self._file_path = file_path
        _, self.ext = os.path.splitext(file_path)
    
    @abstractmethod
    def select_saver(self, canvases: List[LabelingCanvas], skeleton: Skeleton): pass