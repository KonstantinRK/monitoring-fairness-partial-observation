from experiments.experiment import Experiment
from experiments.default_experiment import DefaultExperiment
from experiments.coverage_experiment import CoverageExperiment
from monitors.quantitative_monitor import QuantitativeMonitor
from generators.markov_chain_collection import *
from specifications.specification_collection import *
from experiments.mixing_time_experiment import *
from experiments.concentration_experiment import *

DEFAULT_DURATION = 5000
DEFAULT_REPETITIONS = 10
DEFAULT_CONFIDENCE = 0.95


class MixingTimeExperiment(MixingTimeExperimentBase):

    def __init__(self):
        super().__init__(12)


class HyperCubeCoverage(DefaultExperiment):
    def __init__(self, size, index=0):
        name = "coverage-{0}-{1}".format(str(size), str(index))
        mc = HyperCube(size, batch_size=10**6)
        spec = ProbabilityAAMinusProbabilityBB()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10**8, 100)


class HyperCubeKnownCoverage(DefaultExperiment):
    def __init__(self, size, index=0):
        name = "coverage-{0}-{1}".format(str(size), str(index))
        mc = HyperCubeKnown(size, batch_size=10**6)
        spec = ProbabilityAAMinusProbabilityBB()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10**8, 100)


class HyperCubeCoverageDB(DefaultExperiment):
    def __init__(self, size, index=0):
        name = "coverage-{0}-{1}".format(str(size), str(index))
        mc = HyperCube(size, batch_size=10**6)
        spec = ProbabilityDP()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10**8, 100)


class HyperCubeKnownCoverageDB(DefaultExperiment):
    def __init__(self, size, index=0):
        name = "coverage-{0}-{1}".format(str(size), str(index))
        mc = HyperCubeKnown(size, batch_size=10**6)
        spec = ProbabilityDP()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10**8, 100)



class TinyProb(DefaultExperiment):
    def __init__(self):
        name = "basic"
        mc = TinyMC(batch_size=10**6)
        spec = ProbabilityA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10**8, 1)


class TinyProbA(DefaultExperiment):
    def __init__(self):
        name = "basic"
        mc = TinyMC()
        spec = ProbabilityA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, DEFAULT_DURATION, DEFAULT_REPETITIONS)


class TinyProbAB(DefaultExperiment):
    def __init__(self):
        name = "basic"
        mc = TinyMC()
        spec = ProbabilityAB()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, DEFAULT_DURATION, DEFAULT_REPETITIONS)


class TinyProbAA(DefaultExperiment):
    def __init__(self):
        name = "basic"
        mc = TinyMC()
        spec = ProbabilityAA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, DEFAULT_DURATION, DEFAULT_REPETITIONS)


class TinyProbABMinProbBA(DefaultExperiment):
    def __init__(self):
        name = "basic"
        mc = TinyMC()
        spec = ProbabilityABMinusProbabilityBA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, DEFAULT_DURATION, DEFAULT_REPETITIONS)


class TinyProbAADivProbAB(DefaultExperiment):
    def __init__(self):
        name = "basic"
        mc = TinyMC()
        spec = ProbabilityAADivProbabilityAB()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, DEFAULT_DURATION, DEFAULT_REPETITIONS)


class TinyProbABAdditionProbBA(DefaultExperiment):
    def __init__(self):
        name = "basic"
        mc = TinyMC()
        spec = ProbabilityABAdditionProbabilityBA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, DEFAULT_DURATION, DEFAULT_REPETITIONS)


class TinyProbABTimesProbBA(DefaultExperiment):
    def __init__(self):
        name = "basic"
        mc = TinyMC()
        spec = ProbabilityABTimesProbabilityBA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, DEFAULT_DURATION, DEFAULT_REPETITIONS)


class TinyProbBCondA(DefaultExperiment):
    def __init__(self):
        name = "basic"
        mc = TinyMC()
        spec = ProbabilityBConditionedA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, DEFAULT_DURATION, DEFAULT_REPETITIONS)


class CoverageMediumBbalancedProbAAMinProbBB(CoverageExperiment):
    def __init__(self):
        name = "coverage"
        mc = MediumBalancedMC()
        spec = ProbabilityAAMinusProbabilityBB()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 100000, 100)


class CoverageBalancedProbAAMinProbBB(CoverageExperiment):
    def __init__(self):
        name = "coverage"
        mc = BalancedMC()
        spec = ProbabilityAAMinusProbabilityBB()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 100000, 100)


class LongUnbalancedProbAAMinProbBB(DefaultExperiment):
    def __init__(self):
        name = "longrun"
        mc = UnbalancedMC()
        spec = ProbabilityAAMinusProbabilityBB()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10000000, 1)


class LongMediumBalancedProbAAMinProbBB(DefaultExperiment):
    def __init__(self):
        name = "longrun"
        mc = MediumBalancedMC()
        spec = ProbabilityAAMinusProbabilityBB()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10000000, 1)


