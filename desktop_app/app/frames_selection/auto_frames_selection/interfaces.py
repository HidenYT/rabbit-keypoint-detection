from abc import ABC, abstractmethod
from typing import Iterable, List
from PIL import Image

class FramesSource(ABC):
    @abstractmethod
    def get_frames_by_indicies(self, indicies: Iterable[int]) -> List[Image.Image]: pass

class FramesSelector(ABC):
    @abstractmethod
    def select_frames(self, total_frames: int, sel_frames_n: int, frames_src: FramesSource) -> list[int]:
        pass