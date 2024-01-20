from io import BytesIO
import h5py
import numpy as np
from typing import IO, List
from ..label_saver import LabelSaver
from ..dataset_saver import DatasetSaver

class HDFDatasetSaver(DatasetSaver, LabelSaver):

    IMAGE_FILE_FORMAT = "JPEG"

    # TODO Вместо сохранения всех изображений было бы хорошо сделать сохранение
    # их сжатых в jpeg версий через байты. Пока что не получилось.
    # def save(self):
    #     # Перевод данных в np.ndarray
    #     label_names_arr = np.array(self.label_names)
    #     labels_data_arr = np.array(self.labels_data, dtype=np.int32)
    #     images_bytes: List[bytes] = []
    #     for canvas in self._canvases:
    #         img_bytes = BytesIO()
    #         canvas.image.pil_image.save(img_bytes, format=self.IMAGE_FILE_FORMAT)
    #         img_bytes.seek(0)
    #         images_bytes.append(img_bytes.read())
    #     images_bytes_arr = np.array(images_bytes, dtype="S").tobytes()
    #     column_names_arr = self.column_names
    #     #h5py._errors.unsilence_errors()
    #     # Сохранение
    #     with h5py.File(self._file, 'w') as f:
    #         skeleton_dset = f.create_dataset("skeleton", label_names_arr.shape, dtype=h5py.string_dtype())
    #         skeleton_dset[:] = label_names_arr
            
    #         column_names_dset = f.create_dataset("column_names", (len(column_names_arr), ), dtype=h5py.string_dtype())
    #         column_names_dset[:] = column_names_arr
        
    #         labels_dset = f.create_dataset("labels", labels_data_arr.shape)
    #         labels_dset[:] = labels_data_arr

    #         f.attrs["images_np_array"] = np.void(images_bytes_arr)
    #     print("here")
    
    def save(self):
        # Перевод данных в np.ndarray
        label_names_arr = np.array(self.label_names)
        labels_data_arr = np.array(self.labels_data, dtype=np.int32)
        images_arr = np.array([
            np.asarray(canvas.image.pil_image) 
            for canvas in self._canvases
        ], dtype=np.uint8)
        column_names_arr = self.column_names
        #h5py._errors.unsilence_errors()
        # Сохранение
        with h5py.File(self._file, 'w') as f:
            skeleton_dset = f.create_dataset("skeleton", label_names_arr.shape, dtype=h5py.string_dtype())
            skeleton_dset[:] = label_names_arr
            
            column_names_dset = f.create_dataset("column_names", (len(column_names_arr), ), dtype=h5py.string_dtype())
            column_names_dset[:] = column_names_arr
        
            labels_dset = f.create_dataset("labels", labels_data_arr.shape)
            labels_dset[:] = labels_data_arr

            images_dset = f.create_dataset("images", images_arr.shape, dtype=np.uint8)
            images_dset[:] = images_arr