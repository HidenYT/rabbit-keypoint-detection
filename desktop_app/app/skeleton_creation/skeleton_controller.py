from typing import List, Tuple
import tkinter as tk
import pandas as pd
from core.mvc.view import View
from core.mvc.controller import ControllerNavigator
from .skeleton_view import SkeletonEditWindow
from core.models.skeleton import Skeleton

class SkeletonController(ControllerNavigator):
    def create_skeleton_csv(self, 
                            entries_table: List[Tuple[tk.Entry, tk.Entry]],
                            file) -> None:
        '''Вызывается представлением, когда пользователь сохраняет csv файл скелета.'''
        # Получаем все значения таблицы скелета в виде списка пар значений.
        data = [(e1.get(), e2.get()) for e1, e2 in entries_table]
        # Создание и сохранение pandas DataFrame в csv фйал
        Skeleton.create_skeleton_csv(data, file)
    
    def read_csv(self, file):
        '''Вызывается представлением, когда пользователь открывает csv файл скелета.'''
        if file is not None:
            return pd.read_csv(file)
        else:
            return pd.DataFrame()
        
    def create_view(self) -> View:
        return SkeletonEditWindow(self)