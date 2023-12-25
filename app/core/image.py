import tkinter as tk
from PIL import Image

class ImageFile:
    def __init__(self, image_path) -> None:
        self.image_path = image_path
        self.pil_image = Image.open(image_path)
        self.tk_image = tk.PhotoImage(file=image_path)