from core.view import View
import tkinter as tk
from tkinter import ttk

class LearningView(View):

    WINDOW_TITLE = "Обучение нейросети"

    def _init_menu(self) -> None:
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Выбрать папку с кадрами и разметкой")
        file_menu.add_command(label="Выбрать кадры для обучения")
        file_menu.add_command(label="Выбрать разметку для обучения")
        self.menu.add_cascade(label="Файл", menu=file_menu)

    def _create_widgets(self):
        nn_select_list = ttk.Combobox(
            state="readonly",
            values=[
                "DeepLabCut", 
                "SLEAP", 
                "DeepPoseKit",
                "Self-made NN",
            ],
            master=self.frame,
        )
        nn_select_list.current(0)
        
        test_btn1 = tk.Checkbutton(text="Опция 1", master=self.frame)

        test_label = tk.Label(self.frame, text="Learning rate")
        
        test_entry = tk.Entry(self.frame)

        self.widgets = [
            nn_select_list,
            test_btn1,
            test_label,
            test_entry,
        ]