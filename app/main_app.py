import tkinter as tk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except: pass
from nn_inference.nn_inference_controller import InferenceController
from video_labeling.video_labeling_controller import LabelingController
from nn_learning.nn_learning_controller import LearningController

class MainApp(tk.Tk):
    APP_TITLE = "Animal keypoint detector"

    def initial_state(self):
        self.configure(menu=self.menu)
        self.title(self.APP_TITLE)
        self.frame.pack()

    def run_nn_inference_window(self):
        self.frame.pack_forget()
        cntr = InferenceController(self)
        cntr.show_view()

    def run_labeling_window(self):
        self.frame.pack_forget()
        cntr = LabelingController(self)
        cntr.show_view()

    def run_learning_window(self):
        self.frame.pack_forget()
        cntr = LearningController(self)
        cntr.show_view()

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry("600x400")
        self.menu = self.get_menu()
        self.frame = self.get_frame()
        self.frame.pack()
        self.initial_state()

    def get_menu(self) -> tk.Menu:
        return tk.Menu(self)
    
    def get_frame(self) -> tk.Frame:
        frame = tk.Frame(self)

        btn_labeling = tk.Button(frame, text="Разметить видео", command=self.run_labeling_window)
        btn_labeling.pack()
        btn_learning = tk.Button(frame, text="Обучить нейросеть", command=self.run_learning_window)
        btn_learning.pack()
        btn_inference = tk.Button(frame, text="Запустить обученную нейросеть", command=self.run_nn_inference_window)
        btn_inference.pack()

        return frame