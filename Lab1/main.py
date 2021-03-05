from generator import RandomNumberGenerator as generator


def generate_instance(seed, n):
    rng = generator(seed)

    data = [[0 for x in range(3)] for _ in range(n)]

    A = 0
    for x in range(n):
        data[x][0] = x + 1
        data[x][2] = rng.nextInt(1, 29)
        A += data[x][2]

    for y in range(n):
        data[y][1] = rng.nextInt(1, A)

    nr, r, p = [], [], []

    for z in range(n):
        nr.append(data[z][0])
        r.append(data[z][1])
        p.append(data[z][2])
    print(f"nr: {nr}")
    print(f"r: {r}")
    print(f"p: {p}\n")

    return data


def solution(data):

    start_times = []
    finish_times = []
    last_fin = 0

    for x in range(len(data)):
        start_times.append(max((data[x][1], last_fin)))
        finish_times.append(start_times[x] + data[x][2])
        last_fin = finish_times[x]

    pi, S, C = [], [], []

    for z in range(len(data)):
        pi.append(data[z][0])
        S.append(start_times[z])
        C.append(finish_times[z])
    print(f"pi: {pi}")
    print(f"S: {S}")
    print(f"C: {C}\n")


if __name__ == "__main__":
    seed = int(input("Seed: "))
    n = int(input("Rozmiar: "))

    print(f"\nn: {n}\n")

    data = generate_instance(seed, n)

    #solution for natural permutation
    solution(data)

    #solution for data sorted by r
    data_sorted = sorted(data, key = lambda x: x[1])

    solution(data_sorted)