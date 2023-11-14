import ast
from utils.evaluator import eval_node
from utils.interval_evaluator import eval_node as interval_eval_node
from specifications.specification import Specification
from generators.generator import Generator
from generators.partially_observed_markov_chain import PartiallyObservedMarkovChain


class Expression(Specification):

    # Atom map, name in expression to atom class
    def __init__(self, name, expression, atoms, lower_bound=None, upper_bound=None):
        super().__init__(name)
        self.atoms = atoms
        self.expression = expression
        self.expression_tree = ast.parse(expression, "<string>", mode="eval")
        self.arity = max([a.get_arity() for a in self.atoms])
        comp_lower_bound, comp_upper_bound = self.__evaluate_atom_values({a.name: a.get_bounds() for a in self.atoms})
        self.lower_bound = comp_lower_bound if lower_bound is None else lower_bound
        self.upper_bound = comp_upper_bound if upper_bound is None else upper_bound
        self.value = None

    def get_atom_values(self):
        return {atom.name: atom.value for atom in self.atoms}

    def get_lower_bound(self):
        return self.lower_bound

    def get_upper_bound(self):
        return self.upper_bound

    def get_bounds(self):
        return self.get_lower_bound(), self.get_upper_bound()

    def __build_atom_map(self):
        return {a.name: a.value for a in self.atoms}

    def __evaluate_atom_values(self, atom_values):
        sample = list(atom_values.values())[0]
        if isinstance(sample, (tuple, list)):
            return interval_eval_node(self.expression_tree, atom_values)
        if isinstance(sample, (int, float)):
            return eval_node(self.expression_tree, atom_values)

    def evaluate(self, input_value):
        if isinstance(input_value, dict):
            return self.__evaluate_atom_values(input_value)
        elif isinstance(input_value, Generator):
            return self.__evaluate_generator(input_value)
        return None

    def __evaluate_generator(self, input_generator):
        if isinstance(input_generator, PartiallyObservedMarkovChain):
            self.value = self.__evaluate_pomc(input_generator)
        return self.value

    def __evaluate_pomc(self, pomc):
        for atom in self.atoms:
            atom.evaluate(pomc)
        return self.evaluate(self.get_atom_values())

    def to_dict(self):
        return {"atoms": [atoms.to_dict() for atoms in self.atoms], "expression": self.expression,
                "lower_bound": self.lower_bound, "upper_bound": self.upper_bound, "value": self.value}

