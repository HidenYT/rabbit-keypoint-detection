from abc import ABC, abstractmethod
from typing import Iterable, List, Literal, Tuple, Type
from random import sample
import numpy as np
from .dbscan_duplicates_finder import DBSCANDuplicatesFinder
from .duplicates_finder import DuplicatesFinder
from .hierarchical_duplicates_finder import HierarchicalDuplicatesFinder
from .kmeans_duplicates_finder import KMeansDuplicatesFinder


SELECTION_RANDOM = "random_selection"
SELECTION_UNIFORM = "uniform_selection"
DELETION_KMEANS = "kmeans_deletion"
DELETION_DBSCAN = "dbscan_deletion"
DELETION_HIERARCHICAL = "hierarchical_deletion"

class FramesSource(ABC):
    @abstractmethod
    def get_frames_by_indicies(self, indicies: Iterable[int]) -> List[np.ndarray]: pass

class AutoSelector:
    def __init__(self, 
                 total_frames: int,
                 sel_frames_n: int, 
                 selection_method: Literal["random_selection", "uniform_selection"], 
                 frames_src: FramesSource,
                 duplicates_deletion_method: Literal["kmeans_deletion", "dbscan_deletion", "hierarchical_deletion"] | None = None):
        self.total_frames = total_frames
        self.sel_frames_n = sel_frames_n
        self.frames_src = frames_src
        self.selection_method = selection_method
        self.duplicates_deletion_method = duplicates_deletion_method
        self.frames_nums = None
        self.duplicates = None
    
    def select_frames(self):
        frames = []
        if self.selection_method == SELECTION_RANDOM:
            frames = sample(range(self.total_frames), self.sel_frames_n)
        elif self.selection_method == SELECTION_UNIFORM:
            frames = list(map(int, np.round(np.linspace(0, self.total_frames-1, self.sel_frames_n))))
        self.frames_nums = frames
    
    def find_duplicates(self):
        if self.duplicates_deletion_method is None: 
            raise Exception("Can't find duplicates without deletion method.")
        if self.frames_nums is None: 
            raise Exception("Frames haven't been selected.")
        finder: DuplicatesFinder = {
            DELETION_KMEANS: KMeansDuplicatesFinder,
            DELETION_DBSCAN: DBSCANDuplicatesFinder,
            DELETION_HIERARCHICAL: HierarchicalDuplicatesFinder,
        }[self.duplicates_deletion_method]()
        images = self.frames_src.get_frames_by_indicies(self.frames_nums)
        images_and_idx = list(zip(self.frames_nums, images))
        duplicates = finder.find_duplicates(images_and_idx)
        self.duplicates = duplicates
    
    def remove_duplicates(self):
        if self.duplicates is None:
            raise Exception("Duplicates haven't been found.")
        cleared_frames = []
        for dupls in self.duplicates:
            cleared_frames.append(dupls[0])
        self.frames_nums = cleared_frames