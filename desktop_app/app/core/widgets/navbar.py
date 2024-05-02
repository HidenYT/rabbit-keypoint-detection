import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

class INavigator(ABC):
    '''Интерфейс для классов, которые хотят обрабатывать нажатия на кнопки главного меню.'''
    @abstractmethod
    def go_to_frames_creation(self): pass
    
    @abstractmethod
    def go_to_skeleton_creation(self): pass
    
    @abstractmethod
    def go_to_frames_labeling(self): pass


class Navbar(tk.Frame):
    '''Главное меню, которое является фреймом `Frame`. 
    Содержит кнопки для перехода между представлениями. По нажатии на кнопку вызывает соответствующий метод переданного наследника `INavigator`.'''
    def __init__(self, navigator: INavigator, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        btn_create_frames = ttk.Button(self, text="Выбрать кадры для разметки", 
                                      command=navigator.go_to_frames_creation,
                                      style="navbar.TButton",
                                      takefocus=False)
        btn_create_skeleton = ttk.Button(self, text="Создать скелет", 
                                        command=navigator.go_to_skeleton_creation,
                                        style="navbar.TButton",
                                      takefocus=False)
        btn_frames_labeling = ttk.Button(self, text="Разметить кадры", 
                                        command=navigator.go_to_frames_labeling,
                                        style="navbar.TButton",
                                      takefocus=False)
        btns = [
            btn_create_frames,
            btn_create_skeleton,
            btn_frames_labeling,
        ]
        for i in range(len(btns)):
            self.columnconfigure(i, weight=1, uniform="uniform")
            btns[i].grid(row=0, column=i, sticky="nswe")