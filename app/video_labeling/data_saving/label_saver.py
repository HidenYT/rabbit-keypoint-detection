from typing import IO, List
from .base_saver import BaseLabelDataSaver
from core.models.skeleton import Skeleton
from video_labeling.labeling_canvas import LabelingCanvas


class LabelSaver(BaseLabelDataSaver):

    IMAGE_PATH_COL = "Image path"
    COLUMN_NAME_X_FORMAT = "{}_x"
    COLUMN_NAME_Y_FORMAT = "{}_y"

    def __init__(self, canvases: List[LabelingCanvas], skeleton: Skeleton, file: str | IO[bytes] | IO[str]):
        super().__init__(canvases, skeleton, file)
        # Названия меток
        self.label_names = list(skeleton.nodes)
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
                row.append(str(int(round(coords[name][0]))))
                row.append(str(int(round(coords[name][1]))))
            self.labels_data.append(row)

class ImagePathSaverMixin(LabelSaver):
    def __init__(self, canvases: List[LabelingCanvas], skeleton: Skeleton, file: str | IO[bytes] | IO[str]):
        super().__init__(canvases, skeleton, file)
        for i, canvas in enumerate(self._canvases):
            self.labels_data[i].insert(0, canvas.image.image_path)