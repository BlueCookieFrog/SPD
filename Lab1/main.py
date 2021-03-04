from generator import RandomNumberGenerator as generator

print("Seed: ")
seed = int(input())
print("Rozmiar: ")
n = int(input())

print(f"n: {10}")

rng = generator(seed)
nr = []
prepare_time = []   #r
work_time = []      #p
A = 0

for x in range(n):
    #lista indeksów
    nr.append(x+1)
    work_time.append(rng.nextInt(1, 29))

A = sum(work_time)
for _ in range(n):
    prepare_time.append(rng.nextInt(1, A))

print(f"nr: {nr}")
print(f"r: {prepare_time}")
print(f"p {work_time}")