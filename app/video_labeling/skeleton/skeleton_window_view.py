import tkinter as tk
from tkinter import filedialog
from typing import List, Tuple
from core.scrollable_frame import VerticalScrolledFrame
import pandas as pd
from .skeleton_controller import SkeletonController

class SkeletonEditWindow(tk.Tk):
    def __init__(self, controller: SkeletonController) -> None:
        super().__init__()
        self.controller = controller
        self.geometry("600x500")
        self.title("Редактор скелета")
        self.entries_table: List[Tuple[tk.Entry, tk.Entry]] = []
        self.create_empty_table()
        
        btn_save = tk.Button(self, text="Сохранить", command=self.create_csv)
        btn_save.pack(fill="both", side="bottom")
        btn_del = tk.Button(self, text="Удалить", command=self.remove_entries_row)
        btn_del.pack(fill="both", side="bottom")
        btn_add = tk.Button(self, text="Добавить", command=self.add_row)
        btn_add.pack(fill="both", side="bottom")

        main_menu = tk.Menu(self)
        main_menu.add_command(label="Открыть", command=self.create_table_from_csv)
        self.configure(menu=main_menu)
    
    def add_row(self, value_left: str | None = None, value_right: str | None = None):
        e1, e2 = self.create_entries_row(value_left, value_right)
        e1.grid(row=len(self.entries_table)+1, column=0, sticky="nsew")
        e2.grid(row=len(self.entries_table)+1, column=1, sticky="nsew")
        self.entries_table.append((e1, e2))
    
    def create_entries_row(self, 
                           value_left: str | None = None, 
                           value_right: str | None = None) -> Tuple[tk.Entry, tk.Entry]:
        def handle_in(event):
            e_left.configure(background="#b9eaeb")
            e_right.configure(background="#b9eaeb")
        def handle_out(event):
            e_left.configure(background="white")
            e_right.configure(background="white")
        e_left = tk.Entry(self.frm_table.interior)
        if value_left is not None: e_left.insert(0, value_left)
        e_left.bind("<FocusIn>", handle_in)
        e_left.bind("<FocusOut>", handle_out)
        
        e_right = tk.Entry(self.frm_table.interior)
        if value_right is not None: e_right.insert(0, value_right)
        e_right.bind("<FocusIn>", handle_in)
        e_right.bind("<FocusOut>", handle_out)
        return e_left, e_right
    
    def remove_entries_row(self):
        if len(self.entries_table) == 0: return
        selected_row = None
        for i in range(len(self.entries_table)):
            if self.focus_get() in self.entries_table[i]:
                selected_row = i
                break
        if selected_row is None: return
        e1, e2 = self.entries_table[selected_row]
        e1.destroy()
        e2.destroy()
        self.entries_table.pop(selected_row)
    
    def create_table_from_csv(self):
        self.frm_table.pack_forget()
        self.create_empty_table()

        f = filedialog.askopenfile(defaultextension=".csv", filetypes=[("Comma separated values", [".csv"])])
        df = self.controller.read_csv(f)
        for i in range(len(df)):
            e1 = df.iloc[i, 0] if pd.notna(df.iloc[i, 0]) else ""
            e2 = df.iloc[i, 1] if pd.notna(df.iloc[i, 1]) else ""
            self.add_row(e1, e2)
        
    def create_csv(self):
        f = filedialog.asksaveasfile(defaultextension=".csv", filetypes=[("Comma separated values", [".csv"])])
        self.controller.create_skeleton_csv(self.entries_table, f)
    
    def create_empty_table(self):
        self.frm_table = frm_table = VerticalScrolledFrame(self)
        frm_table.interior.grid_columnconfigure(0, weight=1, uniform=True)
        frm_table.interior.grid_columnconfigure(1, weight=1, uniform=True)
        lbl_point_name = tk.Label(frm_table.interior, text="Название точки")
        lbl_point_name.grid(row=0, column=0)
        lbl_parent_name = tk.Label(frm_table.interior, text="Родительская точка")
        lbl_parent_name.grid(row=0, column=1)
        frm_table.pack(fill="both")