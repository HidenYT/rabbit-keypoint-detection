from abc import ABC, abstractmethod
import core.controller as controller
import tkinter as tk
from typing import List

class View(ABC):

    WINDOW_TITLE = None

    def __init__(self, controller: controller.Controller):
        self.widgets: List[tk.Widget] = []
        self.controller = controller
        self.frame = tk.Frame(self.controller.root)
        self._create_widgets()
        self._create_frame()
        self.menu = tk.Menu()
        self.menu.add_command(label="Назад", command=controller.dismiss_view)
        self._init_menu()
    
    @abstractmethod
    def _init_menu(self) -> None: pass

    @abstractmethod
    def _create_widgets(self): pass

    def _create_frame(self) -> tk.Frame: 
        frame = self.frame
        for widget in self.widgets:
            widget.pack()
        return frame