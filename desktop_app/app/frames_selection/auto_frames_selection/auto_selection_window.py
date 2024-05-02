import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from frames_selection.frames_selection_manager import FramesSelectionManager
from .auto_selector import (
    SELECTION_KMEANS,
    AutoSelector, 
    SELECTION_RANDOM, 
    SELECTION_UNIFORM,
)
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from .auto_selector import FramesSource


class AutoFrameSelectionWindow(tk.Toplevel):

    def __init__(self, master, total_frames: int, frame_src: "FramesSource", frame_selection_manager: FramesSelectionManager):
        super().__init__(master, padx=10, pady=10)
        self.resizable(False, False)
        self.total_frames = total_frames
        self.frame_src = frame_src
        self.frame_selection_manager = frame_selection_manager
        self.title("Автоматическая выборка кадров")

        self.setup_frames_n_entry()

        self.setup_selection_method()

        btn_start = ttk.Button(self, text="Начать", command=self.start_auto_selection)
        btn_start.pack()

        self.setup_selected_frames()

    def setup_frames_n_entry(self):
        lbl_frames_n = ttk.Label(self, text="Количество кадров")
        lbl_frames_n.pack()
        self.entr_frames_n = ttk.Entry(self)
        self.entr_frames_n.pack()
    
    def setup_selection_method(self):
        frm = ttk.Frame(self)
        lbl_sel_method = ttk.Label(frm, text="Способ выборки кадров")
        lbl_sel_method.pack()
        self.selection_method_var = var = tk.StringVar(value=SELECTION_RANDOM)
        sel_method_random = ttk.Radiobutton(frm, 
                                            variable=var, 
                                            value=SELECTION_RANDOM,
                                            text="Случайная выборка")
        sel_method_uniform = ttk.Radiobutton(frm, 
                                             variable=var, 
                                             value=SELECTION_UNIFORM,
                                             text="Равномерная выборка")
        sel_method_kmeans = ttk.Radiobutton(frm, 
                                             variable=var, 
                                             value=SELECTION_KMEANS,
                                             text="K-Means")

        sel_method_random.pack(side='left', fill='x')
        sel_method_uniform.pack(side='left', fill='x')
        sel_method_kmeans.pack(side='left', fill='x')
        frm.pack()
    
    def start_auto_selection(self):
        if not self.entr_frames_n.get(): 
            messagebox.showwarning("Выборка кадров", "Введите число кадров.", parent=self)
            return
        auto_selector = AutoSelector(self.total_frames,
                                     int(self.entr_frames_n.get()),
                                     self.selection_method_var.get(),
                                     self.frame_src)
        auto_selector.select_frames()
        messagebox.showinfo("Выборка кадров", "Автоматическая выборка кадров успешно завершена.", parent=self)
        self.selected_frames = selected_frames = sorted(auto_selector.frames_nums)
        if self.frm_selected_frames is not None: self.frm_selected_frames.destroy()
        self.setup_selected_frames(selected_frames)
        self.btn_unite_selection.config(state='normal')
        self.btn_replace_selection.config(state='normal')

    
    def setup_selected_frames(self, selected_frames: List[int] = []):
        # TODO Сделать ограничение длины строки выбранных кадров, иначе может получиться очень длинное окно
        self.frm_selected_frames = frm = ttk.Frame(self)
        selected_frames_str = ""
        for i in range(len(selected_frames)):
            selected_frames_str = selected_frames_str + f"{selected_frames[i]}, "
            if (i+1)%10 == 0: selected_frames_str = selected_frames_str + "\n"
        selected_frames_str = selected_frames_str or "<Пусто>"
        self.lbl_selected_frames = ttk.Label(frm, text=f"Выбранные кадры:\n{selected_frames_str}", anchor="n")
        self.lbl_selected_frames.pack()

        self.btn_unite_selection = ttk.Button(frm, text="Объединить с уже выбранными кадрами", state="disabled", command=self.unite_selection)
        self.btn_unite_selection.pack(side='left')
        
        self.btn_replace_selection = ttk.Button(frm, text="Заменить выбранные кадры", state="disabled", command=self.replace_selection)
        self.btn_replace_selection.pack(side='right')
        frm.pack()
    
    def unite_selection(self):
        for frm in self.selected_frames:
            self.frame_selection_manager.select(frm)

    def replace_selection(self):
        self.frame_selection_manager.clear()
        for frm in self.selected_frames:
            self.frame_selection_manager.select(frm)