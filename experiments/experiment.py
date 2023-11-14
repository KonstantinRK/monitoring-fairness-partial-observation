import os
from utils.util import safe_json
import time
from pprint import pprint
from utils.data_analysis import DataAnalyser
from csv import writer


class Experiment:

    def __init__(self, name, generator, expression, monitor, duration, repetitions, path="experimental_data",
                 batch_size=10**6, start_at=None, *args, **kwargs):
        if not os.path.exists(path):
            os.mkdir(path)
        self.name = "_".join([name, generator.name, expression.name, monitor.name, str(duration), str(repetitions)])
        self.path = os.path.join(path, self.name + "_" + str(int(time.time())))
        self.generator = generator
        self.expression = expression
        self.monitor = monitor
        self.duration = duration
        self.repetitions = repetitions
        self.data_analyser = DataAnalyser(self.path)
        self.is_not_setup = True
        self.batch_size = batch_size
        self.start_at = start_at

    def setup(self):
        print("-" * 100)
        print("Setup: ", self.name)
        print("-" * 100)
        os.mkdir(self.path)
        self.generator.setup()
        self.compute_true_values()
        meta_dict = self.meta_dict()
        # pprint(meta_dict)
        safe_json(os.path.join(self.path, "meta"), meta_dict)
        #print(self.generator.bound_mixing_time(1/4))

    # ["time", "state", "observation","execution_time" ,"verdict_lower", "verdict_upper", "point_estimate"]
    def process_state(self, state):
        observation = self.generator.observations(state)
        verdict = self.monitor.next_step(observation)
        execution_time = verdict["execution_time"]
        results = [verdict["return"][self.expression.name][k] for k in ["verdict_lower", "verdict_upper", "point_estimate" ]]
        return [state, observation, execution_time] + results

    def run(self, analyse=False):
        if self.is_not_setup:
            self.setup()
            self.is_not_setup = False
        data = []
        for repetition in range(self.repetitions):
            print("-"*100)
            print("Repetition {0}: ".format(repetition), self.name)
            print("-" * 100)
            self.monitor.setup(self.generator, start_at=self.start_at)
            state = self.generator.initial_step()
            data.append([0] + self.process_state(state))
            for i in range(1, self.duration):
                state = self.generator.next_step()
                data.append([i] + self.process_state(state))
                if i % self.batch_size == 0:
                    print("save batch", i)
                    self.save_batch(data, repetition)
                    data = []
            self.save_batch(data, repetition)
        print("#"*100)
        print("#"*100)

    def save_batch(self, data, repetition):
        with open(os.path.join(self.path, "data_{0}.csv".format(repetition)), 'a') as f:
            writer_object = writer(f)
            for row in data:
                writer_object.writerow(row)
            f.close()

    def run2(self, analyse=False):
        if self.is_not_setup:
            self.setup()
            self.is_not_setup = False
        data = []
        for repetition in range(self.repetitions):
            print("-" * 100)
            print("Repetition {0}: ".format(repetition), self.name)
            print("-" * 100)
            self.monitor.setup(self.generator)
            self.generator.initial_step()
            actual_path = self.generator.run_for(self.duration, reset=True)
            observed_path = self.generator.observations(actual_path)
            results = self.monitor.run_on(observed_path)
            experiment_dict = self.experiment_dict(repetition, actual_path, observed_path, results)
            # pprint(experiment_dict)
            safe_json(os.path.join(self.path, "repetition_" + str(repetition)), experiment_dict)
            data += experiment_dict
        safe_json(os.path.join(self.path, "all_data"), data)
        if analyse:
            self.analyse(data)
        print("#" * 100)
        print("#" * 100)

    def analyse(self, data):
        print("-" * 100)
        print("Analyse: ", self.name)
        print("-" * 100)
        self.data_analyser.process_verdicts(data)
        self.data_analyser.aggregate_verdicts()

    def compute_true_values(self):
        return self.expression.evaluate(self.generator)

    @staticmethod
    def experiment_dict(repetition, actual_path, observed_path, results):
        return [{"verdicts": result["return"],
                 "repetition": repetition,
                 "state": actual_path[i],
                 "observation": observed_path[i],
                 "execution_time": result["execution_time"],
                 "time": i
                 } for i, result in enumerate(results)]
        # return {
        #     "repetition": repetition,
        #     "actual_path": actual_path,
        #     # "observed_path": observed_path,
        #     "execution_times": [entry["execution_times"] for entry in additional_information_dict],
        #     "verdict_values": {atom.name: {"verdict_lower": [entry["atom_values"][atom.name][0]
        #                                                   for entry in additional_information_dict],
        #                                    "verdict_upper": [entry["atom_values"][atom.name][1]
        #                                                   for entry in additional_information_dict],
        #                                    "true_value": [atom.value] * len(verdict_lower)
        #                                    } for atom in self.expression.atoms} |
        #                       {self.expression.name: {"verdict_lower": verdict_lower,
        #                                               "verdict_upper": verdict_upper,
        #                                               "true_value": [self.expression.value] * len(verdict_lower)}},
        # }

    def meta_dict(self):
        return {
            "true_value": float(self.expression.value),
            "monitor": self.monitor.to_dict(),
            "expression": self.expression.to_dict(),
            "generator": self.generator.to_dict(),
        }

