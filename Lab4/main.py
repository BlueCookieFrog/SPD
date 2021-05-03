from generator import RandomNumberGenerator as Generatotr
import pandas as pd
import itertools
import time
import functools


def timefunc(func):
    """timefunc's doc"""

    @functools.wraps(func)
    def time_closure(*args, **kwargs):
        """time_wrapper's doc string"""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        time_elapsed = time.perf_counter() - start
        print(f"Function: {func.__name__}, Time: {time_elapsed}s")
        return result

    return time_closure


class Instance:
    def __init__(self, seed, n: int) -> None:
        self.__rng = Generatotr(seed)
        # 2D list (list of n 4-item lists [[0, 0, 0, 0], [0, 0, 0, 0]...])
        # self.data = np.zeros((4, n), dtype = int)
        self.data = [[0 for _ in range(4)] for _ in range(n)]
        self.__n = n

    def generate_instance(self, max_q=None) -> None:
        A = 0
        for x in range(self.__n):
            # indexes
            self.data[x][0] = x + 1
            # generating execution times
            self.data[x][1] = self.__rng.nextInt(1, 29)
            # summing execution times
            A += self.data[x][1]

        for y in range(self.__n):
            # generating weights
            self.data[y][2] = self.__rng.nextInt(1, 9)

        for z in range(self.__n):
            # generating deadlines
            if max_q is None:
                self.data[z][3] = self.__rng.nextInt(1, A)
            else:
                self.data[z][3] = self.__rng.nextInt(1, max_q)

    def print_instance(self) -> None:

        df = pd.DataFrame(self.data)
        df = df.transpose()
        df.index = ["pi:", "p:", "w:", "d:"]
        df.columns = ["" for _ in range(self.__n)]

        print(df, "\n")


def generate_schedule(inst: Instance, permutation: list) -> list:
    """Generates Schedule form instance based on given permutation

    Parameters
    ----------
    inst : Instance
        Given data
    permutation : list
        List with order of tasks

    Returns
    -------
    list
        Generated schedule
    """
    n = len(inst)
    schedule = [[0 for _ in range(5)] for _ in range(n)]

    j = 0
    last_start = 0
    last_finish = 0
    for i in permutation:
        # pi
        schedule[j][0] = i
        # start time
        last_start = schedule[j][1] = last_finish
        # completion time
        last_finish = schedule[j][2] = last_start + inst[i - 1][1]
        # time past deadline
        schedule[j][3] = max(schedule[j][2] - inst[i - 1][3], 0)
        # weighted time
        schedule[j][4] = inst[i - 1][2] * schedule[j][3]
        j += 1

    return schedule


def penalty(schedule: list) -> int:
    """ Calcuates penalty for given schedule """
    pen = 0
    for each in schedule:
        # time past deadline
        pen += each[4]
    return pen

""" Brute Force """

@timefunc
def brute_force(inst: Instance) -> list:
    """Brute Force algorythm that gets permutation with the lowest penalty

    Parameters
    ----------
    inst : Instance

    Returns
    -------
    list
        Returns list that contains best permutation and its penalty
    """
    best = []
    permutations_base = list(range(1, len(inst) + 1))
    for each in itertools.permutations(permutations_base):
        schedule = generate_schedule(inst, each)
        pen = penalty(schedule)

        try:
            best = min(best, [each, pen], key=lambda x: x[1])
        except IndexError:
            best = [each, pen]

    return best


def brute_force_main(inst: Instance) -> list:
    # result = [<permutation: list>, penalty]
    result = brute_force(inst)
    schedule = generate_schedule(inst, result[0])

    return schedule

""" Greedy """

@timefunc
def greedy(inst: Instance) -> list:
    return sorted(inst, key=lambda x: x[3])


def greedy_main(inst: Instance) -> list:
    result = greedy(inst)
    permutation = [int(each[0]) for each in result]
    schedule = generate_schedule(inst, permutation)

    return schedule


def setup() -> Instance:
    seed = int(input("Seed: "))
    n = int(input("Liczba maszyn: "))
    inst = Instance(seed, n)

    inst.generate_instance(max_q=29)
    return inst


def print_schedule(schedule: list) -> None:
    # Prints schedule using pandas DataFrame
    df = pd.DataFrame(schedule)
    df = df.transpose()
    df.index = ["pi:", "S:", "C:", "T:", "WT:"]
    df.columns = ["" for _ in range(len(schedule))]

    print(df)
    print(f"WT sum: {penalty(schedule)}\n")


def main():

    inst = setup()

    inst.print_instance()

    BF = brute_force_main(inst.data)
    print_schedule(BF)

    greed = greedy_main(inst.data)
    print_schedule(greed)


if __name__ == "__main__":

    main()
