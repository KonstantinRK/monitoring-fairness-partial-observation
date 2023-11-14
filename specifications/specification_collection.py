from specifications.quantitative_expression import QuantitativeExpression
from specifications.atom import Atom
from specifications.dict_function import DictFunction


class ProbabilityA(QuantitativeExpression):
    def __init__(self):
        name = "Pa"
        f1 = DictFunction({tuple("a"): 1})
        p1 = Atom("Pa", f1)
        super().__init__(name, "Pa", [p1])


class ProbabilityAB(QuantitativeExpression):
    def __init__(self):
        name = "Pab"
        f1 = DictFunction({("a", "b"): 1})
        p1 = Atom("Pab", f1)
        super().__init__(name, "Pab", [p1])


class ProbabilityAA(QuantitativeExpression):
    def __init__(self):
        name = "Paa"
        f1 = DictFunction({("a", "a"): 1})
        p1 = Atom("Paa", f1)
        super().__init__(name, "Paa", [p1])


class ProbabilityABTimesProbabilityBA(QuantitativeExpression):
    def __init__(self):
        name = "Pab*Pba"
        f1 = DictFunction({("a", "b"): 1})
        p1 = Atom("Pab", f1)
        f2 = DictFunction({("b", "a"): 1})
        p2 = Atom("Pba", f2)
        super().__init__(name, "Pab * Pba", [p1, p2])


class ProbabilityABMinusProbabilityBA(QuantitativeExpression):
    def __init__(self):
        name = "Pab-Pba"
        f1 = DictFunction({("a", "b"): 1})
        p1 = Atom("Pab", f1)
        f2 = DictFunction({("b", "a"): 1})
        p2 = Atom("Pba", f2)
        super().__init__(name, "Pab - Pba", [p1, p2])


class ProbabilityAAMinusProbabilityBB(QuantitativeExpression):
    def __init__(self):
        name = "Paa-Pbb"
        f1 = DictFunction({("a", "a"): 1})
        p1 = Atom("Paa", f1)
        f2 = DictFunction({("b", "b"): 1})
        p2 = Atom("Pbb", f2)
        super().__init__(name, "Paa - Pbb", [p1, p2])


class ProbabilityAADivProbabilityAB(QuantitativeExpression):
    def __init__(self):
        name = "Paa%Pab"
        f1 = DictFunction({("a", "a"): 1})
        p1 = Atom("Paa", f1)
        f2 = DictFunction({("b", "a"): 1})
        p2 = Atom("Pab", f2)
        super().__init__(name, "Paa / Pab", [p1, p2])


class ProbabilityABAdditionProbabilityBA(QuantitativeExpression):
    def __init__(self):
        name = "Pab+2*Pba"
        f1 = DictFunction({("a", "b"): 1})
        p1 = Atom("Pab", f1)
        f2 = DictFunction({("b", "a"): 1})
        p2 = Atom("Pba", f2)
        super().__init__(name, "Pab+2*Pba", [p1, p2])


class ProbabilityBConditionedA(QuantitativeExpression):
    def __init__(self):
        name = "PbCa"
        f1 = DictFunction({("a", "b"): 1})
        f2 = DictFunction({tuple("a"): 1})
        p1 = Atom("Pab", f1)
        p2 = Atom("Pa", f2)
        super().__init__(name, "Pab / Pa", [p1, p2])


class Probability100AA(QuantitativeExpression):
    def __init__(self):
        name = "P100a"
        f1 = DictFunction({tuple(["a"]*100): 1})
        p1 = Atom("P100a", f1)
        super().__init__(name, "P100a", [p1])


class ProbabilityaSg(QuantitativeExpression):
    def __init__(self):
        alphabet = ["*", "a", "b", "r", "g", "s", "f", "1", "2", "3", "4", "5"]
        name = "PaS1"
        f1 = DictFunction({("a", i, "g"): 1 for i in alphabet})
        p1 = Atom("PaS1", f1)
        super().__init__(name, "PaS1", [p1])


class ProbabilityLendingTotalDP(QuantitativeExpression):
    def __init__(self):
        alphabet = ["*", "a", "b", "r", "g", "s", "f", "1", "2", "3", "4", "5"]
        name = "TDP"
        f1 = DictFunction({("a", i, "g"): 1 for i in alphabet})
        p1 = Atom("PaSg", f1)
        f3 = DictFunction({("b", i, "g"): 1 for i in alphabet})
        p3 = Atom("PbSg", f3)
        super().__init__(name, "PaSg - PbSg", [p1, p3,], lower_bound=-1, upper_bound=1)

class ProbabilityLendingDP(QuantitativeExpression):
    def __init__(self):
        alphabet = ["*", "a", "b", "r", "g", "s", "f", "1", "2", "3", "4", "5"]
        name = "DP"
        f1 = DictFunction({("a", i, "g"): 1 for i in alphabet})
        p1 = Atom("PaSg", f1)
        f2 = DictFunction({tuple("a"): 1}, lower_bound=0.0001)
        p2 = Atom("Pa", f2)
        f3 = DictFunction({("b", i, "g"): 1 for i in alphabet})
        p3 = Atom("PbSg", f3)
        f4 = DictFunction({tuple("b"): 1}, lower_bound=0.0001)
        p4 = Atom("Pb", f4)
        super().__init__(name, "PaSg/Pa - PbSg/Pb", [p1, p2, p3, p4], lower_bound=-1, upper_bound=1)


class ProbabilityDP(QuantitativeExpression):
    def __init__(self):
        alphabet = ["a", "b"]
        name = "DP"
        f1 = DictFunction({("a","a"): 1 for i in alphabet})
        p1 = Atom("Paa", f1)
        f2 = DictFunction({tuple("a"): 1})
        p2 = Atom("Pa", f2)
        f3 = DictFunction({("b","b"): 1 for i in alphabet})
        p3 = Atom("Pbb", f3)
        f4 = DictFunction({tuple("b"): 1})
        p4 = Atom("Pb", f4)
        super().__init__(name, "Paa/Pa - Pbb/Pb", [p1, p2, p3, p4], lower_bound=-1, upper_bound=1)