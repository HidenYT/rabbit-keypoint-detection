from abc import ABC, abstractmethod

class FrameSelectionListener(ABC):
    @abstractmethod
    def on_selected(self, frame_idx: int): pass

    @abstractmethod
    def on_removed(self, frame_idx: int): pass

class FramesSelectionManager:

    def __init__(self, frame_selection_listener: FrameSelectionListener) -> None:
        self.selected_frames = set()
        self.listener = frame_selection_listener

    def select(self, frame_idx: int):
        self.selected_frames.add(frame_idx)
        self.listener.on_selected(frame_idx)
    
    def selected(self, frame_idx: int) -> bool:
        return frame_idx in self.selected_frames
    
    def remove(self, frame_idx: int):
        self.selected_frames.remove(frame_idx)
        self.listener.on_removed(frame_idx)

    def toggle(self, frame_idx: int):
        if self.selected(frame_idx):
            self.remove(frame_idx)
        else:
            self.select(frame_idx)