import math
from generator import RandomNumberGenerator as Generatotr
import pandas as pd
import itertools
import time
import functools


def timefunc(func):
    @functools.wraps(func)
    def time_closure(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        time_elapsed = time.perf_counter() - start
        print(f"Function: {func.__name__}, Time: {time_elapsed}s")
        return result

    return time_closure


class Instance:
    def __init__(self, seed, m, n: int) -> None:
        # Instance of rng class
        self.__rng = Generatotr(int(seed))

        # Number of tasks
        self.n = int(n)
        # Number of machines
        self.m = int(m)

        self.data = [[0 for _ in range(4)] for _ in range(self.n)]

    def generate_instance(self) -> None:
        for x, each in enumerate(self.data):
            # Index
            each[0] = x + 1
            # Number of operations
            each[1] = self.__rng.nextInt(1, math.floor(float(m) * 1.2))

            each[2] = []
            for _ in range(each[1]):
                # Performed times
                each[2].append(self.__rng.nextInt(1, 29))

        for each in self.data:
            each[3] = []
            for _ in range(each[1]):
                # Generating machine assigned to task (μ)
                each[3].append(self.__rng.nextInt(1, self.m))

    def print_instance(self) -> None:
        # print(self.data)
        df = pd.DataFrame(self.data)
        df = df.transpose()
        df.index = ["pi:", "o:", "p:", "μ:"]
        df.columns = ["" for _ in range(self.n)]

        print(df, "\n")


if __name__ == "__main__":
    seed = input("Seed: ")
    n, m = input("Size (n x m): ").split("x")
    inst = Instance(seed, m, n)
    inst.generate_instance()

    inst.print_instance()
