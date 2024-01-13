from tkinter import messagebox
from .data_saving.seven_zip_dataset_saver import SevenZipDSSaver
from .data_saving.label_saver_selector import LabelSaverSelector
from core.mvc.view import View
from core.mvc.controller import ControllerNavigator
from .video_labeling_view import LabelingView
from core.models.skeleton import DefaultSkeleton, Skeleton
from typing import List, TYPE_CHECKING
from .labeling_canvas import LabelingCanvas
if TYPE_CHECKING:
    from main_app import MainApp


class LabelingController(ControllerNavigator):

    def __init__(self, root: "MainApp") -> None:
        super().__init__(root)
        self.skeleton: Skeleton | None = None

    def create_view(self) -> View:
        view = LabelingView(self)
        view.skeleton = self.skeleton
        return view
    
    def open_skeleton(self, file) -> Skeleton | None:
        self.skeleton = Skeleton.read_skeleton_from_csv(file)
        return self.skeleton

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
        saver = SevenZipDSSaver(canvases, self.skeleton, file_path)
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