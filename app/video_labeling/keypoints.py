from core.models.skeleton import SkeletonNode, Skeleton
from typing import Dict, TYPE_CHECKING, List, Set, Tuple

if TYPE_CHECKING:
    from .labeling_canvas import LabelingCanvas

class KeypointManager:
    '''Эффетивно управляет множеством точек скелета и связанных с ними объектов. Хранит координаты каждой точки, id её объекта на Canvas, соответствующее имя в скелете, id объекта надписи точки на Canvas.'''
    
    def __init__(self, canvas: "LabelingCanvas", skeleton: Skeleton | None = None) -> None:
        self.canvas = canvas
        self.skeleton = skeleton
        self.keypoint_by_id: Dict[int, Keypoint] = {}
        self.keypoint_by_name: Dict[str, Keypoint] = {}
        self.kp_name_by_id: Dict[int, str] = {}
        self.kp_id_by_name: Dict[str, int] = {}
        self.kp_text_by_kp_id: Dict[int, int] = {}
    
    def get_keypoints_coordinates(self) -> Dict[str, tuple[float, float]]:
        '''Возвращает координаты всех точек в словаре {название_точки: (xi, yi)}'''
        result = {}
        for key in self.keypoint_by_name:
            result[key] = self.get_keypoint_coordinates(self.keypoint_by_name[key])
        return result

    def get_keypoint_coordinates(self, kp: "Keypoint") -> Tuple[float, float]:
        '''Возвращает координаты точки в виде пары xi, yi'''
        cont_x, cont_y = self.canvas.get_containter_top_left()
        return ((kp.x-cont_x)/self.canvas.imscale, (kp.y-cont_y)/self.canvas.imscale)

    def add_keypoint(self, kp_id: int, kp_name: str):
        '''Добавляет точку в менеджер по id на Canvas и названию'''
        if self.skeleton is None: raise Exception("Trying to add keypoint to the KeypointManager, but skeleton was not provided.")
        node = self.skeleton.nodes[kp_name]
        kp = Keypoint(self.canvas, kp_id, node)
        self.keypoint_by_id[kp_id] = kp
        self.keypoint_by_name[kp_name] = kp
        self.kp_name_by_id[kp_id] = kp_name
        self.kp_id_by_name[kp_name] = kp_id
    
    def add_kp_text(self, kp: int | str, text_id: int):
        '''Добавляет напись, соответствующую точке.
        
        - `kp` - id на Canvas или название точки;
        
        - `text_id` - id надписи на Canvas'''
        if isinstance(kp, str):
            id = self.kp_id_by_name[kp]
            self.kp_text_by_kp_id[id] = text_id
        elif isinstance(kp, int):
            self.kp_text_by_kp_id[kp] = text_id
        else:
            raise TypeError("kp can be only int or str.")
    
    def get_kp_by_name(self, name: str) -> "Keypoint":
        '''Возвращает объект `Keypoint` по названию точки.'''
        return self.keypoint_by_name[name]
    
    def get_kp_by_id(self, id: int) -> "Keypoint":
        '''Возвращает объект `Keypoint` по id точки на Canvas.'''
        return self.keypoint_by_id[id]
    
    def get_name_by_id(self, id: int) -> str:
        '''Возвращает название точки по id точки на Canvas.'''
        return self.kp_name_by_id[id]
    
    def get_id_by_name(self, name: str) -> int:
        '''Возвращает id точки по названию точки.'''
        return self.kp_id_by_name[name]
    
    def get_text_id_by_kp_id(self, id: int) -> int:
        '''Возвращает id надписи по id точки на Canvas.'''
        return self.kp_text_by_kp_id[id]
    
    def remove_kp(self, id_or_name: str | int):
        '''Удаляет точку из менеджера точек.
        
        - `id_or_name` - id точки на Canvas или название точки.'''
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
        '''Устанавливает скелет, используемый при работе с точками.'''
        self.skeleton = skeleton
        self.keypoint_by_id: Dict[int, Keypoint] = {}
        self.keypoint_by_name: Dict[str, Keypoint] = {}
        self.kp_name_by_id: Dict[int, str] = {}
        self.kp_id_by_name: Dict[str, int] = {}
        self.kp_text_by_kp_id: Dict[int, int] = {}
    
    def get_kp_ids(self):
        '''Возвращает `dict_keys`, содержащий id всех точек менеджера.'''
        return self.keypoint_by_id.keys()
    
    def get_text_ids(self) -> Set[int]:
        '''Возвращает `set`, содержащий id всех надписей.'''
        return set(self.kp_text_by_kp_id.values())
    
    def clear(self):
        '''Удаляет все точки и тексты из менеджера.'''
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

    @property
    def coordinates(self):
        return self.canvas.coords(self.id)

    @property
    def x(self):
        return self.coordinates[0]
    
    @property
    def y(self):
        return self.coordinates[1]