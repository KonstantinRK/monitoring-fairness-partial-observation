import os
import json
from functools import wraps
import time
import numpy as np
from pprint import pprint
import itertools

def get_sigma_n(sigma, n):
    if n == 1:
        return [[s] for s in sigma]
    sigma_1 = get_sigma_n(sigma, n-1)
    return [s2+[s1] for s2 in sigma_1 for s1 in sigma]


def safe_json(path, data):
    if path[-5:] != ".json":
        path = path + ".json"
    with open(path, "w") as f:
        json.dump(data, f, cls=NpEncoder)


def load_json(path):
    if path[-5:] != ".json":
        path = path + ".json"
    with open(path, "r") as f:
        data = json.load(f)
    return data


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        return {"return": result, "execution_time": total_time}

    return timeit_wrapper


def stars_and_bars(sums_to, array_len):
    return [tuple(k) for k in itertools.product(range(sums_to+1), repeat=array_len)if sum(k) == sums_to]


def list_stars_and_bars(sums_to_list, array_len):
    return list(itertools.product(*[stars_and_bars(s, array_len) for s in sums_to_list]))


def edit_tuple(input_tuple, index_list, value, edit=None):
    x = list(input_tuple)
    if len(index_list) == 1:
        if edit == "-":
            x[index_list[0]] -= value
        elif edit == "+":
            x[index_list[0]] += value
        else:
            x[index_list[0]] = value
    else:
        x[index_list[0]] = edit_tuple(x[index_list[0]], index_list[1:], value, edit)
    return tuple(x)


def save_to_csv(path, list_to_csv):
    if not isinstance(list_to_csv[0], str):
        buff_list = [str(i) for i in list_to_csv]
    else:
        buff_list = list_to_csv
    if os.path.exists(path):
        with open(path, "a") as f:
            f.write("\n" + "\n".join(buff_list))
    else:
        with open(path, "w") as f:
            f.write("\n".join(buff_list))


