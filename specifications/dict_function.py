from specifications.function import Function


class DictFunction(Function):

    def __init__(self, function_dict, lower_bound=None, upper_bound=None, *args, **kwargs):
        arity = len(list(function_dict.keys())[0])
        lower_bound = min(min(function_dict.values()), 0) if lower_bound is None else lower_bound
        upper_bound = max(function_dict.values()) if upper_bound is None else upper_bound
        super().__init__(arity, lower_bound, upper_bound, *args, **kwargs)
        self.function_dict = function_dict

    def __call__(self, input_array, *args, **kwargs):
        # if input_array[0] == "a":
        #     print(input_array, self.function_dict.get(tuple(input_array), 0))
        return self.function_dict.get(tuple(input_array), 0)

    def to_dict(self):
        return super().to_dict() | {"function_dict": {"".join(k): v for k, v in self.function_dict.items()}}
