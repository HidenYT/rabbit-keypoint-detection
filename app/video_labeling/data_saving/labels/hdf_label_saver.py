import h5py
import numpy as np
from ..label_saver import LabelSaver


class HDFLabelSaver(LabelSaver):
    def save(self):
        # Перевод данных в np.ndarray
        label_names_arr = np.array(self.label_names)
        labels_data_arr = np.array(self.labels_data, dtype=np.int32)
        image_paths_arr = np.array([
            canvas.image.image_path for canvas in self._canvases
        ])
        column_names_arr = np.array(self.column_names)
        with h5py.File(self._file, 'w') as f:
            skeleton_dset = f.create_dataset("skeleton", label_names_arr.shape, dtype=h5py.string_dtype())
            skeleton_dset[:] = label_names_arr
            
            column_names_dset = f.create_dataset("column_names", column_names_arr.shape, dtype=h5py.string_dtype())
            column_names_dset[:] = column_names_arr
        
            labels_dset = f.create_dataset("labels", labels_data_arr.shape)
            labels_dset[:] = labels_data_arr

            paths_dset = f.create_dataset("image_paths", image_paths_arr.shape, dtype=h5py.string_dtype())
            paths_dset[:] = image_paths_arr