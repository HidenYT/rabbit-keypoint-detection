from typing import Literal
from frames_selection.auto_frames_selection.interfaces import FramesSource
from frames_selection.auto_frames_selection.kmeans_frames_selector import KMeansFramesSelector
from frames_selection.auto_frames_selection.random_frames_selector import RandomFramesSelector
from frames_selection.auto_frames_selection.uniform_frames_selector import UniformFramesSelector

SELECTION_RANDOM = "random_selection"
SELECTION_UNIFORM = "uniform_selection"
SELECTION_KMEANS = "kmeans_selection"


class AutoSelector:
    def __init__(self, 
                 total_frames: int,
                 sel_frames_n: int, 
                 selection_method: Literal["random_selection", "uniform_selection", "kmeans_selection"], 
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
            frames = RandomFramesSelector().select_frames(self.total_frames, self.sel_frames_n, self.frames_src)
        elif self.selection_method == SELECTION_UNIFORM:
            frames = UniformFramesSelector().select_frames(self.total_frames, self.sel_frames_n, self.frames_src)
        elif self.selection_method == SELECTION_KMEANS:
            frames = KMeansFramesSelector().select_frames(self.total_frames, self.sel_frames_n, self.frames_src)
        self.frames_nums = frames