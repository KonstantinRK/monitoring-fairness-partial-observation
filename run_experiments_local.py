from experiments.experiment_collection import *
from multiprocessing import Pool
import sys, os


def run_experiment(experiment):
    experiment().run()


if __name__ == "__main__":
    sys.stdout = open(os.devnull, 'w')
    with Pool() as pool:
        result = pool.map(run_experiment, [LongDefaultLendingProbaS1])
