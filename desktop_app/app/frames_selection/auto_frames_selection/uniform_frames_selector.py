import numpy as np
from frames_selection.auto_frames_selection.interfaces import FramesSelector, FramesSource


class UniformFramesSelector(FramesSelector):
    def select_frames(self, total_frames: int, sel_frames_n: int, frames_src: FramesSource) -> list[int]:
        return list(map(int, np.round(np.linspace(0, total_frames-1, sel_frames_n))))