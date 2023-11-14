from generators.markov_chain_collection import *
import pandas as pd
import os
import time
import os
from utils.util import safe_json
import time
from pprint import pprint
from utils.data_analysis import DataAnalyser
from csv import writer

class ConcentrationExperiment:

    def __init__(self, name,  generator, expression, monitor, max_time, time_steps, path="experimental_data"):
        self.monitor = monitor
        self.generator = generator
        self.max_time = max_time
        self.time_steps = time_steps
        self.expression = expression
        self.name = "_".join([name, generator.name, expression.name, monitor.name, str(max_time), str(time_steps)])
        self.path =  os.path.join(path, self.name + "_" + str(int(time.time())))

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
        self.monitor.setup(self.generator)

    def run(self):
        self.setup()
        data = []
        for e, i in enumerate(range(1,self.max_time, self.time_steps)):
            verdict = self.monitor.compute_for_time(i)
            lb, ub = self.process_output(verdict)
            data.append([i, "$Lower Bound$", lb])
            data.append([i, "$Upper Bound$", ub])
            data.append([i, "$True Value$", self.expression.value])
            if e % 10**6 == 0:
                print("Done:", i/self.max_time)
        df = pd.DataFrame(data, columns=["observations", "bounds", "value"])
        df.to_csv(os.path.join(self.path, "data.csv"), header=False)

    def process_output(self, verdict):
        results = [verdict[self.expression.name][k] for k in
                   ["verdict_lower", "verdict_upper"]]
        return results

    def compute_true_values(self):
        return self.expression.evaluate(self.generator)

    def meta_dict(self):
        return {
            "true_value": float(self.expression.value),
            "monitor": self.monitor.to_dict(),
            "expression": self.expression.to_dict(),
            "generator": self.generator.to_dict(),
        }