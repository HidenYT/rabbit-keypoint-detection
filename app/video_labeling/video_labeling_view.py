from tkinter import Menu
from core.view import View
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from core.scrollable_frame import VerticalScrolledFrame
from .labeling_canvas import LabelingCanvas
from core.image import ImageFile

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from .video_labeling_controller import LabelingController

class LabelingView(View):

    # WINDOW_TITLE = "Разметка видео"

    def __init__(self, controller: "LabelingController"):
        super().__init__(controller)
        self.setup_content_frame()
        # Список изображений ImageFile
        self.images_list: List[ImageFile] = []
        
        # Список кнопок изображений
        self.img_buttons_list: List[ttk.Button] = []
    
    def create_menu(self) -> Menu:
        menu = tk.Menu(self.controller.root)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Выбрать кадры вручную")
        file_menu.add_command(label="Автоматический выбор кадров")
        file_menu.add_command(label="Выбрать скелет")
        file_menu.add_command(label="Сохранить всё")
        file_menu.add_command(label="Сохранить кадры")
        file_menu.add_command(label="Сохранить разметку json")
        file_menu.add_command(label="Сохранить разметку csv")
        file_menu.add_command(label="Сохранить разметку h5")
        menu.add_cascade(label="Файл", menu=file_menu)
        return menu
    
    def setup_content_frame(self):
        self.canvas_frame = tk.Frame(self)
        self.configuration_frame = tk.Frame(self)
        self.setup_config_frame()
        self.setup_canvas_frame()
        self.grid_columnconfigure(0, weight=3, uniform=True)
        self.grid_columnconfigure(1, weight=2, uniform=True)
        self.grid_rowconfigure(0, weight=1, uniform=True)
        #self.canvas_frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        #self.configuration_frame.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)
        self.canvas_frame.grid(row=0, column=0, sticky="nsew")
        self.configuration_frame.grid(row=0, column=1, sticky="nsew")

    def setup_canvas_frame(self):
        canvas_frame = self.canvas_frame
        self.canvas = canvas = LabelingCanvas(canvas_frame)
        #canvas.setup()

        canvas.pack(expand=True, fill=tk.BOTH)

    def setup_config_frame(self):
        config_frame = self.configuration_frame
        self.images_list_frame = images_list = self.create_images_list_frame()
        self.total_images_number = 0
        action_menu = self.create_action_menu()
        
        config_frame.grid_rowconfigure(0, weight=1, uniform=True)
        config_frame.grid_rowconfigure(1, weight=1, uniform=True)
        config_frame.grid_columnconfigure(0, weight=1)
        images_list.grid(row=0, column=0, sticky="news")
        action_menu.grid(row=1, column=0, sticky="news")


    def create_images_list_frame(self) -> VerticalScrolledFrame:
        config_frame = self.configuration_frame
        images_list = VerticalScrolledFrame(config_frame)
        images_list.interior.grid_columnconfigure(0, weight=1, uniform=True)
        # interior = images_list.interior
        return images_list
    
    def add_image_to_images_list(self, image_path: str):
        image = ImageFile(image_path)
        def command():
            self.show_image(image)
        btn_image = tk.Button(
            self.images_list_frame.interior, 
            text=f"{image_path}", 
            command=command,
            anchor="e"
        )
        self.images_list.append(image)
        self.img_buttons_list.append(btn_image)
        btn_image.grid(row=self.total_images_number, column=0, sticky="nsew")
        self.total_images_number += 1
    
    def remove_image_from_images_list(self, idx: int):
        self.images_list.pop(idx)
        self.img_buttons_list.pop(idx).destroy()

    def show_image(self, image: ImageFile):
        self.canvas.show_image(image, {})


    def create_action_menu(self) -> tk.Frame:
        menu = tk.Frame(self.configuration_frame)
        btn_add_image = ttk.Button(menu, text="Добавить изображения", command=self.add_images)

        btn_add_image.pack(fill=tk.BOTH, side=tk.BOTTOM)
        return menu

    
    def add_images(self):
        images = filedialog.askopenfilenames(filetypes=[
            ("PNG", [".png"]),
            ("JPEG", [".jpg"])
        ])
        if not images: return
        for img_path in images:
            self.add_image_to_images_list(img_path)
        