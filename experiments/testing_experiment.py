from generators.partially_observed_markov_chain import PartiallyObservedMarkovChain
from specifications.quantitative_expression import QuantitativeExpression
from specifications.atom import Atom
from specifications.dict_function import DictFunction
from monitors.quantitative_monitor import QuantitativeMonitor
from experiments.experiment import Experiment
import numpy as np


class SmallExperiment(Experiment):
    def __init__(self):
        name = "test_experiment"
        f1 = DictFunction({("a", "b"): 1})
        p1 = Atom("p1", f1)
        q1 = QuantitativeExpression("q1", "p1", [p1])
        mc = PartiallyObservedMarkovChain("small_mc", np.array([[0.9,0.1,0.0],[0.8,0.1,0.1],[0.7,0.2,0.1]]), {0: "a", 1: "b", 2: "a"})
        monitor = QuantitativeMonitor(0.95, q1)
        super().__init__(name, mc, q1, monitor, 100, 2)


