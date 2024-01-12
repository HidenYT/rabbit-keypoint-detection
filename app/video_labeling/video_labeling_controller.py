from copy import deepcopy
from tkinter import messagebox
import numpy as np
from core.mvc.view import View
from core.mvc.controller import ControllerNavigator
from .video_labeling_view import LabelingView
import pandas as pd
from core.models.skeleton import DefaultSkeleton, Skeleton
from tkinter.messagebox import showwarning
from typing import Iterable, List, TYPE_CHECKING, Sequence
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
        data: List[List[int]] = []
        for canvas in canvases:
            row = []
            # Получаем координаты всех точек канваса
            coords = canvas.keypoint_manager.get_keypoints_coordinates()
            # Для каждой точки добавляем x и y
            for name in label_names:
                row.append(int(round(coords[name][0])))
                row.append(int(round(coords[name][1])))
            data.append(row)
        
        # Создаём таблицу для данных, в которых помимо точек будут пути к файлам
        data_with_paths: List[List[int | str]] = deepcopy(data)
        
        # Список путей к изображениям
        images_paths = []

        # Добавляем во все строки в первый столбец путь к изображению
        for i, row in enumerate(data_with_paths):
            row.insert(0, canvases[i].image.image_path)
            images_paths.append(canvases[i].image.image_path)

        path, ext = os.path.splitext(file)
        try:
            # Создаём DF для удобного сохранения
            if ext in csv_ft[1] or ext in json_ft[1]:
                df = pd.DataFrame(data=data_with_paths, columns=result_label_names)
                if ext in csv_ft[1]:
                    df.to_csv(file, index=False, encoding="utf-16")
                elif ext in json_ft[1]:
                    df.to_json(file, force_ascii=False, orient='records')
            elif ext in hd5_ft[1]:
                self.save_labels_to_h5(file, label_names, data, images_paths)
            else:
                raise TypeError(f"Wrong file extension to save labels: {file}.")
        except Exception as e:
            messagebox.showerror("Сохранение разметки", f"При сохранении разметки произошла ошибка: {e}.")
        else:
            messagebox.showinfo("Сохранение разметки", "Сохранение успешно завершено.")

    def save_labels_to_h5(self, file_path: str, label_names: List[str], paths_and_labels: List[List[int]], paths: List[str]):
        # Пути к файлам
        image_paths = np.array(paths, dtype=np.unicode_)

        # Названия точек
        label_names_data = np.array(label_names)
        
        # Составляем матрицу данных
        labels_data = np.array(paths_and_labels, dtype=np.int32)

        with h5py.File(file_path, 'w') as f:
            skeleton_dset = f.create_dataset("skeleton", label_names_data.shape, dtype=h5py.string_dtype())
            skeleton_dset[:] = label_names_data
        
            labels_dset = f.create_dataset("labels", labels_data.shape)
            labels_dset[:] = labels_data

            paths_dset = f.create_dataset("image_paths", image_paths.shape, dtype=h5py.string_dtype())
            paths_dset[:] = image_paths
        
    def save_dataset(self, canvases: List[LabelingCanvas], file_path: str):
        if self.skeleton is None: 
            showwarning("Скелет не был выбран", "Невозможно сохранить разметку, так как скелет не был выбран.")
            return
        # Названия точек
        label_names_data = np.array(list(self.skeleton.nodes), dtype=np.unicode_)
        
        # Составляем матрицу данных
        labels_data = []
        for canvas in canvases:
            row = []
            # Получаем координаты всех точек канваса
            coords = canvas.keypoint_manager.get_keypoints_coordinates()
            # Для каждой точки добавляем x и y
            for name in self.skeleton.nodes:
                row.append(int(round(coords[name][0])))
                row.append(int(round(coords[name][1])))
            labels_data.append(row)
        
        labels_data = np.array(labels_data, dtype=np.int32)

        # Составляем матрицу изображений
        images_data: np.ndarray = np.array([
            np.asarray(canvas.image.pil_image) for canvas in canvases
        ], dtype=np.int32)
        
        try:
            with h5py.File(file_path, 'w') as f:
                skeleton_dset = f.create_dataset("skeleton", label_names_data.shape, dtype=h5py.string_dtype())
                skeleton_dset[:] = label_names_data

                images_dset = f.create_dataset("images", images_data.shape, dtype=np.int8)
                images_dset[:] = images_data
                
                labels_dset = f.create_dataset("labels", labels_data.shape)
                labels_dset[:] = labels_data
        except Exception as e:
            messagebox.showerror("Сохранение датасета", f"При сохранении датасета произошла ошибка: {e}.")
        else:
            messagebox.showinfo("Сохранение разметки", "Сохранение успешно завершено.")
