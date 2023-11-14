from experiments.experiment_collection import *
from multiprocessing import Pool
import sys
EXPERIMENT_LIST = [LendingSmall, LendingMedium, LendingLarge, LendingMediumLarge, LendingSmallMedium] + [HyperCubeCoverageDB]*10 + [HyperCubeKnownCoverageDB]*10
PARA_LIST = [[]]*5 + [[8, i] for i in range(10)] + [[8, i] for i in range(10)]


# for e in EXPERIMENT_LIST:
#     try:
#         e().run()
#     except:
#         pas

EXP_NR = 10

EXPERIMENT_LIST[EXP_NR](*PARA_LIST[EXP_NR]).run()