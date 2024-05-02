from typing import List
import numpy as np

from frames_selection.auto_frames_selection.interfaces import FramesSelector, FramesSource
from sklearn.cluster import MiniBatchKMeans


class KMeansFramesSelector(FramesSelector):
    
    IMAGE_MAX_DIMENSION = 32

    def select_frames(self, total_frames: int, sel_frames_n: int, frames_src: FramesSource) -> List[int]:
        small_frames = []
        for i in range(total_frames):
            frm = frames_src.get_frames_by_indicies([i])[0]
            w, h = frm.size
            if w > h:
                target_size = self.IMAGE_MAX_DIMENSION, h/w*self.IMAGE_MAX_DIMENSION
            else:
                target_size = w/h*self.IMAGE_MAX_DIMENSION, self.IMAGE_MAX_DIMENSION
            target_size = tuple(map(int, target_size))
            small_frames.append(np.array(frm.resize(target_size)).flatten())
        kmeans_clustering = MiniBatchKMeans(sel_frames_n)
        predictions = kmeans_clustering.fit_predict(small_frames)
        selected_clusters = set()
        selected_frames: list[int] = []
        for frame_i, prediction in enumerate(predictions):
            if prediction in selected_clusters: continue
            selected_clusters.add(prediction)
            selected_frames.append(frame_i)
        return selected_frames