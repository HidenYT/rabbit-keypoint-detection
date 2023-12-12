from typing import List, Tuple
import tkinter as tk
from tkinter import filedialog
import pandas as pd

class SkeletonController:
    def create_skeleton_csv(self, 
                            entries_table: List[Tuple[tk.Entry, tk.Entry]],
                            file) -> None:
        data = [(e1.get(), e2.get()) for e1, e2 in entries_table]
        df = pd.DataFrame(data=data, columns=["Keypoint name", "Parent name"])
        df.to_csv(file, index=False)
    
    def read_csv(self, file):
        if file is not None:
            return pd.read_csv(file)
        else:
            return pd.DataFrame()