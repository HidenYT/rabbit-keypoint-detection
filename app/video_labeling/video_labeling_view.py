from .video_labeling_controller import LabelingController
from core.page_view import PageView
import tkinter as tk

class LabelingView(PageView):

    WINDOW_TITLE = "Разметка видео"

    def __init__(self, controller: LabelingController):
        super().__init__(controller)

    def _init_menu(self) -> None:
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Выбрать кадры вручную")
        file_menu.add_command(label="Автоматический выбор кадров")
        file_menu.add_command(label="Добавить скелет")
        file_menu.add_command(label="Создать/Изменить скелет", command=self.controller.run_create_skeleton)
        file_menu.add_command(label="Сохранить всё")
        file_menu.add_command(label="Сохранить кадры")
        file_menu.add_command(label="Сохранить разметку json")
        file_menu.add_command(label="Сохранить разметку csv")
        file_menu.add_command(label="Сохранить разметку h5")
        self.menu.add_cascade(label="Файл", menu=file_menu)
    
    def _create_widgets(self):
        self.widgets = []
        self.config_widgets = {}