import tkinter as tk
from frames_selection.frames_selection_controller import FramesSelectionController
from core.main_app_interface import MainAppMixin
from skeleton_creation.skeleton_controller import SkeletonController
from video_labeling.video_labeling_controller import LabelingController
from core.widgets.navbar import Navbar

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.mvc.view import View

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except: pass

class MainApp(MainAppMixin):
    APP_TITLE = "Animal keypoint detector"

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        import core.styles
        self.geometry("600x400")
        self.state("zoomed")
        self.title(self.APP_TITLE)
        self.navbar = Navbar(self, self)
        self.navbar.pack(fill="x")
        self.free_space = tk.Frame(self)
        self.free_space.pack(fill="both", expand=True)
        self.frame = tk.Frame(self.free_space)
        self.current_controller = None
        #self.go_to_skeleton_creation()
    
    def go_to_frames_creation(self):
        self.show_view(FramesSelectionController(self).create_view())
        self.current_controller = FramesSelectionController

    def go_to_skeleton_creation(self):
        self.show_view(SkeletonController(self).create_view())
        self.current_controller = SkeletonController

    def go_to_frames_labeling(self):
        self.show_view(LabelingController(self).create_view())

    def show_view(self, view: "View"):
        self.frame.pack_forget()
        self.frame = view
        view.pack(fill="both", expand=True)