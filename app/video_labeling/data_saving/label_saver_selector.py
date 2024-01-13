import os
from typing import List
from core.filetypes import csv_ft, json_ft, hd5_ft
from .csv_label_saver import CSVLabelSaver
from .hdf_label_saver import HDFLabelSaver
from .json_label_saver import JSONLabelSaver
from .label_saver import LabelSaver
from core.models.skeleton import Skeleton
from video_labeling.labeling_canvas import LabelingCanvas


class LabelSaverSelector:
    def __init__(self, file_path: str) -> None:
        _, self.ext = os.path.splitext(file_path)
        self._file_path = file_path
    
    def select_saver(self, canvases: List[LabelingCanvas], skeleton: Skeleton) -> LabelSaver:
        if self.ext in csv_ft[1]:
            return CSVLabelSaver(canvases, skeleton, self._file_path)
        elif self.ext in json_ft[1]:
            return JSONLabelSaver(canvases, skeleton, self._file_path)
        elif self.ext in hd5_ft[1]:
            return HDFLabelSaver(canvases, skeleton, self._file_path)
        else:
            raise Exception(f"Wrong file extension to save labels: {self._file_path}.")