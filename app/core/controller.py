from abc import ABC, abstractmethod
import core.view as view
import tkinter as tk
import main_app

class Controller(ABC):
    def __init__(self, root: "main.MainApp"):
        self.root = root
        self.view = self._create_view()

    @abstractmethod
    def _create_view(self) -> "view.View": pass

    def show_view(self):
        self.view.frame.pack()
        self.root.title(self.view.WINDOW_TITLE)
        self.root.configure(menu=self.view.menu)
    
    def dismiss_view(self):
        self.root.initial_state()
        self.view.frame.pack_forget()

    @abstractmethod
    def process(self, config: dict): pass