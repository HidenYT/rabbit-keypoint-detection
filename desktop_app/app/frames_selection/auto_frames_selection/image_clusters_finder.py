from abc import ABC, abstractmethod
from typing import Dict, Iterable, List, Sequence, Set, Tuple
from PIL import Image

import numpy as np


class ImageClustersFinder(ABC):
    @abstractmethod
    def clusterize_data(self, n_clusters: int, images: List[np.ndarray]) -> np.ndarray | List[int]: pass

    def get_image_indicies(self, n_clusters: int, images: List[np.ndarray]) -> List[int]:
        for i in range(len(images)):
            images[i] = images[i].flatten()
        clusters = self.clusterize_data(n_clusters, images)
        used = set()
        image_indicies = []
        for i, cl in enumerate(clusters):
            if cl not in used:
                image_indicies.append(i)
                used.add(cl)
        return image_indicies