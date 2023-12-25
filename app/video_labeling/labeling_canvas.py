import tkinter as tk
from tkinter import Misc
from typing import Dict
from core.image import ImageFile
from PIL import ImageTk, Image

class LabelingCanvas(tk.Canvas):
    def __init__(self, master: Misc | None = None) -> None:
        self.imscale = 1.0
        super().__init__(master, bg="#ffffff")
        #self.create_oval(1000, 10, 1100, 110)
        def do_zoom(event):
            x = self.canvasx(event.x)
            y = self.canvasy(event.y)
            factor = 1.001 ** event.delta
            self.scale(tk.ALL, x, y, factor, factor)
            self.imscale*= factor
            self.zoom_image()
        self.bind("<Control-MouseWheel>", do_zoom)
        self.bind('<ButtonPress-1>', lambda event: self.scan_mark(event.x, event.y))
        self.bind("<B1-Motion>", lambda event: self.scan_dragto(event.x, event.y, gain=1))

        self.text = self.create_text(0, 0, anchor="nw", text="")

        self.image = None
        self.img_id = None
        
    
    def show_image(self, image: ImageFile, labels: Dict) -> None:
        self.image = image
        self.zoom_image()

    def zoom_image(self):
        if self.img_id is not None:
            self.delete(self.img_id)
        pil_img = self.image.pil_image
        w, h = pil_img.size
        new_size = (int(w*self.imscale), int(h*self.imscale))
        img = pil_img.resize(new_size)
        self.imagetk = ImageTk.PhotoImage(img)
        self.img_id = self.create_image(self.coords(self.text), anchor='nw', image=self.imagetk)
        self.lower(self.img_id)
        