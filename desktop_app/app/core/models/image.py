import tkinter as tk
from typing import Any
from PIL import Image

class ImageFile:
    def __init__(self, image_path: str) -> None:
        self.image_path = image_path
        self.pil_image = Image.open(image_path)
        self.pil_image_opened = True
    
    def reopen_pil_image(self):
        self.pil_image = Image.open(self.image_path)
        self.pil_image_opened = True
    
    def close_pil_image(self):
        self.pil_image.close()
        self.pil_image_opened = False

    def __getattribute__(self, __name: str) -> None:
        if __name == "pil_image":
            if super().__getattribute__("pil_image_opened") == False:
                self.reopen_pil_image()
        return super().__getattribute__(__name)