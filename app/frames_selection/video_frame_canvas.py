from typing import Tuple
from PIL import Image, ImageTk
import tkinter as tk


class VideoFrameCanvas(tk.Canvas):
    def set_image(self, pil_img: Image.Image):
        self.pil_img = pil_img
        self.canvas_w, self.canvas_h = self.winfo_width(), self.winfo_height()
        self.photo_img = photo_img = ImageTk.PhotoImage(pil_img.resize(self.calculate_good_img_size()))
        self.bind("<Configure>", lambda x: self.canvas_config())
        self.image = self.create_image(*self.calculate_good_img_position(), anchor="nw", image=photo_img)
    
    def canvas_config(self):
        self.canvas_w, self.canvas_h = self.winfo_width(), self.winfo_height()
        self.photo_img = ImageTk.PhotoImage(self.pil_img.resize(self.calculate_good_img_size()))
        self.image = self.create_image(*self.calculate_good_img_position(), anchor="nw", image=self.photo_img)

    def calculate_good_img_size(self) -> Tuple[int, int]:
        ratio = self.pil_img.width/self.pil_img.height
        result_w, result_h = self.pil_img.size
        if result_w > self.canvas_w:
            result_w = self.canvas_w
            result_h = result_w/ratio
        if result_h > self.canvas_h:
            result_h = self.canvas_h
            result_w = ratio * result_h
        return int(result_w), int(result_h)

    def calculate_good_img_position(self):
        img_sz = self.calculate_good_img_size()
        mid_w_canv = self.canvas_w/2
        mid_w_img = img_sz[0]/2
        mid_h_canv = self.canvas_h/2
        mid_h_img = img_sz[1]/2
        return int(mid_w_canv-mid_w_img), int(mid_h_canv-mid_h_img)
    