class LongBalancedProbAAMinProbBB(DefaultExperiment):
    def __init__(self):
        name = "longrun"
        mc = BalancedMC()
        spec = ProbabilityAAMinusProbabilityBB()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10000000, 1)


class CoverageMediumBbalancedProbAA(CoverageExperiment):
    def __init__(self):
        name = "coverage"
        mc = MediumBalancedMC()
        spec = ProbabilityAA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 100000, 100)


class CoverageBalancedProbAA(CoverageExperiment):
    def __init__(self):
        name = "coverage"
        mc = BalancedMC()
        spec = ProbabilityAA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 100000, 100)


class LongUnbalancedProbAA(DefaultExperiment):
    def __init__(self):
        name = "longrun"
        mc = UnbalancedMC()
        spec = ProbabilityAA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10000000, 1)


class LongMediumBalancedProbAA(DefaultExperiment):
    def __init__(self):
        name = "longrun"
        mc = MediumBalancedMC()
        spec = ProbabilityAA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10000000, 1)


class LongBalancedProbAA(DefaultExperiment):
    def __init__(self):
        name = "longrun"
        mc = BalancedMC()
        spec = ProbabilityAA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10000000, 1)


class LongUnbalancedProb100AA(DefaultExperiment):
    def __init__(self):
        name = "longrun"
        mc = UnbalancedMC()
        spec = Probability100AA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10000000, 1)


class LongMediumBalancedProb100AA(DefaultExperiment):
    def __init__(self):
        name = "longrun"
        mc = MediumBalancedMC()
        spec = Probability100AA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10000000, 1)


class LongBalancedProb100AA(DefaultExperiment):
    def __init__(self):
        name = "longrun"
        mc = BalancedMC()
        spec = Probability100AA()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10000000, 1)




LENDING_DURATION = 10**20
LENDING_REPETITIONS = 1


class LendingHugePaSg(DefaultExperiment):
    def __init__(self):
        name = "lending"
        mc = HugeLendingMC()
        spec = ProbabilityaSg()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, LENDING_DURATION, LENDING_REPETITIONS)


class LendingLargePaSg(DefaultExperiment):
    def __init__(self):
        name = "lending"
        mc = LargeLendingMC()
        spec = ProbabilityaSg()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, LENDING_DURATION, LENDING_REPETITIONS)


class LendingMediumPaSg(DefaultExperiment):
    def __init__(self):
        name = "lending"
        mc = MediumLendingMC()
        spec = ProbabilityaSg()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, LENDING_DURATION, LENDING_REPETITIONS)


class LendingSmallPaSg(DefaultExperiment):
    def __init__(self):
        name = "lending"
        mc = SmallLendingMC()
        spec = ProbabilityaSg()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, LENDING_DURATION, LENDING_REPETITIONS)


class LendingHuge(DefaultExperiment):
    def __init__(self):
        name = "lending"
        mc = HugeLendingMC()
        spec = ProbabilityLendingDP()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, LENDING_DURATION, LENDING_REPETITIONS)


class LendingLarge(DefaultExperiment):
    def __init__(self):
        name = "lending"
        mc = LargeLendingMC()
        spec = ProbabilityLendingDP()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, LENDING_DURATION, LENDING_REPETITIONS)



class LendingMedium(DefaultExperiment):
    def __init__(self):
        name = "lending"
        mc = MediumLendingMC()
        spec = ProbabilityLendingDP()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, LENDING_DURATION, LENDING_REPETITIONS)


class LendingSmall(DefaultExperiment):
    def __init__(self):
        name = "lending"
        mc = SmallLendingMC()
        spec = ProbabilityLendingDP()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10**8, LENDING_REPETITIONS)


class LendingSmallTotal(DefaultExperiment):
    def __init__(self):
        name = "lending"
        mc = SmallLendingMC()
        spec = ProbabilityLendingTotalDP()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, 10**8, LENDING_REPETITIONS)


class LendingSmallMedium(DefaultExperiment):
    def __init__(self):
        name = "lending"
        mc = SmallMediumLendingMC()
        spec = ProbabilityLendingDP()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, LENDING_DURATION, LENDING_REPETITIONS)


class LendingMediumLarge(DefaultExperiment):
    def __init__(self):
        name = "lending"
        mc = MediumLargeLendingMC()
        spec = ProbabilityLendingDP()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor, LENDING_DURATION, LENDING_REPETITIONS)


class ConcentrationExperimentLendingDP(ConcentrationExperiment):

    def __init__(self):
        name = "convergence_lending"
        mc = SmallLendingMC()
        spec = ProbabilityLendingDP()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor,10**12, 10**7)


class ConcentrationExperimentLendingTDP(ConcentrationExperiment):

    def __init__(self):
        name = "convergence_lending"
        mc = SmallLendingMC()
        spec = ProbabilityLendingTotalDP()
        monitor = QuantitativeMonitor(DEFAULT_CONFIDENCE, spec)
        super().__init__(name, mc, spec, monitor,10**12, 10**7)
