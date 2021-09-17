from itertools import combinations 

set = input()
strings = set.split(" ")

for i in range (0, len(strings) + 1):
    for element in combinations(strings, i):
        print(" ".join(element))





