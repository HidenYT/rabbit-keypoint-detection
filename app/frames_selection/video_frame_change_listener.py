from abc import ABC, abstractmethod


class VideoFrameChangeListener(ABC):
    @abstractmethod
    def on_video_frame_change(self, frame_n: int): pass

    @abstractmethod
    def on_video_frame_change_complete(self, frame_n: int): pass