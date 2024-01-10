from typing import TYPE_CHECKING
from datetime import datetime
import os
import cv2 as cv
from PIL import Image
from frames_selection.frames_selection_manager import FramesSelectionManager
from core.mvc.view import View
from core.mvc.controller import ControllerNavigator
from .frames_selection_view import FramesSelectionView
from tkinter import messagebox

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
        self.video_file_name = os.path.basename(file_path)
        self.video_capture = cv.VideoCapture(file_path)
        return int(self.video_capture.get(cv.CAP_PROP_FRAME_COUNT))
    
    def set_video_frame(self, n: int) -> Image.Image | None:
        if self.video_capture is None: return None
        self.video_capture.set(cv.CAP_PROP_POS_FRAMES, n)
        ret, frm = self.video_capture.read()
        if not ret: 
            raise IndexError(f"Frame #{n} can not be extracted from the video.")
        img = cv.cvtColor(frm, cv.COLOR_BGR2RGB)
        return Image.fromarray(img)
    
    def get_next_video_frame(self) -> Image.Image | None:
        if self.video_capture is None: return None
        ret, frm = self.video_capture.read()
        if ret: 
            img = cv.cvtColor(frm, cv.COLOR_BGR2RGB)
            return Image.fromarray(img)
        return None 

    def get_video_fps(self) -> int | None:
        if self.video_capture is not None: 
            return int(self.video_capture.get(cv.CAP_PROP_FPS))
        return None
    
    def get_video_frame_n(self) -> int | None:
        if self.video_capture is not None:
            return int(self.video_capture.get(cv.CAP_PROP_POS_FRAMES))
        return None

    def __del__(self):
        if self.video_capture is not None:
            self.video_capture.release()

    def save_frames(self, frames_selection_manager: FramesSelectionManager, directory_path):
        if self.video_capture is None: return
        tmp_pos = int(self.video_capture.get(cv.CAP_PROP_POS_FRAMES))-1
        dt_str = datetime.strftime(datetime.now(), "%d.%m.%Y_%H.%M.%S")
        file_name = "frame_{}.jpg"
        dir_name = f"Frames of {self.video_file_name} {dt_str}"
        directory_path = os.path.join(directory_path, dir_name)
        os.makedirs(directory_path, exist_ok=True)
        
        for frame_i in frames_selection_manager.selected_frames:
            self.video_capture.set(cv.CAP_PROP_POS_FRAMES, frame_i)
            ret, frm = self.video_capture.read()
            if ret:
                frm_name = file_name.format(frame_i)
                full_path = os.path.join(directory_path, frm_name)
                is_success, im_buf_arr = cv.imencode(".jpg", frm)
                if is_success:
                    im_buf_arr.tofile(full_path)
            else:
                messagebox.showwarning("Невозможно прочитать кадр", 
                                       f"Кадр {frame_i} не может быть прочтён.")
        self.video_capture.set(cv.CAP_PROP_POS_FRAMES, tmp_pos)