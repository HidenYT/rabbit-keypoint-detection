from abc import ABC, abstractmethod
import core.page_controller as controller
import tkinter as tk
from typing import List

class PageView(ABC):

    WINDOW_TITLE = None

    def __init__(self, controller: controller.PageController):
        self.widgets: List[tk.Widget] = []
        self.controller = controller
        self.frame = tk.Frame(self.controller.root)
        self._create_widgets()
        self._create_frame()
        self.menu = tk.Menu()
        self._init_menu()
        self.menu.add_command(label="Назад", command=self.dismiss_view)
    
    @abstractmethod
    def _init_menu(self) -> None: pass

    @abstractmethod
    def _create_widgets(self): pass

    def _create_frame(self) -> tk.Frame: 
        frame = self.frame
        for widget in self.widgets:
            widget.pack()
        return frame
    
    def show_view(self):
        self.frame.pack()
        self.controller.root.title(self.WINDOW_TITLE)
        self.controller.root.configure(menu=self.menu)
    
    def dismiss_view(self):
        self.controller.root.initial_state()
        self.frame.pack_forget()