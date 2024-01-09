from typing import TYPE_CHECKING
import tkinter as tk
from tkinter import ttk, filedialog
from .video_frame_change_listener import VideoFrameChangeListener
from .video_frame import VideoFrame
from core.mvc.view import View
from core.filetypes import videos_ft


if TYPE_CHECKING:
    from .frames_selection_controller import FramesSelectionController

class FramesSelectionView(View["FramesSelectionController"], VideoFrameChangeListener):
    def __init__(self, controller: "FramesSelectionController") -> None:
        super().__init__(controller)
        self.setup_content_frame()

    def setup_content_frame(self):
        self.video_frame = self.setup_video_frame()
        self.right_panel = self.setup_left_panel()
        self.video_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        self.right_panel.pack(side='right', fill='both', expand=True)

    def setup_video_frame(self) -> VideoFrame:
        return VideoFrame(self, controller=self.controller, frame_change_listener=self)

    def setup_left_panel(self) -> tk.Frame:
        frm = tk.Frame(self)
        btn_choose_video = ttk.Button(frm, text="Открыть видео", command=self.on_open_video)
        btn_choose_video.pack(fill="x")
        return frm
    
    def on_open_video(self):
        file = filedialog.askopenfilename(
            defaultextension='', 
            filetypes=[videos_ft]
        )
        if not file: return
        frames_n = self.controller.open_video(file)
        self.video_frame.set_frames_n(frames_n)
        self.on_video_frame_change_complete(0)

    def on_video_frame_change(self, frame_n: int):
        pass

    def on_video_frame_change_complete(self, frame_n: int):
        img = self.controller.get_video_frame(frame_n)
        if img is not None: self.video_frame.canvas.set_image(img)