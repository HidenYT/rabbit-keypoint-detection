from abc import ABC, abstractmethod
from typing import Iterable, List, Literal
import numpy as np
from .kmeans_cluster_finder import KMeansImageClustersFinder

SELECTION_RANDOM = "random_selection"
SELECTION_UNIFORM = "uniform_selection"

class FramesSource(ABC):
    @abstractmethod
    def get_frames_by_indicies(self, indicies: Iterable[int]) -> List[np.ndarray]: pass

    @abstractmethod
    def get_all_frames(self) -> List[np.ndarray]: pass

class AutoSelector:
    def __init__(self, 
                 total_frames: int,
                 sel_frames_n: int, 
                 selection_method: Literal["random_selection", "uniform_selection"], 
                 frames_src: FramesSource):
        self.total_frames = total_frames
        self.sel_frames_n = sel_frames_n
        self.frames_src = frames_src
        self.selection_method = selection_method
        self.frames_nums = None
        self.duplicates = None
    
    def select_frames(self):
        frames = []
        if self.selection_method == SELECTION_RANDOM:
            frames = KMeansImageClustersFinder().get_image_indicies(self.sel_frames_n, self.frames_src.get_all_frames())
        elif self.selection_method == SELECTION_UNIFORM:
            frames = list(map(int, np.round(np.linspace(0, self.total_frames-1, self.sel_frames_n))))
        self.frames_nums = frames