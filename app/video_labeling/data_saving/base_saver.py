from typing import List, IO
from abc import ABC, abstractmethod
from core.models.skeleton import Skeleton
from video_labeling.labeling_canvas import LabelingCanvas


class BaseLabelDataSaver(ABC):
    def __init__(self, canvases: List[LabelingCanvas], skeleton: Skeleton, file: str | IO[bytes] | IO[str]) -> None:
        self._canvases = canvases
        self._file = file
        self._skeleton = skeleton
    
    @abstractmethod
    def save(self): pass
