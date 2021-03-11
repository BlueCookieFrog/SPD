from generator import RandomNumberGenerator as generator


def generate_instance(seed, n, max_q):
    # initiating class object with seed
    rng = generator(seed)

    # 2D list (list of n 4-item lists [[0, 0, 0, 0], [0, 0, 0, 0]...])
    data = [[0 for _ in range(4)] for _ in range(n)]

    # Sum of all execution times
    A = 0
    for x in range(n):
        # indexes
        data[x][0] = x + 1
        # generating execution times
        data[x][2] = rng.nextInt(1, 29)
        # summing execution times
        A += data[x][2]

    for y in range(n):
        # generating preparation times
        data[y][1] = rng.nextInt(1, A)

    for z in range(n):
        # generating preparation times
        if max_q == "A":
            data[z][3] = rng.nextInt(1, A)
        else:
            data[z][3] = rng.nextInt(1, max_q)

    # lists to make printing data easier
    nr, r, p, q = [], [], [], []

    for z in range(n):
        nr.append(data[z][0])
        r.append(data[z][1])
        p.append(data[z][2])
        q.append(data[z][3])
    print(f"nr: {nr}")
    print(f"r: {r}")
    print(f"p: {p}")
    print(f"q: {q}\n")

    # return data to allow its further processing
    return data


def schrage(data):
    """Schrage algorythm

    almost good, but 9 and 1 are flipped
    """
    G = []
    N = sorted(data, key=lambda x: x[1])
    t = N[0][1]
    pi = []
    max_q = []

    while (len(G) != 0) or (len(N) != 0):
        while (len(N) != 0) and (N[0][1] <= t):
            G.append(N[0])
            N.pop(0)
        if len(G) != 0:
            max_q = sorted(G, key=lambda x: x[3])
            G.pop(G.index(max_q[len(max_q) - 1]))
            pi.append(max_q[len(max_q) - 1])
            t = t + max_q[len(max_q) - 1][2]
        else:
            N = sorted(N, key=lambda x: x[1])
            t = N[0]
    return pi


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
    print(f"Cq: {Cq}\n")
    print(f"Cmax = {max(Cq)}")


if __name__ == "__main__":
    seed = int(input("Seed: "))
    n = int(input("Rozmiar: "))

    print(f"\nn: {n}\n")

    # data = generate_instance(seed, n, 29)
    data = generate_instance(seed, n, "A")

    # solution for natural permutation
    solution(data)

    # solution for data sorted by r
    # data_sorted = sorted(data, key=lambda x: x[1])

    data_sorted = schrage(data)
    print(data_sorted)

    solution(data_sorted)
