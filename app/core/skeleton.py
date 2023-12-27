import pandas as pd
from typing import Union, Dict
from tkinter.messagebox import showwarning

class Skeleton:
    def __init__(self, skeleton_df: pd.DataFrame) -> None:
        self.df = df = skeleton_df
        self.nodes: Dict[str, SkeletonNode] = {}
        for i in range(len(df)):
            node_name = df.loc[i, "Keypoint name"]
            node = SkeletonNode(node_name, None)
            self.nodes[node_name] = node
        for i in range(len(df)):
            node_name = df.loc[i, "Keypoint name"]
            parent_name = df.loc[i, "Parent name"] if pd.notna(df.loc[i, "Parent name"]) else None 
            if parent_name is not None:
                try:
                    self.nodes[node_name].parent = self.nodes[parent_name]
                except KeyError as e:
                    showwarning("Ошибка при загрузке скелета", f"Родительская точка {e} задана неверно")

class SkeletonNode:
    def __init__(self, name: str, parent: Union["SkeletonNode", None]) -> None:
        self.name = name
        self.parent = parent