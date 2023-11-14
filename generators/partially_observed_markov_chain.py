import numpy as np
from generators.generator import Generator
from utils.util import get_sigma_n, save_to_csv
import os


class PartiallyObservedMarkovChain(Generator):

    def __init__(self, name, transition_matrix, label_function, initial_distribution=None, execution_path=None,
                 stationary_distribution=None, spectral_gap=None, states=None, path=None, batch_size=10 ** 6, mixing_time=None, *args, **kwargs):
        super().__init__(name, path)
        self.transition_matrix = np.array(transition_matrix) if transition_matrix is not None else None
        self.initial_distribution = np.array(initial_distribution) if initial_distribution is not None else None
        self.stationary_distribution = np.array(stationary_distribution) if stationary_distribution is not None else None
        self.spectral_gap = spectral_gap
        self.label_function = label_function if not isinstance(label_function, dict) else lambda x: label_function[x]
        self.batch_size = batch_size
        self.mixing_time = mixing_time
        self.states = np.array(range(len(transition_matrix))) if states is None else states
        self.size = len(self.states)

        self.current_state = None
        self.execution_path = execution_path

    def reset(self):
        self.transition_matrix = None
        self.stationary_distribution = None
        self.stationary_distribution = None
        self.states = None

    def setup(self):
        if self.stationary_distribution is None or self.spectral_gap is None:
            self.stationary_distribution, self.spectral_gap = self.spectral_analysis()
        if self.initial_distribution is None:
            self.initial_distribution = self.stationary_distribution

    def initial_step(self):
        if self.execution_path is None or len(self.execution_path) == 0:
            self.current_state = None
            self.execution_path = []
            self.current_state = np.random.choice(self.states, p=self.initial_distribution)
            self.record_step()
        else:
            self.current_state = self.execution_path[-1]
        return self.current_state

    def observations(self, execution_path):
        if isinstance(execution_path, list):
            return [self.label_function(s) for s in execution_path]
        else:
            return self.label_function(execution_path)

    def get_observed_path(self):
        return self.observations(self.execution_path)

    def record_step(self):
        if self.batch_size is not None and self.batch_size < len(self.execution_path):
            self.save_execution_path()
            #self.save_execution_trace()
            self.execution_path = []
        self.execution_path.append(self.current_state)

    def save_execution_trace(self):
        path = os.path.join(self.path, "execution_trace.csv")
        save_to_csv(path, self.observations(self.execution_path))

    def load_execution_trace(self):
        path = os.path.join(self.path, "execution_trace.csv")
        save_to_csv(path, self.observations(self.execution_path))

    def next_step(self, record=False):
        self.current_state = np.random.choice(self.states, p=self.transition_matrix[self.current_state])
        if record:
            self.record_step()
        return self.current_state

    def run_for(self, duration, reset=True):
        if reset:
            self.execution_path = []
        self.initial_step()
        for i in range(duration):
            self.next_step()
        return self.execution_path

    def spectral_analysis(self):
        transition_matrix_transp = self.transition_matrix.T
        eigenvals, eigenvects = np.linalg.eig(transition_matrix_transp)
        close_to_1_idx = np.isclose(eigenvals, 1)
        target_eigenvect = eigenvects[:, close_to_1_idx]
        target_eigenvect = target_eigenvect[:, 0]
        stationary_distrib = target_eigenvect / sum(target_eigenvect)
        eigenvals = np.sort(eigenvals)
        spectral_gap = 1 - np.max(np.abs(eigenvals)[0:-1])
        return stationary_distrib.astype(np.float64), spectral_gap

    def probability_path(self, execution_path):
        return self.initial_distribution[execution_path[0]] * \
            np.prod([self.transition_matrix[execution_path[i]][execution_path[i + 1]] for i in range(len(execution_path) - 1)])

    def expectation_observation_path(self, function, arity):
        return np.sum([function(self.observations(execution_path)) * self.probability_path(execution_path)
                       for execution_path in get_sigma_n(self.states, arity)])

    def bound_mixing_time(self, epsilon):
        if self.mixing_time is None:
            relaxation_time = 1 / self.spectral_gap
            N = len(self.states)
            print(float(2 * N * relaxation_time * np.log(relaxation_time) + \
                4 * (1 + np.log(2)) * N * relaxation_time + 2 * (1 /np.log(epsilon) - 1) * relaxation_time))
            return float(2 * N * relaxation_time * np.log(relaxation_time) + \
                4 * (1 + np.log(2)) * N * relaxation_time + 2 * (1 /np.log(epsilon) - 1) * relaxation_time)
        else:
            print(self.mixing_time(epsilon))
            return self.mixing_time(epsilon)

    # !!! COULD BE WRONG CHECK EPSILON

    def to_dict(self, small=True):
        class_dict = {"name": self.name,
                      "spectral_gap": self.spectral_gap,
                      "size": self.size,
                      "mixing_time_bound": self.bound_mixing_time(1/4),
                      # "execution_path": self.execution_path,
                      }
        if not small:
            class_dict["transition_matrix"] = self.transition_matrix.tolist()
            class_dict["initial_distribution"] = self.initial_distribution.tolist()
            class_dict["stationary_distribution"] = self.stationary_distribution.tolist()
            class_dict["label_dict"] = {int(i): self.label_function(i) for i in self.states}
        return class_dict


    @staticmethod
    def load_from_dict(path):
        class_dict = super().load_from_dict(path)
        return PartiallyObservedMarkovChain(**class_dict)
