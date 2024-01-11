from tkinter import messagebox
from core.mvc.view import View
from core.mvc.controller import ControllerNavigator
from .video_labeling_view import LabelingView
import pandas as pd
from core.models.skeleton import DefaultSkeleton, Skeleton
from tkinter.messagebox import showwarning
from typing import List, TYPE_CHECKING
from .labeling_canvas import LabelingCanvas
import os
from core.filetypes import csv_ft, json_ft, hd5_ft
import h5py
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

    def save_labels(self, canvases: List[LabelingCanvas], file: str):
        if self.skeleton is None: 
            showwarning("Скелет не был выбран", "Невозможно сохранить разметку, так как скелет не был выбран.")
            return
        # Названия точек
        label_names = list(self.skeleton.nodes)
        # Названия столбцов в итоговом файле
        result_label_names = ["Image path"]
        for name in label_names:
            result_label_names.append(f"{name}_x")
            result_label_names.append(f"{name}_y")
        
        # Составляем таблицу данных
        data = []
        for canvas in canvases:
            row = []
            # Получаем координаты всех точек канваса
            coords = canvas.keypoint_manager.get_keypoints_coordinates()
            # Для каждой точки добавляем x и y
            for name in label_names:
                row.append(int(round(coords[name][0])))
                row.append(int(round(coords[name][1])))
            data.append(row)
        
        # Добавляем во все строки в первый столбец путь к изображению
        for i, row in enumerate(data):
            row.insert(0, canvases[i].image.image_path)
        # Создаём DF для удобного сохранения
        df = pd.DataFrame(data=data, columns=result_label_names)

        path, ext = os.path.splitext(file)
        try:
            if ext in csv_ft[1]:
                df.to_csv(file, index=False, encoding="utf-16")
            elif ext in json_ft[1]:
                df.to_json(file, force_ascii=False, orient='records')
            elif ext in hd5_ft[1]:
                # TODO Сделать сохранение в h5 и всего датасета в h5
                pass
                #df.to_hdf(file, key="labels")
            else:
                raise TypeError(f"Wrong file extension to save labels: {file}.")
        except Exception as e:
            messagebox.showerror("Сохранение разметки", f"При сохранении разметки произошла ошибка: {e}.")
        else:
            messagebox.showinfo("Сохранение разметки", "Сохранение успешно завершено.")