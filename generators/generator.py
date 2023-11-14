import json
import os
from utils.util import save_to_csv


class Generator:

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.execution_path = []

    def setup(self):
        pass

    def next_step(self):
        pass

    def initial_step(self):
        pass

    def run_for(self, duration, reset=True):
        pass

    def to_dict(self):
        pass

    def set_path(self, path):
        self.path = path

    def save_to_dict(self, path):
        path = os.path.join(path, self.name + ".json")
        with open(path, "w") as f:
            return json.dump(self.to_dict(), f)

    def save_execution_path(self):
        path = os.path.join(self.path, "execution_path.csv")
        save_to_csv(path, self.execution_path)

    def get_file_path_execution_path(self):
        return os.path.join(self.path, "execution_path.csv")

    def observations(self, path):
        pass

    @staticmethod
    def load_from_dict(path):
        with open(path, "r") as f:
            return json.load(f)