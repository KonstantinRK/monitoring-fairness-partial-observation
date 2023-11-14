from generators.markov_chain_collection import *
import pandas as pd
import os
import time


class MixingTimeExperimentBase:

    def __init__(self, max_range=12, path = "experimental_data"):
        self.max_range = max_range
        self.name = "mixing_time_experiment"
        self.path = os.path.join(path, self.name + "_" + str(int(time.time())))

    def run(self):
        data = []
        os.mkdir(self.path)
        for i in range(2, self.max_range+1):
            h = HyperCube(i)
            hk = HyperCubeKnown(i)
            h.setup()
            hk.setup()
            data.append([i, "loose", h.bound_mixing_time(1 / 4)])
            data.append([i, "tight", hk.bound_mixing_time(1 / 4)])
            print([i, "loose", h.bound_mixing_time(1 / 4)])
            print([i, "tight", hk.bound_mixing_time(1 / 4)])
            print("-" * 100)
        df = pd.DataFrame(data, columns=["size", "bound", "mixing_time"])
        df.to_csv(os.path.join(self.path, "data.csv"))


