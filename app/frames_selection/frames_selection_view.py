from typing import TYPE_CHECKING
import tkinter as tk
from tkinter import ttk, filedialog
from frames_selection.selected_frames_frame import SelectedFramesFrame
from frames_selection.frames_selection_manager import FrameSelectionListener, FramesSelectionManager
from .video_frame_change_listener import VideoFrameChangeListener
from .video_frame import VideoFrame
from core.mvc.view import View
from core.filetypes import videos_ft
if TYPE_CHECKING:
    from .frames_selection_controller import FramesSelectionController


class FramesSelectionView(View["FramesSelectionController"], 
                          VideoFrameChangeListener,
                          FrameSelectionListener):
    def __init__(self, controller: "FramesSelectionController") -> None:
        super().__init__(controller)
        self.frames_selection_manager = FramesSelectionManager(self)
        self.setup_content_frame()

    def setup_content_frame(self):
        self.video_frame = self.setup_video_frame()
        self.right_panel = self.setup_left_panel()
        self.video_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        self.right_panel.pack(side='right', fill='both', expand=True)

    def setup_video_frame(self) -> VideoFrame:
        return VideoFrame(self, 
                          controller=self.controller, 
                          frame_change_listener=self,
                          frame_selection_manager=self.frames_selection_manager)

    def setup_left_panel(self) -> tk.Frame:
        frm = tk.Frame(self)
        btn_choose_video = ttk.Button(frm, text="Открыть видео", command=self.on_open_video)
        btn_choose_video.pack(fill="x")
        self.frm_selected_frames = SelectedFramesFrame(frm, self)
        self.frm_selected_frames.pack(fill='both', expand=True)
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
        img = self.controller.set_video_frame(frame_n)
        if img is not None: self.video_frame.set_image(img)

    def on_frame_selection_toggle(self, frame_idx: int):
        pass

    def on_selected(self, frame_idx: int):
        self.frm_selected_frames.select_frame(frame_idx)
    
    def on_removed(self, frame_idx: int):
        self.frm_selected_frames.remove_frame(frame_idx)