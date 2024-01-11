from typing import Iterable, Set, Tuple
from numpy import ndarray
from .duplicates_finder import DuplicatesFinder


class DBSCANDuplicatesFinder(DuplicatesFinder):
    def find_labels_and_scores(self, images: Iterable[Tuple[int, ndarray]]) -> Iterable[Set[int]]:
        pass