from generators.partially_observed_markov_chain import PartiallyObservedMarkovChain
import numpy as np
import math
import itertools
from pprint import pprint
from utils.util import list_stars_and_bars, edit_tuple


class HyperCubeBase(PartiallyObservedMarkovChain):

    def __init__(self, name, size,  *args, **kwargs):
        super().__init__(name, self.construct_transition_matrix(size), self.construct_dictionary(size),  *args, **kwargs)


    @staticmethod
    def construct_transition_matrix(size):
        states = list(itertools.product([0, 1], repeat=size))
        sid = {s: i for i, s in enumerate(states)}
        trmtr = np.zeros((len(states), len(states)))
        for s in states:
            trmtr[sid[s]][sid[s]] = 1/2
            for i in range(size):
                s_next = tuple([s[j] if j != i else int(not bool(s[j])) for j in range(size)])
                trmtr[sid[s]][sid[s_next]] = 1/2*1/size
        return trmtr

    @staticmethod
    def flip(value):
        return 1 if value == 0 else 0

    @staticmethod
    def construct_dictionary(size):
        return {i: "a" if bool(s[0]) else "b" for i, s in enumerate(list(itertools.product([0, 1], repeat=size)))}

class HyperCube(HyperCubeBase):

    def __init__(self, size, *args, **kwargs):
        super().__init__("hypercube-" + str(size), size, *args, **kwargs)


class HyperCubeKnown(HyperCubeBase):

    def __init__(self, size,  *args, **kwargs):
        super().__init__("hypercube-known-"+str(size), size,
                         mixing_time=lambda epsilon: size * math.log(size) + size*math.log(1 / epsilon), *args, **kwargs)




class TinyMC(PartiallyObservedMarkovChain):

    def __init__(self, *args, **kwargs):
        super().__init__("tiny-mc", [[0.9,0.1,0.0],[0.8,0.1,0.1],[0.7,0.2,0.1]], {0: "a", 1: "b", 2: "a"},  *args, **kwargs)


class UnbalancedMC(PartiallyObservedMarkovChain):

    def __init__(self):
        super().__init__("unbalanced-mc", [[0., 0.25, 0.25, 0.25, 0.25],
                                     [0.02, 0.96, 0.02, 0., 0.],
                                     [0.02, 0.96, 0.02, 0., 0.],
                                     [0.02,  0., 0., 0.96, 0.02],
                                     [0.02, 0., 0., 0.96, 0.02],
                                     ], {0: "c", 1: "a", 2: "b", 3: "b", 4: "a"})


class MediumBalancedMC(PartiallyObservedMarkovChain):

    def __init__(self):
        super().__init__("medium-balanced-mc", [[0., 0.25, 0.25, 0.25, 0.25],
                                     [0.20, 0.60, 0.20, 0., 0.],
                                     [0.20, 0.60, 0.20, 0., 0.],
                                     [0.20,  0., 0., 0.60, 0.20],
                                     [0.20, 0., 0., 0.60, 0.20],
                                     ], {0: "c", 1: "a", 2: "b", 3: "b", 4: "a"})


class BalancedMC(PartiallyObservedMarkovChain):

    def __init__(self):
        super().__init__("balanced-mc", [[0.2, 0.2, 0.2, 0.2, 0.2],
                                     [0.2, 0.2, 0.2, 0.2, 0.2],
                                     [0.2, 0.2, 0.2, 0.2, 0.2],
                                     [0.2, 0.2, 0.2, 0.2, 0.2],
                                     [0.2, 0.2, 0.2, 0.2, 0.2],
                                     ], {0: "c", 1: "a", 2: "b", 3: "b", 4: "a"})


