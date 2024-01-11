from abc import ABC, abstractmethod
from typing import Dict, Iterable, List, Sequence, Set, Tuple

import numpy as np


class DuplicatesFinder(ABC):
    @abstractmethod
    def find_labels_and_scores(self, images: List[Tuple[int, np.ndarray]]) -> Tuple[List[np.ndarray], List[float]]: pass

    def find_duplicates(self, images: List[Tuple[int, np.ndarray]]) -> List[List[int]]:
        labels, scores = self.find_labels_and_scores(images)
        mx_score = max(scores)
        idx_mx = scores.index(mx_score)
        labels_dict: Dict[float, List[int]] = {}
        for i in range(len(images)):
            lbl = labels[idx_mx][i]
            labels_dict.setdefault(lbl, [])
            labels_dict[lbl].append(images[i][0])
        return list(labels_dict.values())