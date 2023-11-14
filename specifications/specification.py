
class Specification:

    def __init__(self, name):
        self.name = name
        self.value = None
        self.arity = 0

    def evaluate(self, *args, **kwargs):
        pass

    def set_value(self, value):
        self.value = value

    def to_dict(self):
        return {}