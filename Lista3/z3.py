import sys
# from functools import reduce


with open(sys.argv[1], "r") as f:
    sizes = [int(line.split()[-1]) for line in f]
    # sum = reduce(lambda acc, size: acc + size, sizes)
    print("Całkowita liczba bajtów:", sum(sizes))
