from typing import Dict
import tkinter as tk
from tkinter import ttk
from core.view import View
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nn_inference_controller import InferenceController

class InferenceView(View):

    WINDOW_TITLE = "Запуск нейросети"

    def __init__(self, controller: "InferenceController"):
        super().__init__(controller)

    def create_menu(self) -> tk.Menu:
        menu = tk.Menu(self.controller.root)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Добавить видео")
        file_menu.add_command(label="Выбрать нейросеть")
        menu.add_cascade(label="Файл", menu=file_menu)
        return menu
    
    def setup_content_frame(self) -> None:
        lbl_save_option = tk.Label(master=self.content_frame, text="Сохранить результаты в виде...")

        cmb_save_options = ttk.Combobox(
            master=self.content_frame, 
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

        lbl_save_name = tk.Label(master=self.content_frame, text="Название файла (каталога при сохранении кадров)")
        ent_save_name = tk.Entry(master=self.content_frame, )

        lbl_save_path = tk.Label(master=self.content_frame, text="Сохранить в...")
        ent_save_path = tk.Entry(master=self.content_frame, )

        btn_run = tk.Button(master=self.content_frame, text="Запустить", command=self.run_click)
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
        for w in self.widgets:
            w.pack()
    
    def run_click(self):
        config = {}
        for k, v in self.config_widgets.items():
            config[k] = v.get()
        self.controller.process(config)