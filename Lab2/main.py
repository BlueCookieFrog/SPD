from generator import RandomNumberGenerator as Generatotr
import numpy as np


class Instance:
    def __init__(self, seed, n) -> None:
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
            self.data[x][2] = self.__rng.nextInt(1, 29)
            # summing execution times
            A += self.data[x][2]

        for y in range(self.__n):
            # generating preparation times
            self.data[y][1] = self.__rng.nextInt(1, A)

        for z in range(self.__n):
            # generating preparation times
            if max_q is None:
                self.data[z][3] = self.__rng.nextInt(1, A)
            else:
                self.data[z][3] = self.__rng.nextInt(1, max_q)

    def print_instance(self) -> None:

        temp = np.array(self.data)
        print(f"nr: {np.array2string(temp[:, 0], separator=', ')}")
        print(f"r:  {np.array2string(temp[:, 1], separator=', ')}")
        print(f"p:  {np.array2string(temp[:, 2], separator=', ')}")
        print(f"q:  {np.array2string(temp[:, 3], separator=', ')}\n")


class Schrage:
    def __init__(self, data) -> None:
        self.data = data
        self.pi = []

    def schrage(self) -> None:
        """
        Schrage algorythm.
        """
        G = []
        # sorted by
        N = sorted(self.data, key=lambda x: x[1])
        t = N[0][1]
        max_q = []

        while (len(G) != 0) or (len(N) != 0):
            while (len(N) != 0) and (N[0][1] <= t):
                G.append(N[0])
                N.pop(0)
            if len(G) != 0:
                max_q = sorted(G, key=lambda x: x[3])[-1]
                G.pop(G.index(max_q))
                self.pi.append(max_q)
                t = t + max_q[2]
            else:
                t = sorted(N, key=lambda x: x[1])[0][1]

    def print_instance(self) -> None:
        temp = np.array(self.pi)
        print(f"nr: {np.array2string(temp[:, 0], separator=', ')}")
        print(f"r:  {np.array2string(temp[:, 1], separator=', ')}")
        print(f"p:  {np.array2string(temp[:, 2], separator=', ')}")
        print(f"q:  {np.array2string(temp[:, 3], separator=', ')}\n")


def solution(data):

    # indexes
    pi = []
    # start times
    S = []
    # finish times
    C = []
    # finish and deliver time
    Cq = []
    # last finish time
    last_fin = 0

    # write indexes
    for z in range(len(data)):
        pi.append(data[z][0])

    # calculate S an C
    for x in range(len(data)):
        S.append(max((data[x][1], last_fin)))
        C.append(S[x] + data[x][2])
        last_fin = C[x]
        Cq.append(C[x] + data[x][3])

    print(f"pi: {pi}")
    print(f"S: {S}")
    print(f"C: {C}")
    print(f"Cq: {Cq}")
    print(f"Cmax = {max(Cq)}\n")


if __name__ == "__main__":
    seed = int(input("Seed: "))
    n = int(input("Rozmiar: "))

    Rng = Instance(seed, n)

    # Rng.generate_instance(29)
    Rng.generate_instance()
    Rng.print_instance()

    schr = Schrage(Rng.data)
    schr.schrage()
    schr.print_instance()

    solution(schr.pi)
