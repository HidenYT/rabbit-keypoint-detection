import tkinter as tk
from tkinter import Menu, filedialog, messagebox
from typing import Callable, List, Tuple, TYPE_CHECKING
from core.widgets.scrollable_frame import VerticalScrolledFrame
import pandas as pd
from core.mvc.view import View
from tkinter import ttk
from core.filetypes import csv_ft

if TYPE_CHECKING:
    from .skeleton_controller import SkeletonController

class SkeletonEditWindow(View["SkeletonController"]):
    def __init__(self, controller: "SkeletonController") -> None:
        super().__init__(controller)
        self.focus_row = None
        self.setup_content_frame()

    def create_menu(self) -> Menu:
        main_menu = tk.Menu(self.controller.root)
        return main_menu
    
    def setup_content_frame(self):
        self.entries_table: List[Tuple[tk.Entry, tk.Entry]] = []
        self.frm_table = VerticalScrolledFrame(self)
        self.create_empty_table()
        
        frm_bottom_panel = tk.Frame(self)
        frm_bottom_panel.pack(side=tk.BOTTOM, fill="x")
        for i in range(2): frm_bottom_panel.grid_columnconfigure(i, weight=1, uniform="uniform")

        frm_control_buttons = self.create_table_control_buttons_frame(frm_bottom_panel)
        frm_file_buttons = self.create_file_buttons_frame(frm_bottom_panel)
        
        frm_file_buttons.grid(row=0, column=0, sticky="news")
        frm_control_buttons.grid(row=0, column=1, sticky="news")
        #frm_control_buttons.grid(fill="x", side="bottom")
    
    def create_table_control_buttons_frame(self, bottom_panel: tk.Frame):
        frm_bottom_panel = tk.Frame(bottom_panel)
        #for i in range(2): frm_bottom_panel.grid_columnconfigure(i, weight=1)
        
        btn_del = ttk.Button(frm_bottom_panel, 
                             text="Удалить строку", 
                             command=self.remove_entries_row,
                             style="default.TButton",
                             takefocus=False)
        #btn_del.grid(row=0, column=0, sticky="nsew")

        btn_add = ttk.Button(frm_bottom_panel, 
                             text="Добавить строку", 
                             command=self.add_row,
                             style="default.TButton",
                             takefocus=False)
        #btn_add.grid(row=0, column=1, sticky="nsew")
        btn_add.pack(fill='both', expand=True)
        btn_del.pack(fill='both', expand=True)
        return frm_bottom_panel
    
    def create_file_buttons_frame(self, bottom_panel: tk.Frame):
        frm_file_buttons_frame = tk.Frame(bottom_panel)
        for i in range(3): frm_file_buttons_frame.grid_columnconfigure(i, weight=1, uniform='uniform')

        btn_new = ttk.Button(
            frm_file_buttons_frame,
            text="Новый файл",
            command=self.create_new_file,
            style="default.TButton",
            takefocus=False
        )
        btn_open = ttk.Button(
            frm_file_buttons_frame,
            text="Открыть",
            command=self.open_file,
            style="default.TButton",
            takefocus=False
        )
        btn_save = ttk.Button(
            frm_file_buttons_frame,
            text="Сохранить как",
            command=self.save_as_csv,
            style="default.TButton",
            takefocus=False
        )
        #btn_new.grid(row=0, column=0, sticky="news")
        #btn_open.grid(row=0, column=1, sticky="news")
        #btn_save.grid(row=0, column=2, sticky="news")
        btn_new.pack(fill="x")
        btn_open.pack(fill="x")
        btn_save.pack(fill="x")
        return frm_file_buttons_frame
    
    def create_new_file(self):
        create = messagebox.askokcancel(
            "Создать новый файл?", 
            "Все несохранённые изменения будут утеряны."
        )
        if create:
            self.create_empty_table()
    
    def open_file(self):
        f = filedialog.askopenfile(filetypes=[csv_ft])
        if f is not None:
            self.create_table_from_csv(f)

    def add_row(self, value_left: str | None = None, value_right: str | None = None):
        e1, e2 = self.create_entries_row(value_left, value_right)
        e1.grid(row=self.grid_rows_num+1, column=0, sticky="nsew")
        e2.grid(row=self.grid_rows_num+1, column=1, sticky="nsew")
        self.grid_rows_num += 1
        self.entries_table.append((e1, e2))
    
    def create_entries_row(self, 
                           value_left: str | None = None, 
                           value_right: str | None = None) -> Tuple[tk.Entry, tk.Entry]:

        def handle_in(event):
            e_left.configure(style="selected_skeleton_table_cell.TEntry")
            e_right.configure(style="selected_skeleton_table_cell.TEntry")
        def handle_out(event):
            e_left.configure(style="skeleton_table_cell.TEntry")
            e_right.configure(style="skeleton_table_cell.TEntry")

        e_left = self.create_cell(value_left, handle_in, handle_out)
        e_right = self.create_cell(value_right, handle_in, handle_out)
        
        return e_left, e_right
    
    def create_cell(self, 
                    text: str | None, 
                    handle_in: Callable[[tk.Event], None], 
                    handle_out: Callable[[tk.Event], None]):
        from core.styles import skeleton_table_cell_font
        e = ttk.Entry(self.frm_table.interior,
                    style="skeleton_table_cell.TEntry",
                    font=skeleton_table_cell_font)
        if text is not None: e.insert(0, text)
        e.bind("<FocusIn>", handle_in)
        e.bind("<FocusOut>", handle_out)
        return e
    
    def remove_entries_row(self):
        if len(self.entries_table) == 0: return
        selected_row = None
        for i in range(len(self.entries_table)):
            if self.focus_get() in self.entries_table[i]:
                selected_row = i
                break
        if selected_row is None: return
        e1, e2 = self.entries_table[selected_row]
        e1.pack_forget()
        e1.destroy()
        e2.pack_forget()
        e2.destroy()
        self.entries_table.pop(selected_row)
    
    def create_table_from_csv(self, f):
        self.create_empty_table()
        df = self.controller.read_csv(f)
        for i in range(len(df)):
            e1 = str(df.iloc[i, 0]) if pd.notna(df.iloc[i, 0]) else ""
            e2 = str(df.iloc[i, 1]) if pd.notna(df.iloc[i, 1]) else ""
            self.add_row(e1, e2)
        
    def save_as_csv(self):
        f = filedialog.asksaveasfile(filetypes=[csv_ft], defaultextension="")
        if f is not None:
            self.controller.create_skeleton_csv(self.entries_table, f)
    
    def create_empty_table(self):
        self.grid_rows_num = 0
        self.frm_table.pack_forget()
        self.entries_table.clear()
        self.frm_table = frm_table = VerticalScrolledFrame(self)
        frm_table.interior.grid_columnconfigure(0, weight=1, uniform="uniform")
        frm_table.interior.grid_columnconfigure(1, weight=1, uniform="uniform")
        lbl_point_name = ttk.Label(frm_table.interior, text="Название точки",
                                   style="default.TLabel")
        lbl_point_name.grid(row=0, column=0)
        lbl_parent_name = ttk.Label(frm_table.interior, text="Родительская точка",
                                    style="default.TLabel")
        lbl_parent_name.grid(row=0, column=1)
        frm_table.pack(fill="both", expand=True)