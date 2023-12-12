from core.page_controller import PageController

class InferenceController(PageController):
    def process(self, config: dict):
        print(config)
        