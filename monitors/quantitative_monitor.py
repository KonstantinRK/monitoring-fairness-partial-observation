from monitors.monitor import Monitor
from monitors.atom_monitor import AtomMonitor
from generators.partially_observed_markov_chain import PartiallyObservedMarkovChain
from utils.util import timeit
from utils.output_dict import get_output_dict
from pprint import pprint
import numpy as np

class QuantitativeMonitor(Monitor):

    def __init__(self, confidence, expression, mixing_time=None):
        super().__init__("quantitative_monitor", confidence)
        self.mixing_time = mixing_time
        self.expression = expression
        self.atom_monitors = []

    def setup(self, generator, epsilon_mix=1/4, start_at=None, *args, **kwargs):
        if self.mixing_time is None:
            if isinstance(generator, PartiallyObservedMarkovChain):
                self.mixing_time = generator.bound_mixing_time(epsilon_mix)
            if isinstance(generator, int):
                self.mixing_time = generator
        self.atom_monitors = [AtomMonitor(1 - (1 - self.confidence) / len(self.expression.atoms), a,
                                          self.mixing_time) for a in self.expression.atoms]
        for a in self.atom_monitors:
            a.setup(generator, epsilon_mix, start_at)

    @timeit
    def next_step(self, next_observation, atoms=False):
        atom_estimates = {atom_monitor.atom.name: atom_monitor.next_step(next_observation)
                          for atom_monitor in self.atom_monitors}
        interval_estimates = {atom: (values["verdict_lower"], values["verdict_upper"])
                              for atom, values in atom_estimates.items()}
        point_estimates = {atom: values["point_estimate"]
                           for atom, values in atom_estimates.items()}
        # pprint(atom_estimates)
        # pprint(self.compute_output(point_estimates, interval_estimates))
        # print("______")
        if atoms:
            return {self.expression.name: self.compute_output(point_estimates, interval_estimates)} | atom_estimates
        else:
            return {self.expression.name: self.compute_output(point_estimates, interval_estimates)}

    def compute_output(self, point_estimates, interval_estimates):
        pe = self.expression.evaluate(point_estimates)
        lb, ub = self.compute_bounds(self.expression.evaluate(interval_estimates))
        # print(interval_estimates)
        # print(pe)
        # print(point_estimates)
        # print(lb, ub)
        return get_output_dict(lb, ub, pe, self.expression.value)

    def compute_for_time(self, time_step, atoms=False):
        atom_estimates = {atom_monitor.atom.name: atom_monitor.compute_for_time(time_step)
                          for atom_monitor in self.atom_monitors}
        interval_estimates = {atom: (values["verdict_lower"], values["verdict_upper"])
                              for atom, values in atom_estimates.items()}
        point_estimates = {atom: values["point_estimate"]
                           for atom, values in atom_estimates.items()}
        # pprint(atom_estimates)
        # pprint(self.compute_output(point_estimates, interval_estimates))
        # print("______")
        if atoms:
            return {self.expression.name: self.compute_output(point_estimates, interval_estimates)} | atom_estimates
        else:
            return {self.expression.name: self.compute_output(point_estimates, interval_estimates)}

    def compute_bounds(self, verdict):
        verdict = list(verdict)
        if np.isnan(verdict[0]):
            verdict[0] = - np.infty
        if np.isnan(verdict[1]):
            verdict[1] = np.infty
        return max(verdict[0], self.expression.get_lower_bound()), min(verdict[1], self.expression.get_upper_bound())

    def to_dict(self):
        return super().to_dict() | {"atoms": [atom.to_dict() for atom in self.atom_monitors]}