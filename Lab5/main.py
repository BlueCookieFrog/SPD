import math

from numpy import maximum
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

        self.data = [[None for _ in range(2)] for _ in range(self.n)]

    def generate_instance(self) -> None:
        # for i, each in enumerate(self.data):
        #     # Index
        #     each[0] = i + 1
        #     # Number of operations
        #     each[1] = 1 +self.__rng.nextInt( 1, math.floor(float(m) * 1.2))

        #     each[2] = []
        #     for _ in range(each[1]):
        #         # Performed times
        #         each[2].append(self.__rng.nextInt(1, 29))

        # for each in self.data:
        #     each[3] = []
        #     for _ in range(each[1]):
        #         # Generating machine assigned to task (μ)
        #         each[3].append(self.__rng.nextInt(1, self.m))

        #For NEH

        for i, each in enumerate(self.data):
            each[0] = i + 1
            each[1] = []
            for j in range(self.m):
                each[1].append(self.__rng.nextInt(1, 29))

    def print_instance(self) -> None:
        # print(self.data)
        df = pd.DataFrame(self.data)
        df = df.transpose()
        df.index = ["pi:", "p:"]
        df.columns = ["" for _ in range(self.n)]

        print(df, "\n")

def print_result(data) -> None:
        # print(self.data)

        s =  Schedule(data)
        _, C = s.generate_schedule()
        df = pd.DataFrame(data+C)
        df = df.transpose()
        df.index = ["pi:", "p:", "C"]
        df.columns = ["" for _ in range(self.n)]

        print(df, "\n")
        print(f"Cmax: {s.C_max()}")

class Schedule:
    def __init__(self, data) -> None:
        self.data = data
        print(self.data)

    def generate_schedule(self) -> None:

        self.S = [[0 for _ in range(len(self.data[i][1]))] for i in range(len(self.data))]
        self.C = [[0 for _ in range(len(self.data[i][1]))] for i in range(len(self.data))]

        last_start = 0

        for task in range(len(self.data)):
            for mach in range(len(self.data[task][1])):
                # last_start = self.S[task][mach] = last_fin
                if task == 0 and mach == 0:
                    pass
                elif task == 0:
                    last_start = self.S[task][mach] = self.C[task][mach-1]
                elif mach == 0:
                    last_start = self.S[task][mach] = self.C[task-1][mach]
                else:
                    last_start = self.S[task][mach] = max(self.C[task][mach-1], self.C[task-1][mach])
                self.C[task][mach] = last_start + self.data[task][1][mach]

        return self.S,self.C

    def C_max(self):
        return max(self.C, key = lambda x: x[-1])[-1]

def C_max(dat):
    Sch = Schedule(dat)
    Sch.generate_schedule()
    return Sch.C_max()


def NEH(inst: Instance):
    N = inst.data
    k = 1
    W = []
    # for i, each in enumerate(N):
    #     W.append([i,each])

    for each in N:
        W.append(each)

    W.sort(key=lambda x: sum(x[1]))

    pi_p = []
    pi_s = []
    while len(W) != 0:
        j = W.pop()
        for l in range(k):
            pi_p.insert(l, j)
            try:
                if C_max(pi_p) < C_max(pi_s):
                    pi_s = pi_p
            except ValueError:
                pi_s = pi_p
        pi_p = pi_s
        k += 1

    return pi_p



if __name__ == "__main__":
    seed = input("Seed: ")
    n, m = input("Size (n x m): ").split("x")
    inst = Instance(seed, m, n)
    inst.generate_instance()

    inst.print_instance()

    result = NEH(inst)

    print_result(result)