class GeneralLevelMC(PartiallyObservedMarkovChain):

    def __init__(self, name, levels, level_self_probability=None):
        self.self_probability = [0]*len(levels) if level_self_probability is None else level_self_probability
        self.id_state_map = [(e,) for e in levels[0]]
        self.state_id_map = {s: i for i, s in enumerate(self.id_state_map)}
        self.label_dict = {self.get_id(s): self.get_label(s) for s in self.id_state_map}
        self.temp_probabilities = {}
        self.transition_matrix = None
        self.initialise_probabilities(levels)
        self.transfer_to_transition_matrix()
        super().__init__(name, self.transition_matrix, self.label_dict)
        self.temp_probabilities = None
       # self.print_positive_probabilities()

    def setup(self):
        super().setup()
        # self.print_positive_probabilities()

    def reset(self):
        super().reset()
        self.id_state_map = None
        self.state_id_map = None
        self.label_dict = None
        self.temp_probabilities = None

    def print_positive_probabilities(self):
        for id1, s1 in enumerate(self.id_state_map):
            ps = np.sum(self.transition_matrix[id1])
            print("#" * 100)
            print("-" * 100)
            print("{1} | {0} ---> *".format(s1, round(ps, 2)))
            print("-" * 100)
            for id2, s2 in enumerate(self.id_state_map):
                p = self.transition_matrix[id1][id2]
                if p > 0:
                    print("    {2} | {0} ---> {1}".format(s1, s2, round(p, 2)))
            print("#"*100)
            print("")

    def print_zero_probabilities(self):
        for id1, s1 in enumerate(self.id_state_map):
            ps = np.sum(self.transition_matrix[id1])
            if ps == 0:
                print("-" * 100)
                print("{1} | {0} ---> *".format(s1, round(ps, 2)))
                print("-" * 100)

    def print_not1_probabilities(self):
        for id1, s1 in enumerate(self.id_state_map):
            ps = np.sum(self.transition_matrix[id1])
            if ps != 1:
                print("#" * 100)
                print("-" * 100)
                print("{1} | {0} ---> *".format(s1, round(ps, 2)))
                print("-" * 100)
                for id2, s2 in enumerate(self.id_state_map):
                    p = self.transition_matrix[id1][id2]
                    if p > 0:
                        print("    {2} | {0} ---> {1}".format(s1, s2, round(p, 2)))
                print("#" * 100)
                print("")

    def get_id(self, state):
        return self.state_id_map[state]

    def transfer_to_transition_matrix(self):
        self.transition_matrix = np.zeros((len(self.id_state_map), len(self.id_state_map)))
        for k, v in self.temp_probabilities.items():
            self.transition_matrix[k[0]][k[1]] = v

    def initialise_probabilities(self, levels):
        self.add_transition_level(tuple(), levels)

    def add_transition_level(self, state, levels):
        if len(levels) <= len(state):
            for next_state in self.get_return_states(state):
                self.add_probability(state, next_state, len(state))
        else:
            for next_level in levels[len(state)]:
                next_state = (*state, next_level)
                if len(state) > 0:
                    if self.get_probability(state, next_state) > 0:
                        self.add_to_maps(next_state)
                        self.add_self_probability(state, len(state))
                        self.add_probability(state, next_state, len(state))
                        self.add_transition_level(next_state, levels)
                else:
                    self.add_transition_level(next_state, levels)

    def add_self_probability(self, state, level):
        s1_id = self.get_id(state)
        self.temp_probabilities[s1_id, s1_id] = self.self_probability[level-1]

    def add_probability(self, state, next_state, level):
        prob = self.get_probability(state, next_state)
        s1_id = self.get_id(state)
        s2_id = self.get_id(next_state)
        self.temp_probabilities[s1_id, s2_id] = prob * (1-self.self_probability[level-1])

    def add_to_maps(self, state):
        self.state_id_map[state] = len(self.id_state_map)
        self.id_state_map.append(state)
        self.label_dict[self.get_id(state)] = self.get_label(state)

    def get_return_states(self, state):
        pass

    def get_probability(self, state, next_state):
        pass

    @staticmethod
    def get_label(state):
        pass


