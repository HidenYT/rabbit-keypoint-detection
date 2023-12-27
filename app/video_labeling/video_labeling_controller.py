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
        try:
            df = pd.read_csv(file)
            self.skeleton = Skeleton(df)
            return self.skeleton
        except KeyError as e:
            showwarning("Ошибка при загрузке скелета", f"Родительская точка {e} задана неверно.")
        except Exception as e:
            showwarning("Ошибка при загрузке скелета", f"Неизвестная ошибка: {e}.")
        return None

    def save_labels(self, canvases: List[LabelingCanvas], file):
        if self.skeleton is not None:
            label_names = list(self.skeleton.nodes)
            result_label_names = ["Image path"]
            for name in label_names:
                result_label_names.append(f"{name}_x")
                result_label_names.append(f"{name}_y")
            
            data = []
            for canvas in canvases:
                row = []
                coords = canvas.keypoint_manager.get_keypoints_coordinates()
                for name in label_names:
                    row.append(int(round(coords[name][0])))
                    row.append(int(round(coords[name][1])))
                data.append(row)
            
            for i, row in enumerate(data):
                row.insert(0, canvases[i].image.image_path)
            df = pd.DataFrame(data=data, columns=result_label_names)
            df.to_csv(file, index=False, encoding="utf-16")