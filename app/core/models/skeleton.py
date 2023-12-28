import pandas as pd
from typing import Union, Dict, List, Tuple
from tkinter.messagebox import showwarning

class Skeleton:
    KEYPOINT_NAME_FIELD = "Keypoint name"
    PARENT_NAME_FIELD = "Parent name"

    def __init__(self, skeleton_df: pd.DataFrame) -> None:
        self.df = df = skeleton_df
        self.nodes: Dict[str, SkeletonNode] = {}
        # Создаём вершины без родителей
        if self.KEYPOINT_NAME_FIELD not in skeleton_df.columns:
            raise SkeletonCSVFieldError(f"Столбец {self.KEYPOINT_NAME_FIELD} не найден в csv файле.")
        if self.PARENT_NAME_FIELD not in skeleton_df.columns:
            raise SkeletonCSVFieldError(f"Столбец {self.PARENT_NAME_FIELD} не найден в csv файле.")
        for i in range(len(df)):
            node_name = str(df.loc[i, self.KEYPOINT_NAME_FIELD])
            node = SkeletonNode(node_name, None)
            self.nodes[node_name] = node
        # Добавляем вершинам родителей
        for i in range(len(df)):
            node_name = str(df.loc[i, self.KEYPOINT_NAME_FIELD])
            parent = df.loc[i, self.PARENT_NAME_FIELD]
            parent_name =  str(parent) if pd.notna(parent) else None 
            if parent_name is not None:
                self.nodes[node_name].parent = self.nodes[parent_name]

    @staticmethod
    def create_skeleton_csv(data: List[Tuple[str, str]], file):
        df = pd.DataFrame(data=data, columns=[Skeleton.KEYPOINT_NAME_FIELD, Skeleton.PARENT_NAME_FIELD])
        df.to_csv(file, index=False)

    @staticmethod
    def read_skeleton_from_csv(file) -> Union["Skeleton", None]:
        try:
            df = pd.read_csv(file)
            return Skeleton(df)
        except SkeletonCSVFieldError as e:
            showwarning("Ошибка при загрузке скелета", str(e))
        except KeyError as e:
            showwarning("Ошибка при загрузке скелета", f"Родительская точка {e} задана неверно.")
        except Exception as e:
            showwarning("Ошибка при загрузке скелета", f"Неизвестная ошибка: {e}.")
        return None

class SkeletonCSVFieldError(Exception): pass

class SkeletonNode:
    def __init__(self, name: str, parent: Union["SkeletonNode", None]) -> None:
        self.name = name
        self.parent = parent