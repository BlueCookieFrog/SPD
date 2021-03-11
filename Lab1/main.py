from generator import RandomNumberGenerator as generator


def generate_instance(seed, n):
    # initiating class object with seed
    rng = generator(seed)

    # 2D list (list of n 3-item lists [[0, 0, 0], [0, 0, 0]...])
    data = [[0 for _ in range(3)] for _ in range(n)]

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

    # lists to make printing data easier
    nr, r, p = [], [], []

    for z in range(n):
        nr.append(data[z][0])
        r.append(data[z][1])
        p.append(data[z][2])
    print(f"nr: {nr}")
    print(f"r: {r}")
    print(f"p: {p}\n")

    # return data to allow its further processing
    return data


def solution(data):

    # indexes
    pi = []
    # start times
    S = []
    # finish times
    C = []
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

    print(f"pi: {pi}")
    print(f"S: {S}")
    print(f"C: {C}\n")


if __name__ == "__main__":
    seed = int(input("Seed: "))
    n = int(input("Rozmiar: "))

    print(f"\nn: {n}\n")

    data = generate_instance(seed, n)

    # solution for natural permutation
    solution(data)

    # solution for data sorted by r
    data_sorted = sorted(data, key=lambda x: x[1])

    solution(data_sorted)
