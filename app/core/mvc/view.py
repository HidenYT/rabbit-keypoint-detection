from abc import ABC, abstractmethod
import tkinter as tk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .controller import ControllerNavigator

class View(ABC, tk.Frame):
    '''Базовый класс для представлений. При создании принимает контроллер, соответствующий данному представлению. Этому контроллеру представление будет передавать различные команды от пользовательского интерфейса.
    
    Представление - фрейм, который помещается основным приложением в его GUI. 
    '''
    def __init__(self, controller: "ControllerNavigator") -> None:
        super().__init__(controller.root.free_space)
        self.controller = controller
        self.content_frame = tk.Frame(self)

    @abstractmethod
    def create_menu(self) -> tk.Menu:
        '''Метод должен возвращать меню `Menu` данного представления.'''
        pass