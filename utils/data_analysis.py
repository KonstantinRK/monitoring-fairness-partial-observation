from utils.util import load_json
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import os
from pprint import pprint


class DataAnalyser:

    def __init__(self, base_path, data=None):
        self.base_path = base_path
        self.data_path = os.path.join(self.base_path, "all_data")
        self.processed_verdicts = None

    def load_all_data(self, data=None):
        if data is None:
            data = load_json(self.data_path)
        return data

    def process_verdicts(self, data):
        print("---")
        print("Process Verdict Data:")
        data = self.__get_verdict_data(data)
        self.processed_verdicts = pd.DataFrame(data, columns=["repetition", "time", "expression", "value_type", "value"])
        print("---")
        print("Save Verdict Data:")
        self.processed_verdicts.to_csv(os.path.join(self.base_path, "verdict_data.csv"))

    def aggregate_verdicts(self):
        print("---")
        print("Process Aggregate Verdict Data:")
        df = self.processed_verdicts.groupby(["time", "expression", "value_type"]).mean().reset_index()[["time", "expression", "value_type", "value"]]
        print("---")
        print("Save Aggregate Verdict Data:")
        df.to_csv(os.path.join(self.base_path, "aggregate_verdict_data.csv"))
        sns.relplot(kind="line", data=df, x="time", y="value", hue="value_type",
                    row="expression")
        plt.savefig(os.path.join(self.base_path, "aggregate_verdict_plot.pdf"), dpi=1000)

    def compute_coverage(self, confidence):
        print("---")
        print("Process Coverage Data:")
        lower_quantile = (1 - confidence) / 2
        upper_quantile = 1 - lower_quantile
        df = self.processed_verdicts.groupby(["time", "expression", "value_type"]).quantile([lower_quantile, upper_quantile]).reset_index().rename(columns={"level_3": "quantile"})[["time", "expression", "value_type", "quantile", "value"]]
        print("---")
        print("Save Coverage Data:")
        df.to_csv(os.path.join(self.base_path, "coverage_data.csv"))
        print("---")
        print("Plot Coverage Data:")
        sns.relplot(kind="line", data=df, x="time", y="value", col="expression",
                    hue=df[["value_type", "quantile"]].apply(tuple, axis=1))
        plt.savefig(os.path.join(self.base_path, "coverage_plot.pdf"), dpi=1000)

    # def compute_coverage(self, expression, confidence):
    #     print("---")
    #     print("Process Coverage Data:")
    #     data = []
    #     lower_quantile = (1-confidence)/2
    #     upper_quantile = 1-lower_quantile
    #     for g in self.processed_verdicts[(self.processed_verdicts["expression"] == expression)].groupby("time"):
    #         empiric_lower, empiric_upper = g[1][g[1]["value_type"] == "point_estimate"]["value"].quantile(
    #             [lower_quantile, upper_quantile]).values
    #         average_lower = g[1][g[1]["value_type"] == "verdict_lower"]["value"].mean()
    #         average_upper = g[1][g[1]["value_type"] == "verdict_upper"]["value"].mean()
    #         data.append([g[0], "empiric_lower", empiric_lower])
    #         data.append([g[0], "empiric_upper", empiric_upper])
    #         data.append([g[0], "average_lower", average_lower])
    #         data.append([g[0], "average_upper", average_upper])
    #     df = pd.DataFrame(data, columns=["time", "value_type", "value"])
    #     print("---")
    #     print("Save Coverage Data:")
    #     df.to_csv(os.path.join(self.base_path, "coverage_data.csv"))
    #     print("---")
    #     print("Plot Coverage Data:")
    #     sns.relplot(kind="line", data=df, x="time", y="value", hue="value_type")
    #     plt.savefig(os.path.join(self.base_path, "coverage_plot.pdf"), dpi=1000)

    def plot_processed_verdicts(self):
        if self.processed_verdicts is None:
            self.processed_verdicts = pd.read_csv(os.path.join(self.base_path, "verdict_data.csv"), index_col=0)
        print("---")
        print("Plot Verdict Data:")
        sns.relplot(kind="line", data=self.processed_verdicts, x="time", y="value", hue="value_type",
                    row="repetition", col="expression")
        plt.savefig(os.path.join(self.base_path, "verdict_plot.pdf"), dpi=1000)

    @staticmethod
    def __get_verdict_data(data):
        return [[entry["repetition"], entry["time"], expression, value_type, value]
                for entry in data for expression, verdict_dict in entry["verdicts"].items()
                for value_type, value in verdict_dict.items()]

    # @staticmethod
    # def __transform_verdict_dict(verdict_dict):
    #     data = []
    #     for key in verdict_dict.keys():
    #         data += DataAnalyser.__format_sequential_data(verdict_dict, key)
    #     return pd.DataFrame(data, columns=["time", "repetition", "expression", "verdict", "value"])
    #
    # @staticmethod
    # def __format_sequential_data(verdict_dict, key):
    #     data = []
    #     for repetition in verdict_dict:
    #         data += [[t, repetition["repetition"], key, entry] for t, entry in enumerate(repetition[key])]
    #     return data






