import os
from tkinter import messagebox
import pandas as pd
from .data_saving.datasets.dataset_saver_selector import DatasetSaverSelector
from .data_saving.labels.label_saver_selector import LabelSaverSelector
from core.mvc.view import View
from core.mvc.controller import ControllerNavigator
from .video_labeling_view import LabelingView
from core.models.skeleton import DefaultSkeleton, Skeleton
from core.filetypes import json_ft, csv_ft
from typing import List, TYPE_CHECKING
from .labeling_canvas import LabelingCanvas
if TYPE_CHECKING:
    from main_app import MainApp


class LabelingController(ControllerNavigator):

    def __init__(self, root: "MainApp") -> None:
        super().__init__(root)
        self.skeleton: Skeleton | None = DefaultSkeleton()

    def create_view(self) -> View:
        view = LabelingView(self)
        view.skeleton = self.skeleton
        return view
    
    def open_skeleton(self, file) -> Skeleton | None:
        self.skeleton = Skeleton.read_skeleton_from_csv(file)
        return self.skeleton
    
    def open_labels(self, file: str) -> pd.DataFrame:
        _, ext = os.path.splitext(file)
        if ext in csv_ft[1]:
            return pd.read_csv(file, header=[0, 1], encoding="utf-16")
        raise Exception(f"Can't open labels with extension {ext}")

    def save_labels(self, canvases: List[LabelingCanvas], file: str):
        if self.skeleton is None: 
            show_no_skeleton_warning()
            return
        label_saver_selector = LabelSaverSelector(file)
        label_saver = label_saver_selector.select_saver(canvases, self.skeleton)
        try:
            label_saver.save()
        except Exception as e:
            show_labels_save_fail(str(e))
        else:
            show_labels_save_success()
        
    def save_dataset(self, canvases: List[LabelingCanvas], file_path: str):
        if self.skeleton is None: 
            show_no_skeleton_warning()
            return
        saver_selector = DatasetSaverSelector(file_path)
        saver = saver_selector.select_saver(canvases, self.skeleton)
        try:
            saver.save()
        except Exception as e:
            show_labels_save_fail(str(e))
        else:
            show_labels_save_success()

def show_no_skeleton_warning():
    messagebox.showwarning("Скелет не был выбран", "Невозможно сохранить разметку, так как скелет не был выбран.")

def show_labels_save_success():
    messagebox.showinfo("Сохранение разметки", "Сохранение успешно завершено.")

def show_labels_save_fail(e: str):
    messagebox.showerror("Сохранение разметки", f"При сохранении разметки произошла ошибка: {e}.")