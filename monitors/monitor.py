from utils.util import timeit

class Monitor:

    def __init__(self, name, confidence):
        self.name = name
        self.confidence = confidence

    def next_step(self, next_observation):
        return {}

    def setup(self, *args, **kwargs):
        pass

    def run_on(self, input_array):
        return [self.next_step(s) for s in input_array]

    def to_dict(self):
        return {"name": self.name, "confidence": self.confidence}


