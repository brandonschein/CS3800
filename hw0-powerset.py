from itertools import combinations 

try:
    set = input()
except EOFError:
    set = ""
except:
    print("invalid input")

strings = set.split(" ")
    
element_arr = []

for i in range (1, len(strings) + 1):
    for element in combinations(strings, i):
        element_arr.append(element)

for x in range (0, len(element_arr)):
    print(" ".join(element_arr[x]))