class LendingMC(GeneralLevelMC):

    NAME = "default-lending"
    GROUPS = ("a", "b")
    CREDIT_SCORES = (1, 2, 3, 4, 5)
    DECISIONS = ("r", "g")
    FEEDBACK = ("f", "n", "s")
    GROUP_DISTRIBUTION = {"a": 3, "b": 3}
    DECISION_DISTRIBUTION = {"a": {i: 0.2*i for i in CREDIT_SCORES}, "b": {i: 0.15*i for i in CREDIT_SCORES}}
    FEEDBACK_DISTRIBUTION = {"a": {i: 0.2*i for i in CREDIT_SCORES}, "b": {i: 0.2*i for i in CREDIT_SCORES}}
    INERTIA = 0.1

    def __init__(self):
        self.ENVIRONMENTS = list_stars_and_bars([self.GROUP_DISTRIBUTION[g] for g in self.GROUPS], len(self.CREDIT_SCORES))
        self.group_map = {g: i for i, g in enumerate(self.GROUPS)}
        self.credit_score_map = {c: i for i, c in enumerate(self.CREDIT_SCORES)}
        levels = [self.ENVIRONMENTS, self.GROUPS, self.CREDIT_SCORES, self.DECISIONS, self.FEEDBACK]
        self_loops = [self.INERTIA] + ([0]*(len(levels)-1))
        super().__init__(self.NAME, levels, self_loops)

    def reset(self):
        self.ENVIRONMENTS = None


    def get_group_id(self, group):
        return self.group_map[group]

    def get_credit_score_id(self, credit_score):
        return self.credit_score_map[min(max(self.CREDIT_SCORES), max(min(self.CREDIT_SCORES), credit_score))]

    def get_probability(self, state, next_state):
        level = len(state)
        if level == 1:
            return self.group_probability(*next_state)
        if level == 2:
            return self.credit_score_probability(*next_state)
        if level == 3:
            return self.decision_probability(*next_state)
        if level == 4:
            return self.feedback_probability(*next_state)
        if level == 5:
            return self.environment_probability(*state, *next_state)

    def group_probability(self, environment, group):
        return self.GROUP_DISTRIBUTION[group] / np.sum(list(self.GROUP_DISTRIBUTION.values()))

    def credit_score_probability(self, environment, group, credit_score):
        return environment[self.group_map[group]][self.credit_score_map[credit_score]]/self.GROUP_DISTRIBUTION[group]

    def decision_probability(self, environment, group, credit_score, decision):
        return self.DECISION_DISTRIBUTION[group][credit_score] if decision == "g" else \
            1-self.DECISION_DISTRIBUTION[group][credit_score]

    def feedback_probability(self, environment, group, credit_score, decision, feedback):
        if decision == "g":
            if feedback == "n":
                return 0.0
            return self.FEEDBACK_DISTRIBUTION[group][credit_score] if feedback == "s" else \
                1 - self.FEEDBACK_DISTRIBUTION[group][credit_score]
        if decision == "r" and feedback == "n":
            return 1.0
        return 0.0

    def environment_probability(self, environment, group, credit_score, decision, feedback, next_environment):
        x = self.get_return_states((environment, group, credit_score, decision, feedback))
        if (next_environment,) in x:
            return 1.0
        else:
            return 0.0

    def get_return_states(self, state):
        environment, group, credit_score, decision, feedback = state
        if feedback == "n":
            return [(environment,)]
        buf_env = edit_tuple(environment, [self.get_group_id(group),
                                           self.get_credit_score_id(credit_score)], 1, edit="-")
        if feedback == "f":
            return [(edit_tuple(buf_env, [self.get_group_id(group),
                                         self.get_credit_score_id(credit_score - 1)], 1, edit="+"), )]
        if feedback == "s":
            return [(edit_tuple(buf_env, [self.get_group_id(group),
                                         self.get_credit_score_id(credit_score + 1)], 1, edit="+"), )]

    @staticmethod
    def get_label(state):
        if len(state) == 1:
            return "*"
        else:
            return str(state[-1])

        # components = [environments, groups, credit_scores, decisions, feedback]
        # self.state_order = [(lambda x: list(itertools.product(*x)))(components[:i]) for i in range(1,len(components))]
        # self.state_map = {state: nr for nr, state in enumerate(self.state_order)}
        # self.transition_matrix


