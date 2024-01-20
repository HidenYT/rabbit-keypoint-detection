from typing import List
from core.models.skeleton import Skeleton
from video_labeling.data_saving.datasets.hdf_dataset_saver import HDFDatasetSaver
from video_labeling.data_saving.datasets.seven_zip_dataset_saver import SevenZipDSSaver
from video_labeling.labeling_canvas import LabelingCanvas
from ..saver_selector import SaverSelector
from core.filetypes import hd5_ft, seven_z_ft

class DatasetSaverSelector(SaverSelector):
    def select_saver(self, canvases: List[LabelingCanvas], skeleton: Skeleton):
        if self.ext in seven_z_ft[1]:
            return SevenZipDSSaver(canvases, skeleton, self._file_path)
        elif self.ext in hd5_ft[1]:
            return HDFDatasetSaver(canvases, skeleton, self._file_path)
        else:
            raise Exception(f"Wrong file extension to save dataset: {self._file_path}.")