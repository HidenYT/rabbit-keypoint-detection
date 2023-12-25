import tkinter as tk
from .navbar import INavigator

class MainAppMixin(tk.Tk, INavigator):
    '''Интерфейс главного приложения. Совмещает в себе `Tk` и `INavigator`.'''
    pass