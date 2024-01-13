import pandas as pd
from .label_saver import ImagePathSaverMixin


class JSONLabelSaver(ImagePathSaverMixin):
    def save(self):
        df = pd.DataFrame(self.labels_data, columns=self.csv_column_names)
        df.to_json(self._file, force_ascii=False, orient='records')