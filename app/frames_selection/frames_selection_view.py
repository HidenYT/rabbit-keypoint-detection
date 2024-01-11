import os
from tkinter import messagebox
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
        lbl_info = tk.Label(frm, text="Выбранные кадры")
        lbl_info.pack(fill='x')
        self.frm_selected_frames = SelectedFramesFrame(frm, self)
        self.frm_selected_frames.pack(fill='both', expand=True)
        btn_choose_video = ttk.Button(frm, text="Открыть видео", command=self.on_open_video)
        btn_choose_video.pack(fill="x", side='bottom')
        btn_save = ttk.Button(frm, text="Сохранить кадры", command=self.save_selected_frames)
        btn_save.pack(fill='x', side='bottom')
        return frm
    
    def on_open_video(self):
        file = filedialog.askopenfilename(
            defaultextension='', 
            filetypes=[videos_ft]
        )
        if not file: return
        self.frames_selection_manager.clear()
        frames_n = self.controller.open_video(file)
        self.video_frame.set_frames_n(frames_n)
        self.on_video_frame_change_complete(0)

    def on_video_frame_change_complete(self, frame_n: int):
        self.controller.set_video_frame(frame_n)
        self.video_frame.update_frame()

    def on_selected(self, frame_idx: int):
        self.frm_selected_frames.select_frame(frame_idx)
    
    def on_removed(self, frame_idx: int):
        self.frm_selected_frames.remove_frame(frame_idx)

    def save_selected_frames(self):
        dir = filedialog.askdirectory().replace("/", os.sep)
        if dir:
            saved = self.controller.save_frames(self.frames_selection_manager, dir)
            if saved:
                messagebox.showinfo("Сохранение", "Файлы были успешно сохранены.")
            else:
                messagebox.showerror("Сохранение", "При сохранении произошла ошибка.")

    def on_selection_clear(self):
        self.frm_selected_frames.remove_all_frames()