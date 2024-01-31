from typing import IO, List
from .base_saver import BaseLabelDataSaver
from core.models.skeleton import Skeleton
from video_labeling.labeling_canvas import LabelingCanvas
import pandas as pd


class LabelSaver(BaseLabelDataSaver):

    IMAGE_PATH_COL = "Image path"
    COLUMN_NAME_X_FORMAT = "{}_x"
    COLUMN_NAME_Y_FORMAT = "{}_y"

    def __init__(self, canvases: List[LabelingCanvas], skeleton: Skeleton, file: str | IO[bytes] | IO[str]):
        super().__init__(canvases, skeleton, file)
        # Названия меток
        self.label_names = list(skeleton.nodes)
        # Названия столбцов с multiindex
        self.label_names_multiindex = pd.MultiIndex.from_product(
            [self.label_names, ["X", "Y"]], 
            names=["Keypoint", "Axis"]
        )
        # Названия столбцов с multiindex со столбцов пути файла
        self.label_names_multiindex_with_img_path = pd.MultiIndex.from_product(
            [[self.IMAGE_PATH_COL], [""]]
        ).append(self.label_names_multiindex)
        # Названия столбцов
        self.column_names: List[str] = []
        for name in self.label_names:
            self.column_names.append(self.COLUMN_NAME_X_FORMAT.format(name))
            self.column_names.append(self.COLUMN_NAME_Y_FORMAT.format(name))
        # Названия столбцов для csv
        self.csv_column_names = [self.IMAGE_PATH_COL] + self.column_names
        # Разметка
        self.labels_data: List[List[str]] = []
        for canvas in canvases:
            row: List[str] = []
            coords = canvas.keypoint_manager.get_keypoints_coordinates()
            for name in self.label_names:
                if canvas.keypoint_manager.get_kp_by_name(name).visible:
                    row.append(str(coords[name][0]))
                    row.append(str(coords[name][1]))
                else:
                    row.append('')
                    row.append('')
            self.labels_data.append(row)

class ImagePathSaverMixin(LabelSaver):
    def __init__(self, canvases: List[LabelingCanvas], skeleton: Skeleton, file: str | IO[bytes] | IO[str]):
        super().__init__(canvases, skeleton, file)
        for i, canvas in enumerate(self._canvases):
            self.labels_data[i].insert(0, canvas.image.image_path)