class CollapsedLendingMC(PartiallyObservedMarkovChain):

    NAME = "default-lending"
    GROUPS = ("a", "b")
    CREDIT_SCORES = (1, 2, 3, 4, 5)
    DECISIONS = ("r", "g")
    FEEDBACK = ("f", "n", "s")
    GROUP_DISTRIBUTION = {"a": 3, "b": 3}
    DECISION_DISTRIBUTION = {"a": {i: 0.2*i for i in CREDIT_SCORES}, "b": {i: 0.15*i for i in CREDIT_SCORES}}
    FEEDBACK_DISTRIBUTION = {"a": {i: 0.2*i for i in CREDIT_SCORES}, "b": {i: 0.2*i for i in CREDIT_SCORES}}

    def __init__(self):
        self.ENVIRONMENTS = list_stars_and_bars([self.GROUP_DISTRIBUTION[g] for g in self.GROUPS],
                                                len(self.CREDIT_SCORES))
        self.state_id_map = {}
        self.id_state_map = {}
        self.group_map = {g: i for i, g in enumerate(self.GROUPS)}
        self.credit_score_map = {c: i for i, c in enumerate(self.CREDIT_SCORES)}
        transition_matrix = self.compute_transition_matrix()
        super().__init__(self.NAME, transition_matrix, self.lending_label_function)

    def lending_label_function(self, state_id):
        pass

    def yield_states(self, environment):
        for group in self.GROUPS:
            for score in self.CREDIT_SCORES:
                for decision in self.DECISIONS:
                    for feedback in self.FEEDBACK:
                        prob = self.compute_probability((environment, group, score, decision, feedback))
                        if prob > 0:
                            yield environment, group, score, decision, feedback

    def compute_transition_matrix(self):
        state_dict = {}
        state_id = 0
        for environment in self.ENVIRONMENTS:
            for state in self.yield_states(environment):
                self.state_id_map[state] = state_id
                self.id_state_map[state_id] = state
                state_id += 1
                state_dict[state] = []
                next_environment = self.get_next_environment(state)
                for next_state in self.yield_states(next_environment):
                    state_dict[state].append(next_state)
        return self.fill_transition_matrix(state_dict)

    def fill_transition_matrix(self, state_dict):
        transition_matrix = np.zeros((len(state_dict), len(state_dict)))
        for state, next_states in state_dict.items():
            for next_state in next_states:
                transition_matrix[self.state_id_map[state]][self.state_id_map[next_state]] = self.compute_probability(next_state)
        return transition_matrix

    def compute_probability(self, state):
        environment, group, score, decision, feedback = state
        return self.group_probability(environment, group)* self.credit_score_probability(environment,group,score) * \
            self.decision_probability(environment, group, score, decision) * \
            self.feedback_probability(environment, group, score, decision, feedback)

    def group_probability(self, environment, group):
        return self.GROUP_DISTRIBUTION[group] / np.sum(list(self.GROUP_DISTRIBUTION.values()))

    def credit_score_probability(self, environment, group, credit_score):
        return environment[self.group_map[group]][self.credit_score_map[credit_score]] / self.GROUP_DISTRIBUTION[
            group]

    def decision_probability(self, environment, group, credit_score, decision):
        return self.DECISION_DISTRIBUTION[group][credit_score] if decision == "g" else \
            1 - self.DECISION_DISTRIBUTION[group][credit_score]

    def feedback_probability(self, environment, group, credit_score, decision, feedback):
        if decision == "g":
            if feedback == "n":
                return 0.0
            return self.FEEDBACK_DISTRIBUTION[group][credit_score] if feedback == "s" else \
                1 - self.FEEDBACK_DISTRIBUTION[group][credit_score]
        if decision == "r" and feedback == "n":
            return 1.0
        return 0.0

    def get_next_environment(self, state):
        environment, group, credit_score, decision, feedback = state
        if feedback == "n":
            return [(environment,)]
        buf_env = edit_tuple(environment, [self.get_group_id(group),
                                           self.get_credit_score_id(credit_score)], 1, edit="-")
        if feedback == "f":
            return [(edit_tuple(buf_env, [self.get_group_id(group),
                                         self.get_credit_score_id(credit_score - 1)], 1, edit="+"), )]
        if feedback == "s":
            return [(edit_tuple(buf_env, [self.get_group_id(group),
                                         self.get_credit_score_id(credit_score + 1)], 1, edit="+"), )]

    def get_group_id(self, group):
        return self.group_map[group]

    def get_credit_score_id(self, credit_score):
        return self.credit_score_map[min(max(self.CREDIT_SCORES), max(min(self.CREDIT_SCORES), credit_score))]

    def get_id(self, state):
        return self.state_id_map[state]


class HugeLendingMC(LendingMC):

    NAME = "huge-lending"
    GROUPS = ("a", "b")
    CREDIT_SCORES = (1, 2, 3, 4, 5)
    DECISIONS = ("r", "g")
    FEEDBACK = ("f", "n", "s")
    GROUP_DISTRIBUTION = {"a": 5, "b": 5}
    DECISION_DISTRIBUTION = {"a": {i: 0.2*i for i in CREDIT_SCORES}, "b": {i: 0.15*i for i in CREDIT_SCORES}}
    FEEDBACK_DISTRIBUTION = {"a": {i: 0.2*i for i in CREDIT_SCORES}, "b": {i: 0.2*i for i in CREDIT_SCORES}}


