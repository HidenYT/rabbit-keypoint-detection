from core.page_controller import PageController
from .skeleton.skeleton_window_view import SkeletonEditWindow
from .skeleton.skeleton_controller import SkeletonController

class LabelingController(PageController):
    
    def save_labels(self, data: dict):
        print(data)

    def run_create_skeleton(self):
        skel_controller = SkeletonController()
        root = SkeletonEditWindow(skel_controller)
        root.mainloop()