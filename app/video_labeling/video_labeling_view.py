from tkinter import Menu
from core.view import View
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from core.scrollable_frame import VerticalScrolledFrame
from .labeling_canvas import LabelingCanvas
from core.image import ImageFile
from core.skeleton import Skeleton
from core.filetypes import csv_ft, png_ft, jpg_ft, images_ft

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from .video_labeling_controller import LabelingController

class LabelingView(View):
    def __init__(self, controller: "LabelingController"):
        super().__init__(controller)
        self.setup_content_frame()
        # Список изображений ImageFile
        self.images_list: List[ImageFile] = []
        
        # Список кнопок изображений
        self.img_buttons_list: List[tk.Button] = []

        # Список LabelinCanvas-ов. Каждый отвечает за своё изображение, хранит его разметку
        self.canvases: List[LabelingCanvas] = []

        # Открытый Canvas
        self.canvas: LabelingCanvas | None = None

        # Скелет
        self.skeleton: Skeleton | None = None
    
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
        # Frame для LabelingCanvas, находится слева
        self.canvas_frame = tk.Frame(self)

        # Frame для всех настроек и кнопок, находится справа
        self.configuration_frame = tk.Frame(self)
        self.setup_config_frame()

        self.grid_columnconfigure(0, weight=3, uniform=True)
        self.grid_columnconfigure(1, weight=2, uniform=True)
        self.grid_rowconfigure(0, weight=1, uniform=True)
        self.canvas_frame.grid(row=0, column=0, sticky="nsew")
        self.configuration_frame.grid(row=0, column=1, sticky="nsew")

    def setup_config_frame(self):
        config_frame = self.configuration_frame

        # Frame для списка изображений, находится вверху
        self.images_list_frame = images_list = self.create_images_list_frame()
        self.total_images_number = 0

        # Frame для всех кнопок, находится внизу
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
        return images_list
    
    def add_image_to_images_list(self, image_path: str):
        # ImageFile и LabelingCanvas, хранящий изображение
        image = ImageFile(image_path)
        canvas = LabelingCanvas(self.canvas_frame, image)

        # Отображаем скелет, если он есть
        if self.skeleton is not None: canvas.set_skeleton(self.skeleton)
        
        # Кнопка для открытия изображения
        btn_image = tk.Button(
            self.images_list_frame.interior, 
            text=f"{image_path}", 
            command=lambda: self.show_canvas(canvas),
            anchor="e"
        )

        # Добавляем всё в списки
        self.images_list.append(image)
        self.img_buttons_list.append(btn_image)
        self.canvases.append(canvas)
        self.total_images_number += 1

        # Отображаем
        btn_image.grid(row=self.total_images_number, column=0, sticky="nsew")
    
    def remove_image_from_images_list(self, idx: int):
        self.images_list.pop(idx)
        self.canvases.pop(idx)
        self.img_buttons_list.pop(idx).destroy()

    def show_canvas(self, canvas: LabelingCanvas):
        """Открыть и показать заданный `LabelingCanvas` в `Frame`-е для `LabelingCanvas`-ов"""
        # Убираем старый Canvas
        if self.canvas is not None:
            self.canvas.pack_forget()
        # Ставим переданный
        self.canvas = canvas
        canvas.pack(fill=tk.BOTH, expand=True)

    def create_action_menu(self) -> tk.Frame:
        menu = tk.Frame(self.configuration_frame)
        btn_add_image = ttk.Button(menu, text="Добавить изображения", command=self.add_images)
        btn_choose_skeleton = ttk.Button(menu, text="Выбрать скелет", command=self.choose_skeleton)
        btn_save_labels = ttk.Button(menu, text="Сохранить разметку", command=self.save_labels)
        btn_add_image.pack(fill=tk.BOTH, side=tk.BOTTOM)
        btn_choose_skeleton.pack(fill=tk.BOTH, side=tk.BOTTOM)
        btn_save_labels.pack(fill=tk.BOTH, side=tk.BOTTOM)
        return menu

    def add_images(self):
        images = filedialog.askopenfilenames(filetypes=[images_ft, png_ft, jpg_ft])
        if not images: return
        for img_path in images:
            self.add_image_to_images_list(img_path)
        
    def choose_skeleton(self):
        skeleton = filedialog.askopenfile(
            defaultextension=".csv", 
            filetypes=[csv_ft]
        )
        if not skeleton: return
        self.skeleton = skeleton = self.controller.open_skeleton(skeleton)
        if skeleton is not None:
            for canvas in self.canvases:
                canvas.set_skeleton(skeleton)
    
    def save_labels(self):
        file = filedialog.asksaveasfile(defaultextension="", filetypes=[csv_ft])
        if file is not None:
            self.controller.save_labels(self.canvases, file)