import os
from tkinter import messagebox
from typing import TYPE_CHECKING, Iterable, List
import tkinter as tk
from tkinter import ttk, filedialog
from .auto_frames_selection.interfaces import FramesSource
from .auto_frames_selection.auto_selection_window import AutoFrameSelectionWindow
from frames_selection.selected_frames_frame import SelectedFramesFrame
from frames_selection.frames_selection_manager import FramesSelectionManager
from .video_frame_change_listener import VideoFrameChangeListener
from .video_frame import VideoFrame
from core.mvc.view import View
from core.filetypes import videos_ft
from PIL import Image
if TYPE_CHECKING:
    from .frames_selection_controller import FramesSelectionController


class FramesSelectionView(View["FramesSelectionController"], 
                          VideoFrameChangeListener,
                          FramesSource):
    def __init__(self, controller: "FramesSelectionController") -> None:
        super().__init__(controller)
        self.setup_content_frame()

    def setup_content_frame(self):
        self.right_panel = self.setup_left_panel()
        self.video_frame = self.setup_video_frame()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=60, uniform="uniform")
        self.grid_columnconfigure(1, weight=40, uniform="uniform")
        self.video_frame.grid(column=0, row=0, sticky="news")
        self.right_panel.grid(column=1, row=0, sticky="news")

    def setup_video_frame(self) -> VideoFrame:
        return VideoFrame(self, 
                          controller=self.controller, 
                          frame_change_listener=self,
                          frame_selection_manager=self.frames_selection_manager)

    def setup_left_panel(self) -> tk.Frame:
        frm = tk.Frame(self)
        lbl_info = ttk.Label(frm, text="Выбранные кадры", anchor="center", style="default.TLabel")
        lbl_info.pack(fill='x')
        self.frm_selected_frames = SelectedFramesFrame(frm, self)
        self.frames_selection_manager = FramesSelectionManager(self.frm_selected_frames)
        self.frm_selected_frames.pack(fill='both', expand=True)
        bottom_panel = ttk.Frame(frm)
        btn_choose_video = ttk.Button(bottom_panel, text="Открыть видео", command=self.on_open_video, style="default.TButton")
        btn_choose_video.pack(fill="x", side='bottom')
        btn_save = ttk.Button(bottom_panel, text="Сохранить кадры", command=self.save_selected_frames, style="default.TButton")
        btn_save.pack(fill='x', side='bottom')
        btn_auto_select = ttk.Button(bottom_panel, text="Автоматическая выборка", command=self.open_auto_selection_window, style="default.TButton")
        btn_auto_select.pack(fill='x', side='bottom')
        sep = ttk.Separator(bottom_panel, orient="horizontal")
        sep.pack(fill="x", side="bottom", pady=(10, 10))
        bottom_panel.pack(fill='x', side="bottom")
        return frm
    
    def open_auto_selection_window(self):
        if self.controller.video_capture is None: return
        AutoFrameSelectionWindow(self, self.video_frame.frames_n, self, self.frames_selection_manager).mainloop()
    
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

    def save_selected_frames(self):
        dir = filedialog.askdirectory().replace("/", os.sep)
        if dir:
            saved = self.controller.save_frames(self.frames_selection_manager, dir)
            if saved:
                messagebox.showinfo("Сохранение", "Файлы были успешно сохранены.")
            else:
                messagebox.showerror("Сохранение", "При сохранении произошла ошибка.")

    def get_frames_by_indicies(self, indicies: Iterable[int]) -> List[Image.Image]:
        current_cap_idx = self.controller.get_showing_frame_n()+1
        result: List[Image.Image] = []
        for idx in indicies:
            self.controller.set_video_frame(idx)
            img = self.controller.get_current_frame()
            if img is None: 
                raise Exception(f"Image at index {idx} is not available.")
            result.append(img)
        self.controller.set_video_frame(current_cap_idx)
        return result