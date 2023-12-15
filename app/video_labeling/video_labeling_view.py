from tkinter import Menu
from core.view import View
import tkinter as tk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .video_labeling_controller import LabelingController

class LabelingView(View):

    # WINDOW_TITLE = "Разметка видео"

    def __init__(self, controller: "LabelingController"):
        super().__init__(controller)
    
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
        pass