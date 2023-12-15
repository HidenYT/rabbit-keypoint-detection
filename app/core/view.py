from abc import ABC, abstractmethod
import tkinter as tk
from .navbar import Navbar 

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .controller import ControllerNavigator

class View(ABC, tk.Frame):
    def __init__(self, controller: "ControllerNavigator") -> None:
        super().__init__(controller.root.free_space)
        self.controller = controller
        self.content_frame = tk.Frame(self)

    @abstractmethod
    def create_menu(self) -> tk.Menu:
        pass

    @abstractmethod
    def setup_content_frame(self):
        pass

    def create_frame(self):
        self.setup_content_frame()
        self.content_frame.pack(fill="both", expand=True)