from itertools import groupby
from typing import Dict, Iterable, Sequence, Set, Tuple, List
import numpy as np
from .duplicates_finder import DuplicatesFinder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class KMeansDuplicatesFinder(DuplicatesFinder):
    def find_labels_and_scores(self, images: List[Tuple[int, np.ndarray]]) -> Tuple[List[np.ndarray], List[float]]:
        min_clusters_n = int(len(images)*0.9)
        scores = []
        all_labels: List[np.ndarray] = []
        images_no_idx = np.array([img[1].flatten() for img in images])
        for n_clusters in range(min_clusters_n, len(images)):
            kmeans = KMeans(n_clusters)
            labels = kmeans.fit_predict(images_no_idx)
            all_labels.append(labels)
            score = silhouette_score(images_no_idx, labels)
            scores.append(score)
        return all_labels, scores
