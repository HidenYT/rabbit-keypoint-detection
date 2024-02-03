import tkinter as tk
from PIL import Image

class ImageFile:
    def __init__(self, image_path: str) -> None:
        self.image_path = image_path
        self.pil_image = Image.open(image_path)
    
    def reopen(self):
        self.pil_image = Image.open(self.image_path)