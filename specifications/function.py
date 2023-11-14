
class Function:

    def __init__(self, arity, lower_bound, upper_bound, *args, **kwargs):
        self.arity = arity
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __call__(self, *args, **kwargs):
        pass

    def get_arity(self):
        return self.arity

    def to_dict(self):
        return {"arity": self.arity, "lower_bound": self.lower_bound, "upper_bound": self.upper_bound }
