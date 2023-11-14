import math
from monitors.monitor import Monitor
from generators.partially_observed_markov_chain import PartiallyObservedMarkovChain
from utils.output_dict import get_output_dict
import numpy as np


class AtomMonitor(Monitor):

    def __init__(self, confidence, atom, mixing_time=None):
        super().__init__("atom_monitor", confidence)
        self.mixing_time = mixing_time
        self.atom = atom
        self.time_step = 0
        self.estimate = 0
        self.error = None
        self.observation_array = [None]*atom.get_arity()

    def setup(self, generator, epsilon_mix=1/4, start_at=None, *args, **kwargs):
        if self.mixing_time is None:
            if isinstance(generator, PartiallyObservedMarkovChain):
                self.mixing_time = generator.bound_mixing_time(epsilon_mix)
            if isinstance(generator, int):
                self.mixing_time = generator
        self.error = None
        self.observation_array = [None]*self.atom.get_arity()
        if start_at is None:
            self.time_step = 0
            self.estimate = 0
        else:
            self.time_step = start_at
            self.estimate = self.atom.value

    def compute_for_time(self, time_step):
        n = time_step - self.atom.get_arity() + 1
        estimate = self.atom.value
        if n > 0:
            error = math.sqrt(math.log(2 / (1 - self.confidence)) * time_step * min(n, self.atom.get_arity()) * 9 * self.mixing_time / (2 * n ** 2))
            point_estimate = min(max(self.atom.get_lower_bound(), estimate), self.atom.get_upper_bound())
            lower_bound = max(self.atom.get_lower_bound(), estimate - error)
            upper_bound = min(self.atom.get_upper_bound(), estimate + error)
            return get_output_dict(lower_bound, upper_bound, point_estimate, self.atom.value)
        else:
            return get_output_dict(self.atom.get_lower_bound(), self.atom.get_upper_bound(), 0, self.atom.value)

    def next_step(self, next_observation):
        self.time_step += 1
        removed_observation = self.observation_array.pop(0)
        self.observation_array.append(next_observation)
        if removed_observation is not None:
            value = self.atom.evaluate(self.observation_array)
            self.estimate = (self.estimate * (self.time_step - self.atom.get_arity()) + value) / \
                            (self.time_step - self.atom.get_arity() + 1)
            self.error = self.error_computation()
            # print(self.error)
            #print(self.mixing_time, self.atom.name, self.estimate,  self.error)
            return self.compute_output()
        return get_output_dict(self.atom.get_lower_bound(), self.atom.get_upper_bound(), 0, self.atom.value)

    def compute_output(self):
        lb, ub = self.get_interval_estimate()
        return get_output_dict(lb, ub, self.get_point_estimate(), self.atom.value)

    def get_point_estimate(self):
        return min(max(self.atom.get_lower_bound(), self.estimate), self.atom.get_upper_bound())

    def get_interval_estimate(self):
        return max(self.atom.get_lower_bound(), self.estimate-self.error), \
            min(self.atom.get_upper_bound(), self.estimate+self.error)

    def error_computation(self):
        time_step = self.time_step
        n = time_step - self.atom.get_arity() + 1
        return math.sqrt(math.log(2/(1-self.confidence)) * time_step * min(n, self.atom.get_arity())
                         * 9 * self.mixing_time / (2 * n ** 2))

    def to_dict(self):
        return super().to_dict() | {"atom": self.atom.to_dict()}

    