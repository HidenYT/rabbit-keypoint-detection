import tkinter as tk
from abc import ABC, abstractmethod

class BaseWindow(ABC, tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not isinstance(self.master, main.MainApp):
            raise Exception("Only MainApp can be the root of a window.")
        self.setup()

    @abstractmethod
    def get_window_title(self) -> str: pass

    def get_menu(self) -> tk.Menu:
        main_menu = tk.Menu(self.master)
        main_menu.add_command(label="Назад", command=self.back)
        self.setup_menu(main_menu)
        return main_menu
    
    @abstractmethod
    def setup_menu(self, menu: tk.Menu) -> None: pass

    @abstractmethod
    def setup(self) -> None: pass

    def back(self):
        self.pack_forget()
        self.master.initial_state()
