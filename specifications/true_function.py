from specifications.function import Function


class TrueFunction(Function):

    def __init__(self, function, arity, lower_bound, upper_bound, *args, **kwargs):
        super().__init__(arity, lower_bound, upper_bound, *args, **kwargs)
        self.function = function

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

