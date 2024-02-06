from typing import List
from numpy import ndarray
from .image_clusters_finder import ImageClustersFinder
from sklearn.cluster import MiniBatchKMeans


class KMeansImageClustersFinder(ImageClustersFinder):
    def clusterize_data(self, n_clusters: int, images: List[ndarray]) -> ndarray | List[int]:
        model = MiniBatchKMeans(n_clusters=n_clusters)
        return model.fit_predict(images)