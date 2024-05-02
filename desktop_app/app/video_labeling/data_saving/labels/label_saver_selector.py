import os
from typing import List
from core.filetypes import csv_ft
from .csv_label_saver import CSVLabelSaver
from ..label_saver import LabelSaver
from ..saver_selector import SaverSelector
from core.models.skeleton import Skeleton
from video_labeling.labeling_canvas import LabelingCanvas


class LabelSaverSelector(SaverSelector):
    
    def select_saver(self, canvases: List[LabelingCanvas], skeleton: Skeleton) -> LabelSaver:
        if self.ext in csv_ft[1]:
            return CSVLabelSaver(canvases, skeleton, self._file_path)
        else:
            raise Exception(f"Wrong file extension to save labels: {self._file_path}.")