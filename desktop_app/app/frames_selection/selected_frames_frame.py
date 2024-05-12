import tkinter as tk
from tkinter import ttk
from typing import Dict
from .frames_selection_manager import FrameSelectionListener
from core.widgets.scrollable_frame import VerticalScrolledFrame
from .video_frame_change_listener import VideoFrameChangeListener


class SelectedFramesFrame(VerticalScrolledFrame,
                          FrameSelectionListener):
    def __init__(self, master, frame_change_listener: VideoFrameChangeListener):
        super().__init__(master)
        self.frame_change_listener = frame_change_listener
        self.frame_buttons: Dict[int, ttk.Button] = {}

    def redraw_buttons(self):
        btns = sorted(list(self.frame_buttons.items()))
        for btn in btns:
            btn[1].pack_forget()
        for btn in btns:
            btn[1].pack(fill='x', expand=True)
    
    def on_selected(self, frame_idx: int):
        def choose_frame():
            self.frame_change_listener.on_video_frame_change_complete(frame_idx)
        btn_frame = ttk.Button(self.interior,
                               text=str(frame_idx),
                               command=choose_frame,
                               style="default.TButton")
        self.frame_buttons[frame_idx] = btn_frame
        self.redraw_buttons()

    def on_removed(self, frame_idx: int):
        btn = self.frame_buttons[frame_idx]
        btn.destroy()
        del self.frame_buttons[frame_idx]

    def on_selection_clear(self):
        for btn in self.frame_buttons.values():
            btn.destroy()
        self.frame_buttons.clear()