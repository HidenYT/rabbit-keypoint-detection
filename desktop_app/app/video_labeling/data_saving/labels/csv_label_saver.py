from typing import IO, Iterable, List
import pandas as pd

from core.models.skeleton import Skeleton
from video_labeling.labeling_canvas import LabelingCanvas
from ..label_saver import ImagePathSaverMixin


class CSVLabelSaver(ImagePathSaverMixin):
    def save(self):
        df = pd.DataFrame(self.labels_data, columns=self.csv_column_names)
        df.to_csv(self._file, index=False, encoding="utf-16")

class CustomImagePathCSVLabelSaver(CSVLabelSaver):
    def __init__(self, 
                 canvases: List[LabelingCanvas], 
                 skeleton: Skeleton, 
                 file: str | IO,
                 image_paths: Iterable[str]):
        super().__init__(canvases, skeleton, file)
        for i, path in enumerate(image_paths):
            self.labels_data[i][0] = path