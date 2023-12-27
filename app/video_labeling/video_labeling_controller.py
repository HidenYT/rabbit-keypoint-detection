from core.main_app_interface import MainAppMixin
from core.view import View
from core.controller import ControllerNavigator
from .video_labeling_view import LabelingView
import pandas as pd
from core.skeleton import Skeleton
from tkinter.messagebox import showwarning
from typing import List
from .labeling_canvas import LabelingCanvas

class LabelingController(ControllerNavigator):
    def __init__(self, root: MainAppMixin) -> None:
        super().__init__(root)
        self.skeleton: Skeleton | None = None

    def create_view(self) -> View:
        return LabelingView(self)
    
    def open_skeleton(self, file) -> Skeleton:
        self.skeleton = Skeleton.read_skeleton_from_csv(file)
        return self.skeleton

    def save_labels(self, canvases: List[LabelingCanvas], file):
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
            
        df = pd.DataFrame(data=data, columns=result_label_names)
        df.to_csv(file, index=False, encoding="utf-16")