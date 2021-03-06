import math
from typing import Generator
from generator import RandomNumberGenerator as Generator
import pandas as pd
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
        self.__rng = Generator(int(seed))

        # Number of tasks
        self.n = int(n)
        # Number of machines
        self.m = int(m)

        self.data = [[None for _ in range(2)] for _ in range(self.n)]

    def generate_instance(self) -> None:

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

    s = Schedule(data)
    _, C = s.generate_schedule()

    result = [[i[0], C_each] for i, C_each in zip(data, C)]
    df = pd.DataFrame(result)
    df = df.transpose()
    df.index = ["pi:", "C"]
    df.columns = ["" for _ in range(len(result))]

    print(df, "\n")
    print(f"Cmax: {s.C_max()}")


class Schedule:
    def __init__(self, data) -> None:
        self.data = data

    def generate_schedule(self) -> None:

        self.S = [
            [0 for _ in range(len(self.data[i][1]))] for i in range(len(self.data))
        ]
        self.C = self.S.copy()

        last_start = 0

        for task in range(len(self.data)):
            for mach in range(len(self.data[task][1])):
                # handling edge cases
                if task == 0 and mach == 0:
                    # leaves 0 as strat time for firs task on first machine
                    pass
                elif task == 0:
                    # fist task on machine
                    last_start = self.S[task][mach] = self.C[task][mach - 1]
                elif mach == 0:
                    # task on first machine
                    last_start = self.S[task][mach] = self.C[task - 1][mach]
                else:
                    last_start = self.S[task][mach] = max(
                        self.C[task][mach - 1], self.C[task - 1][mach]
                    )

                self.C[task][mach] = last_start + self.data[task][1][mach]

        return self.S, self.C

    def C_max(self):
        return max(self.C, key=lambda x: x[-1])[-1]


def C_max(dat):
    Sch = Schedule(dat)
    Sch.generate_schedule()
    return Sch.C_max()


def NEH_plus_4(data, current):

    pi = data.copy()
    best = []

    for each in pi:
        if each != current:
            i = pi.index(each)
            pi.pop(i)
            try:
                if C_max(pi) < best[0]:
                    best = [C_max(pi), each]
            except IndexError:
                best = [C_max(pi), each]

        pi = data.copy()

    if len(data) > 1:
        W = []
        W = pi.copy()
        # print(best)
        i = pi.index(best[1])
        W.pop(i)

        pi_s = []
        pi_p = []

        j = best[1]

        for l in range(len(W) + 1):
            pi_p = W.copy()
            pi_p.insert(l, j)
            # print(f"NEH+ {[each[0] for each in pi_p]}")
            # print(f"C_max: {C_max(pi_p)}")
            try:
                if C_max(pi_p) < C_max(pi_s):
                    pi_s = pi_p.copy()
            except ValueError:
                # handles first chceck when pi_s is empty
                pi_s = pi_p.copy()

        pi_p = pi_s.copy()
        # print(f"NEH+ best: {[each[0] for each in pi_p]}")
        # print(f"NEH+ Cmax: {C_max(pi_p)}\n")
    else:
        pi_p = pi

    return pi_p

@timefunc
def NEH(inst: Instance):
    N = inst.data
    k = 1
    W = []

    W = N.copy()

    W.sort(key=lambda x: sum(x[1]))

    pi_p = []
    pi_p2 = []
    pi_s = []
    while len(W) != 0:
        j = W.pop()

        for l in range(k):
            pi_p2 = pi_p.copy()
            pi_p2.insert(l, j)
            # print([each[0] for each in pi_p2])
            try:
                if C_max(pi_p2) < C_max(pi_s):
                    pi_s = pi_p2.copy()
            except ValueError:
                # handles first chceck when pi_s is empty
                pi_s = pi_p2.copy()

        # print(f"best: {[each[0] for each in pi_s]}")
        # print(f"Cmax: {C_max(pi_s)}\n")
        pi_p = NEH_plus_4(pi_s, j)

        pi_s = []
        k += 1

    return pi_p

@timefunc
def simulated_annealing(inst: Instance, seed, epoch = 5):
    rng = Generator(int(seed))

    N = inst.data
    # greedy
    N.sort(key= lambda x: sum(x[1]))

    T = 1550.0
    Tend = 20.0

    L=int(epoch)

    pi = []
    pi_new = []
    pi_s = []

    it = 0

    for each in N:
        pi.append(each)
        pi_s.append(each)

    while T > Tend:
        for _ in range(L):
            i = rng.nextInt(0, len(N)-1)
            j = rng.nextInt(0, len(N)-1)
            pi_new = pi
            pi_new[i], pi_new[j] = pi_new[j], pi_new[i]

            C_max_new = C_max(pi_new)
            C_max_old = C_max(pi)

            if C_max_new > C_max_old:
                r = rng.nextFloat(0,1)
                delta = C_max_old-C_max_new
                if r >= math.exp(delta/T):
                    pi_new = pi

            pi = pi_new

            if C_max(pi) <  C_max(pi_s):
                pi_s = pi

        it += 1
        T = T / math.log(it+1)

    return pi_s

@timefunc
def tabu_search(inst: Instance, cadance = 5, itLimit = 1000):
    N = inst.data
    # greedy
    N.sort(key= lambda x: sum(x[1]))

    tabu = [[0 for _ in range(len(N))] for _ in range(len(N))]

    pi = []
    pi_new = []
    pi_s = []

    cadance = int(cadance)

    J = 0
    K = 0

    for each in N:
        pi.append(each)
        pi_s.append(each)

    for it in range(itLimit):
        c_best = math.inf
        for j in range(len(N)):
            for k in range(j+1, len(N)):
                if tabu[j][k] < it:
                    pi_new = pi
                    pi_new[j], pi_new[k] = pi_new[k], pi_new[j]

                    c_max_new = C_max(pi_new)
                    if c_max_new < c_best:
                        c_best = c_max_new
                        J = j
                        K = k

        pi[J], pi[K] = pi[K], pi[J]

        tabu[J][K] = it + cadance
        tabu[K][J] = tabu[J][K]

        if C_max(pi) < C_max(pi_s):
            pi_s = pi

    return pi_s


if __name__ == "__main__":
    seed = input("Seed: ")
    n, m = input("Size (n x m): ").split("x")
    inst = Instance(seed, m, n)
    inst.generate_instance()

    print("Instancja:")
    inst.print_instance()

    result = NEH(inst)
    print("NEH:")
    print_result(result)
    print("\n")

    result = simulated_annealing(inst, 20, 2*int(n))
    print("Symulowane Wyżarzanie:")
    print_result(result)
    print("\n")


    result = tabu_search(inst, n)
    print("Przeszukiwanie z Zabronieniami:")
    print_result(result)