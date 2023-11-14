from specifications.specification import Specification
from generators.generator import Generator
from generators.partially_observed_markov_chain import PartiallyObservedMarkovChain


class Atom(Specification):

    def __init__(self, name, function):
        super().__init__(name)
        self.function = function

    def get_arity(self):
        return self.function.get_arity()

    def get_lower_bound(self):
        return self.function.lower_bound

    def get_upper_bound(self):
        return self.function.upper_bound

    def get_bounds(self):
        return self.get_lower_bound(), self.get_upper_bound()

    def evaluate(self, input_value):
        if isinstance(input_value, list):
            return self.__evaluate_array(input_value)
        elif isinstance(input_value, Generator):
            return self.__evaluate_generator(input_value)
        return None

    def __evaluate_array(self, input_array):
        # print(self.function(input_array))
        return self.function(input_array)

    def __evaluate_generator(self, input_generator):
        if isinstance(input_generator, PartiallyObservedMarkovChain):
            self.value = self.__evaluate_pomc(input_generator)
        return self.value

    def __evaluate_pomc(self, pomc):
        return pomc.expectation_observation_path(self.function, self.get_arity())

    def to_dict(self):
        try:
            return {"name": self.name, "arity": self.get_arity(), "function": self.function.to_dict(), "true_value":self.value}
        except AttributeError:
            return {"name": self.name, "arity": self.get_arity(), "function": {}, "true_value": self.value}
