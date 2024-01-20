from typing import Iterable, Set, Tuple, List
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from .duplicates_finder import DuplicatesFinder


class DBSCANDuplicatesFinder(DuplicatesFinder):
    def find_labels_and_scores(self, images: List[Tuple[int, np.ndarray]]) -> Tuple[List[np.ndarray], List[float]]:
        images_no_idx = np.array([img[1].flatten() for img in images])
        dbscan = DBSCAN(eps=10000, min_samples=2)
        labels = dbscan.fit_predict(images_no_idx)
        neg_label = -1
        for i in range(len(labels)):
            if labels[i] == -1:
                labels[i] = neg_label
                neg_label -= 1
        return [labels], [1]