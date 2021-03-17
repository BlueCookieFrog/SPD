from generator import RandomNumberGenerator as Generatotr
import numpy as np


class Instance:
    def __init__(self, seed, n) -> None:
        self.__rng = Generatotr(seed)
        self.data = np.array([[0 for _ in range(4)] for _ in range(n)])
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

        print(f"nr: {np.array2string(self.data[:, 0], separator=', ')}")
        print(f"r:  {np.array2string(self.data[:, 1], separator=', ')}")
        print(f"p:  {np.array2string(self.data[:, 2], separator=', ')}")
        print(f"q:  {np.array2string(self.data[:, 3], separator=', ')}\n")


def schrage(data) -> list:
    """
        Schrage algorythm.
    """
    G = []
    # sorted by
    N = sorted(data, key=lambda x: x[1])
    t = N[0][1]
    pi = []
    max_q = []

    while (len(G) != 0) or (len(N) != 0):
        while (len(N) != 0) and (N[0][1] <= t):
            G.append(N[0])
            N.pop(0)
        if len(G) != 0:
            max_q = sorted(G, key=lambda x: x[3])[-1]
            print(sorted(G, key=lambda x: x[3]))
            G.pop(G.index(max_q))
            pi.append(max_q)
            t = t + max_q[2]
        else:
            t = sorted(N, key=lambda x: x[1])[0]
    return pi


if __name__ == "__main__":
    seed = int(input("Seed: "))
    n = int(input("Rozmiar: "))

    Rng = Instance(seed, n)

    # Rng.generate_instance(29)
    Rng.generate_instance()
    Rng.print_instance()

    schrage(Rng.data)
