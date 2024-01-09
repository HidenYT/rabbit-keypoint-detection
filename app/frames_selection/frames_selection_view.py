from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2
from core.mvc.view import View
from core.filetypes import videos_ft


if TYPE_CHECKING:
    from .frames_selection_controller import FramesSelectionController

class VideoFrameChangeListener(ABC):
    @abstractmethod
    def on_video_frame_change(self, frame_n: int): pass

    @abstractmethod
    def on_video_frame_change_complete(self, frame_n: int): pass

class FramesSelectionView(View["FramesSelectionController"], VideoFrameChangeListener):
    def __init__(self, controller: "FramesSelectionController") -> None:
        super().__init__(controller)
        self.setup_content_frame()

    def setup_content_frame(self):
        self.video_frame = self.setup_video_frame()
        self.right_panel = self.setup_left_panel()
        self.video_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        self.right_panel.pack(side='right', fill='both', expand=True)

    def setup_video_frame(self) -> "VideoFrame":
        return VideoFrame(self, frame_change_listener=self)

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
        if file is None: return
        frames_n = self.controller.open_video(file)
        self.video_frame.set_frames_n(frames_n)
        self.on_video_frame_change_complete(0)

    def on_video_frame_change(self, frame_n: int):
        #print(frame_n)
        pass

    def on_video_frame_change_complete(self, frame_n: int):
        img = self.controller.get_video_frame(frame_n)
        if img is not None:
            self.video_frame.set_image(img)



class VideoFrame(tk.Frame):
    def __init__(self, 
                 master, 
                 frames_n: int = 99, 
                 frame_change_listener: VideoFrameChangeListener | None = None):
        super().__init__(master)

        self.frames_n = frames_n
        self.frame_change_listener = frame_change_listener
        
        self.video_frame = self.setup_video_frame()
        self.bottom_bar = self.setup_bottom_bar()
        self.video_frame.pack(side='top', fill='both', expand=True)
        self.bottom_bar.pack(side='bottom', fill='x')
    
    def set_frames_n(self, frames_n: int):
        self.frames_n = frames_n
        self.scale.config(to=frames_n-1)

    def set_frame_change_listener(self, listener: VideoFrameChangeListener):
        self.frame_change_listener = listener

    def remove_frame_change_listener(self):
        self.frame_change_listener = None

    def setup_video_frame(self) -> tk.Frame:
        frm = tk.Frame(self)
        self.canvas = image = tk.Canvas(frm)
        image.pack(fill='both', expand=True)
        return frm
    
    def set_image(self, pil_img: Image.Image):
        self.canvas.pack_forget()
        photo_img = ImageTk.PhotoImage(pil_img)
        self.canvas = tk.Canvas(self.video_frame)
        self.master.update()
        self.canvas_w, self.canvas_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.canvas.bind("<Configure>", lambda x: self.canvas_config())
        self.container = self.canvas.create_rectangle(0, 0, self.canvas_w, self.canvas_h, width=10)
        self.image = self.canvas.create_image(0, 0, anchor="nw", image=photo_img)
        self.photo_img = photo_img
        self.canvas.pack(fill='both', expand=True)

    def canvas_config(self):
        self.master.update()
        self.canvas_w, self.canvas_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.canvas.delete(self.container)
        self.container = self.canvas.create_rectangle(0, 0, self.canvas_w, self.canvas_h, width=10)
        self.image = self.canvas.create_image(0, 0, anchor="nw", image=self.photo_img)

    def setup_bottom_bar(self) -> tk.Frame:
        self.bottom_frame = frm = tk.Frame(self)
        self.scale = scale = ttk.Scale(frm, from_=0, to=self.frames_n-1, value=0, command=self.on_scale_changed)
        scale.bind("<ButtonRelease-1>", self.on_scale_changing_complete)

        scale.pack(fill='both', side='bottom', expand=True)
        return frm
    
    def on_scale_changed(self, value: str):
        frame_n = int(round(float(value)))
        if self.frame_change_listener is not None:
            self.frame_change_listener.on_video_frame_change(frame_n)

    def on_scale_changing_complete(self, event):
        frame_n = int(round(float(self.scale.get())))
        if self.frame_change_listener is not None:
            self.frame_change_listener.on_video_frame_change_complete(frame_n)
        