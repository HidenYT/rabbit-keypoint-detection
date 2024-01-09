from typing import TYPE_CHECKING
import cv2 as cv
from PIL import Image
from core.mvc.view import View
from core.mvc.controller import ControllerNavigator
from .frames_selection_view import FramesSelectionView

if TYPE_CHECKING:
    from main_app import MainApp

class FramesSelectionController(ControllerNavigator):
    def __init__(self, root: "MainApp") -> None:
        super().__init__(root)
        self.video_capture: cv.VideoCapture | None = None

    def create_view(self) -> View:
        return FramesSelectionView(self)
    
    def open_video(self, file_path: str) -> int:
        """Открывает видео и возвращает количество кадров в нём."""
        self.video_capture = cv.VideoCapture(file_path)
        return int(self.video_capture.get(cv.CAP_PROP_FRAME_COUNT))
    
    def get_video_frame(self, n: int) -> Image.Image | None:
        if self.video_capture is None: return None
        self.video_capture.set(cv.CAP_PROP_POS_FRAMES, n)
        ret, frm = self.video_capture.read()
        if not ret: 
            raise IndexError(f"Frame #{n} can not be extracted from the video.")
        img = cv.cvtColor(frm, cv.COLOR_BGR2RGB)
        return Image.fromarray(img)