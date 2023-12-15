from abc import ABC, abstractmethod
from .main_app_interface import MainAppMixin
from .navbar import INavigator

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_app import MainApp
    from .view import View

class Controller(ABC):
    def __init__(self, root: "MainApp") -> None:
        self.root = root
    
    @abstractmethod
    def create_view(self) -> "View":
        pass

class ControllerNavigator(INavigator, Controller):
    def __init__(self, root: MainAppMixin) -> None:
        super().__init__(root)
        self.navigator = root
    
    def go_to_frames_creation(self):
        self.navigator.go_to_frames_creation()

    def go_to_skeleton_creation(self):
        self.navigator.go_to_skeleton_creation()
    
    def go_to_frames_labeling(self):
        self.navigator.go_to_frames_labeling()
    
    def go_to_nn_training(self):
        self.navigator.go_to_nn_training()
    
    def go_to_nn_inference(self):
        self.navigator.go_to_nn_inference()