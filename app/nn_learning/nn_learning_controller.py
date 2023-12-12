from core.page_controller import PageController

class LearningController(PageController):
    def process(self, config: dict):
        print(config)