from experiments.experiment import Experiment
from utils.data_analysis import DataAnalyser


class DefaultExperiment(Experiment):

    def __init__(self, name, generator, expression, monitor, duration, repetitions, path="experimental_data", *args, **kwargs):
        super().__init__(name, generator, expression, monitor, duration, repetitions, path, *args, **kwargs)

    def analyse(self, data):
        super().analyse(data)
        self.data_analyser.plot_processed_verdicts()
