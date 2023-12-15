from core.view import View
import tkinter as tk
from tkinter import ttk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .nn_learning_controller import LearningController

class LearningView(View):

    # WINDOW_TITLE = "Обучение нейросети"

    def __init__(self, controller: "LearningController") -> None:
        super().__init__(controller)

    def create_menu(self) -> tk.Menu:
        menu = tk.Menu(self.controller.root)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Выбрать папку с кадрами и разметкой")
        file_menu.add_command(label="Выбрать кадры для обучения")
        file_menu.add_command(label="Выбрать разметку для обучения")
        menu.add_cascade(label="Файл", menu=file_menu)
        return menu

    def setup_content_frame(self):
        nn_select_list = ttk.Combobox(
            state="readonly",
            values=[
                "DeepLabCut", 
                "SLEAP", 
                "DeepPoseKit",
                "Self-made NN",
            ],
            master=self.content_frame,
        )
        nn_select_list.current(0)
        
        test_btn1 = tk.Checkbutton(text="Опция 1", master=self.content_frame)

        test_label = tk.Label(self.content_frame, text="Learning rate")
        
        test_entry = tk.Entry(self.content_frame)

        widgets = [
            nn_select_list,
            test_btn1,
            test_label,
            test_entry,
        ]
        for w in widgets:
            w.pack()