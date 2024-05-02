from random import sample
from frames_selection.auto_frames_selection.interfaces import FramesSelector, FramesSource


class RandomFramesSelector(FramesSelector):
    def select_frames(self, total_frames: int, sel_frames_n: int, frames_src: FramesSource) -> list[int]:
        return sample(range(total_frames), sel_frames_n)