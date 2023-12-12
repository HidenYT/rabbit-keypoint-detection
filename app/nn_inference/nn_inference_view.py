from typing import Dict
import tkinter as tk
from tkinter import ttk
from core.controller import Controller
from core.view import View

class InferenceView(View):

    WINDOW_TITLE = "Запуск нейросети"

    def _init_menu(self) -> tk.Menu:
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Добавить видео")
        file_menu.add_command(label="Выбрать нейросеть")
        self.menu.add_cascade(label="Файл", menu=file_menu)
    
    def _create_widgets(self) -> None:
        lbl_save_option = tk.Label(master=self.frame, text="Сохранить результаты в виде...")

        cmb_save_options = ttk.Combobox(
            master=self.frame, 
            state="readonly",
            values=[
                "Файл разметки json",
                "Файл разметки csv",
                "Файл разметки h5",
                "Видео с разметкой",
                "Кадры с разметкой",
            ]
        )
        cmb_save_options.current(0)

        lbl_save_name = tk.Label(master=self.frame, text="Название файла (каталога при сохранении кадров)")
        ent_save_name = tk.Entry(master=self.frame, )

        lbl_save_path = tk.Label(master=self.frame, text="Сохранить в...")
        ent_save_path = tk.Entry(master=self.frame, )

        btn_run = tk.Button(master=self.frame, text="Запустить", command=self.run_click)
        self.widgets = [
            lbl_save_option,
            cmb_save_options,
            lbl_save_name,
            ent_save_name,
            lbl_save_path,
            ent_save_path,
            btn_run
        ]

        self.config_widgets: Dict[str, tk.Widget] = {
            "file_format": cmb_save_options,
            "file_name": ent_save_name,
            "file_path": ent_save_path,
        }
    
    def run_click(self):
        config = {}
        for k, v in self.config_widgets.items():
            config[k] = v.get()
        self.controller.process(config)