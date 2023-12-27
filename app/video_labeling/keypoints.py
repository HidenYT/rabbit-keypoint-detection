from core.skeleton import SkeletonNode, Skeleton
from typing import Dict, TYPE_CHECKING, List, Set

if TYPE_CHECKING:
    from .labeling_canvas import LabelingCanvas

class KeypointManager:
    def __init__(self, canvas: "LabelingCanvas", skeleton: Skeleton | None = None) -> None:
        self.canvas = canvas
        self.skeleton = skeleton
        self.keypoint_by_id: Dict[int, Keypoint] = {}
        self.keypoint_by_name: Dict[str, Keypoint] = {}
        self.kp_name_by_id: Dict[int, str] = {}
        self.kp_id_by_name: Dict[str, int] = {}
        self.kp_text_by_kp_id: Dict[int, int] = {}
    
    def get_keypoints_coordinates(self) -> Dict[str, tuple[float, float]]:
        result = {}
        for key in self.keypoint_by_name:
            result[key] = self.get_keypoint_coordinates(self.keypoint_by_name[key])
        return result

    def get_keypoint_coordinates(self, kp: "Keypoint"):
        cont_x, cont_y = self.canvas.get_containter_top_left()
        return ((kp.x-cont_x)/self.canvas.imscale, (kp.y-cont_y)/self.canvas.imscale)

    def add_keypoint(self, kp_id: int, kp_name: str):
        node = self.skeleton.nodes[kp_name]
        kp = Keypoint(self.canvas, kp_id, node)
        self.keypoint_by_id[kp_id] = kp
        self.keypoint_by_name[kp_name] = kp
        self.kp_name_by_id[kp_id] = kp_name
        self.kp_id_by_name[kp_name] = kp_id
    
    def add_kp_text(self, kp: int | str, text_id: int):
        if isinstance(kp, str):
            id = self.kp_id_by_name[kp]
            self.kp_text_by_kp_id[id] = text_id
        elif isinstance(kp, int):
            self.kp_text_by_kp_id[kp] = text_id
        else:
            raise TypeError("kp can be only int or str.")
    
    def get_kp_by_name(self, name: str) -> "Keypoint":
        return self.keypoint_by_name[name]
    
    def get_kp_by_id(self, id: int) -> "Keypoint":
        return self.keypoint_by_id[id]
    
    def get_name_by_id(self, id: int) -> str:
        return self.kp_name_by_id[id]
    
    def get_id_by_name(self, name: str) -> int:
        return self.kp_id_by_name[name]
    
    def get_text_id_by_kp_id(self, id: int) -> int:
        return self.kp_text_by_kp_id[id]
    
    def remove_kp(self, id_or_name: str | int):
        if isinstance(id_or_name, int):
            id = id_or_name
            name = self.get_name_by_id(id)
        elif isinstance(id_or_name, str):
            name = id_or_name
            id = self.get_id_by_name(name)
        else:
            raise TypeError("id_or_name should be either int or str.")
        del self.keypoint_by_id[id]
        del self.keypoint_by_name[name]
        del self.kp_name_by_id[id]
        del self.kp_id_by_name[name]
    
    def set_skeleton(self, skeleton: Skeleton):
        self.skeleton = skeleton
        self.keypoint_by_id: Dict[int, Keypoint] = {}
        self.keypoint_by_name: Dict[str, Keypoint] = {}
        self.kp_name_by_id: Dict[int, str] = {}
        self.kp_id_by_name: Dict[str, int] = {}
        self.kp_text_by_kp_id: Dict[int, int] = {}
    
    def get_kp_ids(self) -> Set[int]:
        return self.keypoint_by_id.keys()
    
    def get_text_ids(self) -> Set[int]:
        return set(self.kp_text_by_kp_id.values())
    
    def clear(self):
        self.keypoint_by_id: Dict[int, Keypoint] = {}
        self.keypoint_by_name: Dict[str, Keypoint] = {}
        self.kp_name_by_id: Dict[int, str] = {}
        self.kp_id_by_name: Dict[str, int] = {}
        self.kp_text_by_kp_id: Dict[int, int] = {}

class Keypoint:
    def __init__(self, canvas: "LabelingCanvas", id: int, skeleton_node: SkeletonNode):
        self.canvas = canvas
        self.id = id
        self.skeleton_node = skeleton_node
    
    @staticmethod
    def get_coordinates_from_bbox(bbox: tuple[int, int, int, int]) -> tuple[float, float]:
        x1, y1, x2, y2 = bbox
        return (x1+x2)/2, (y1+y2)/2 

    @property
    def coordinates(self):
        return self.x, self.y
    
    @property
    def bbox(self):
        return self.canvas.bbox(self.id)

    @property
    def x(self):
        return (self.bbox[0]+self.bbox[2])/2
    
    @property
    def y(self):
        return (self.bbox[1]+self.bbox[3])/2