class LargeLendingMC(LendingMC):

    NAME = "large-lending"
    GROUPS = ("a", "b")
    CREDIT_SCORES = (1, 2, 3, 4, 5)
    DECISIONS = ("r", "g")
    FEEDBACK = ("f", "n", "s")
    GROUP_DISTRIBUTION = {"a": 3, "b": 3}
    DECISION_DISTRIBUTION = {"a": {i: 0.2*i for i in CREDIT_SCORES}, "b": {i: 0.15*i for i in CREDIT_SCORES}}
    FEEDBACK_DISTRIBUTION = {"a": {i: 0.2*i for i in CREDIT_SCORES}, "b": {i: 0.2*i for i in CREDIT_SCORES}}


class MediumLargeLendingMC(LendingMC):

    NAME = "medium-large-lending"
    GROUPS = ("a", "b")
    CREDIT_SCORES = (1, 2, 3)
    DECISIONS = ("r", "g")
    FEEDBACK = ("f", "n", "s")
    GROUP_DISTRIBUTION = {"a": 200, "b": 200}
    DECISION_DISTRIBUTION = {"a": {1: 0.2, 2: 0.5, 3: 0.8}, "b":  {1: 0.3, 2: 0.6, 3: 0.9}}
    FEEDBACK_DISTRIBUTION = {"a":  {1: 0.3, 2: 0.6, 3: 0.9}, "b":  {1: 0.3, 2: 0.6, 3: 0.9}}


class MediumLendingMC(LendingMC):

    NAME = "medium-lending"
    GROUPS = ("a", "b")
    CREDIT_SCORES = (1, 2, 3)
    DECISIONS = ("r", "g")
    FEEDBACK = ("f", "n", "s")
    GROUP_DISTRIBUTION = {"a": 5, "b": 5}
    DECISION_DISTRIBUTION = {"a": {1: 0.2, 2: 0.5, 3: 0.8}, "b":  {1: 0.3, 2: 0.6, 3: 0.9}}
    FEEDBACK_DISTRIBUTION = {"a":  {1: 0.3, 2: 0.6, 3: 0.9}, "b":  {1: 0.3, 2: 0.6, 3: 0.9}}


class SmallMediumLendingMC(LendingMC):

    NAME = "small-medium-lending"
    GROUPS = ("a", "b")
    CREDIT_SCORES = (1, 2)
    DECISIONS = ("r", "g")
    FEEDBACK = ("f", "n", "s")
    GROUP_DISTRIBUTION = {"a": 500, "b": 500}
    DECISION_DISTRIBUTION = {"a": {1: 0.4, 2: 0.8}, "b": {1: 0.5, 2: 0.9}}
    FEEDBACK_DISTRIBUTION = {"a": {1: 0.4, 2: 0.8}, "b": {1: 0.4, 2: 0.8}}


class SmallLendingMC(LendingMC):

    NAME = "small-lending"
    GROUPS = ("a", "b")
    CREDIT_SCORES = (1, 2)
    DECISIONS = ("r", "g")
    FEEDBACK = ("f", "n", "s")
    GROUP_DISTRIBUTION = {"a": 2, "b": 2}
    DECISION_DISTRIBUTION = {"a": {1: 0.4, 2: 0.8}, "b": {1: 0.5, 2: 0.9}}
    FEEDBACK_DISTRIBUTION = {"a": {1: 0.4, 2: 0.8}, "b": {1: 0.4, 2: 0.8}}


class SmallLending2MC(LendingMC):

    NAME = "small-lending-2"
    GROUPS = ("a", "b")
    CREDIT_SCORES = (1, 2)
    DECISIONS = ("r", "g")
    FEEDBACK = ("f", "n", "s")
    GROUP_DISTRIBUTION = {"a": 2, "b": 2}
    DECISION_DISTRIBUTION = {"a": {1: 0.4, 2: 0.8}, "b": {1: 0.5, 2: 0.9}}
    FEEDBACK_DISTRIBUTION = {"a": {1: 0.4, 2: 0.8}, "b": {1: 0.4, 2: 0.8}}