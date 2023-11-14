import os
from io import StringIO
import time
import shutil

class SlimData:

    def __init__(self, base_path="", directory_name="experimental_data", filter_words=None, increments=10**6):
        self.path_from = os.path.join(base_path, directory_name)
        self.directory_to_name = "slim_" + directory_name + str(int(time.time()))
        self.path_to = os.path.join(base_path, self.directory_to_name)
        self.increments = increments
        self.filter_words = filter_words

    def setup(self):
        try:
            os.mkdir(self.path_to)
        except FileExistsError:
            self.setup()

    def process(self):
        self.setup()
        for directory in os.listdir(self.path_from):
            process = True
            for word in self.filter_words:
                if word in directory:
                    break
                process = False
            if process:
                path_from = os.path.join(self.path_from, directory)
                path_to = os.path.join(self.path_to, directory)
                if os.path.isdir(path_from) and directory[0]!=".":
                    os.mkdir(path_to)
                    for file in os.listdir(path_from):
                        file_path_from = os.path.join(path_from, file)
                        file_path_to = os.path.join(path_to, file)
                        print(file_path_from)
                        print(file_path_to)
                        if file[0] != ".":
                            if ".csv" in file:
                                self.slim_file(file_path_from, file_path_to)
                            else:
                                shutil.copyfile(file_path_from, file_path_to)
                            print(os.path.getsize(file_path_from)/1024**3, "--->", os.path.getsize(file_path_to)/1024**3)
                            print("")

    def slim_file(self, path_from, path_to):
        i = 0
        new_file = StringIO()
        with open(path_from, "r") as f:
            for line in f:
                if i % self.increments == 0:
                    new_file.write(line)
                i += 1
        with open(path_to, "w") as f:
            f.write(new_file.getvalue())

