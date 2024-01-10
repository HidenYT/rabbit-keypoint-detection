import tkinter as tk
from tkinter import ttk
from typing import Dict
from core.widgets.scrollable_frame import VerticalScrolledFrame
from .video_frame_change_listener import VideoFrameChangeListener


class SelectedFramesFrame(VerticalScrolledFrame):
    def __init__(self, master, frame_change_listener: VideoFrameChangeListener):
        super().__init__(master)
        self.frame_change_listener = frame_change_listener
        self.frame_buttons: Dict[int, ttk.Button] = {}

    def select_frame(self, frame_n: int):
        def choose_frame():
            self.frame_change_listener.on_video_frame_change_complete(frame_n)
        btn_frame = ttk.Button(self.interior,
                               text=str(frame_n),
                               command=choose_frame)
        btn_frame.pack(fill='x', expand=True)
        self.frame_buttons[frame_n] = btn_frame

    def remove_frame(self, frame_n: int):
        btn = self.frame_buttons[frame_n]
        btn.destroy()