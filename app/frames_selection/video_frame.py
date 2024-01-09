import tkinter as tk
from tkinter import ttk
from .video_frame_canvas import VideoFrameCanvas
from .video_frame_change_listener import VideoFrameChangeListener

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .frames_selection_controller import FramesSelectionController

class VideoFrame(tk.Frame):
    def __init__(self, 
                 master,
                 controller: "FramesSelectionController", 
                 frames_n: int = 100, 
                 frame_change_listener: VideoFrameChangeListener | None = None):
        super().__init__(master)
        self.controller = controller

        self.frames_n = frames_n
        self.frame_change_listener = frame_change_listener
        self.playing = False
        
        self.video_frame = self.setup_video_frame()
        self.bottom_bar = self.setup_bottom_bar()
        self.video_frame.pack(side='top', fill='both', expand=True)
        self.bottom_bar.pack(side='bottom', fill='x')
    
    def set_frames_n(self, frames_n: int):
        self.frames_n = frames_n
        self.slider.config(to=frames_n-1, value=0)

    def set_frame_change_listener(self, listener: VideoFrameChangeListener):
        self.frame_change_listener = listener

    def remove_frame_change_listener(self):
        self.frame_change_listener = None

    def setup_video_frame(self) -> tk.Frame:
        frm = tk.Frame(self)
        self.canvas = canvas = VideoFrameCanvas(frm)
        canvas.pack(fill='both', expand=True)
        return frm

    def setup_bottom_bar(self) -> tk.Frame:
        self.bottom_frame = frm = tk.Frame(self)
        self.slider = slider = ttk.Scale(frm, from_=0, to=self.frames_n-1, value=0, command=self.on_slider_changed)
        slider.bind("<ButtonRelease-1>", self.on_slider_changing_complete)

        slider.pack(fill='both', side='left', expand=True)

        btn_play = ttk.Button(frm, text="Play", command=self.play_video)
        btn_pause = ttk.Button(frm, text="Pause", command=self.pause_video)

        btn_play.pack(side='left')
        btn_pause.pack(side='left')
        return frm
    
    def on_slider_changed(self, value: str):
        frame_n = int(round(float(value)))
        if self.frame_change_listener is not None:
            self.frame_change_listener.on_video_frame_change(frame_n)

    def on_slider_changing_complete(self, event):
        frame_n = int(round(float(self.slider.get())))
        if self.frame_change_listener is not None and not self.playing:
            self.frame_change_listener.on_video_frame_change_complete(frame_n)
        
    def play_video(self):
        if self.playing: return
        if self.controller.video_capture is None: return 
        # Иначе всё работает
        delay = int(1000/self.controller.get_video_fps())
        
        def play():
            if not self.playing: return
            img = self.controller.get_next_video_frame()
            if img is None: 
                self.pause_video()
                return
            self.canvas.set_image(img)
            self.slider.config(value=self.controller.get_video_frame_n())
            self.master.after(delay, play)
        self.slider.config(state="disabled")
        self.playing = True
        play()

    def pause_video(self):
        self.slider.config(state="normal")
        self.playing = False