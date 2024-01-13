from io import BytesIO
import py7zr
from typing import IO, List
from ..dataset_saver import DatasetSaver
from ..labels.csv_label_saver import CustomImagePathCSVLabelSaver
from core.models.skeleton import Skeleton
from video_labeling.labeling_canvas import LabelingCanvas

class SevenZipDSSaver(DatasetSaver):

    IMAGE_FILE_FORMAT = "JPEG"
    IMAGE_NAME_FORMAT = "img{}.jpg"

    def __init__(self, canvases: List[LabelingCanvas], skeleton: Skeleton, file: str | IO[bytes]) -> None:
        super().__init__(canvases, skeleton, file)
        self._csv_labels_buffer = BytesIO()
        img_names: List[str] = [self.IMAGE_NAME_FORMAT.format(i) for i in range(len(canvases))]
        self._csv_saver = CustomImagePathCSVLabelSaver(canvases, 
                                                       skeleton, 
                                                       self._csv_labels_buffer,
                                                       img_names)

    def save(self):
        self._csv_saver.save()
        with py7zr.SevenZipFile(self._file, "w") as f:
            self._csv_labels_buffer.seek(0)
            f.writef(self._csv_labels_buffer, "labels.csv")
            for i, canvas in enumerate(self._canvases):
                img = canvas.image.pil_image
                img_bytes = BytesIO()
                img.save(img_bytes, format=self.IMAGE_FILE_FORMAT)
                img_bytes.seek(0)
                f.writef(img_bytes, self.IMAGE_NAME_FORMAT.format(i))