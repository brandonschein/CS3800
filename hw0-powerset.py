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
if(len(element_arr) != 1):
    element_arr.append("")
   
for x in range (0, len(element_arr)):
    print(" ".join(element_arr[x]))
