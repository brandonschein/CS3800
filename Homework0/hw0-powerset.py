# NOTE: I remember using this library in a high school programming class to 
# build a powerset and our teacher had us use a function to produce them so we could
# experiment in class. 
#import to help me build the powerset
from itertools import combinations 

#accounting for empty string/invalid input
try:
    set = input()
except EOFError:
    set = ""
except:
    print("invalid input")

strings = set.split(" ")

#instantiating the array to add the elements too for printing
element_arr = []

#using the combinations from itertools to create the powerset
for i in range (1, len(strings) + 1):
    for element in combinations(strings, i):
        #adding each combo to the element array 
        element_arr.append(element)

#dealing with the empty case 
if(len(element_arr) != 1):
    element_arr.append("")
   
#printing the array 
for x in range (0, len(element_arr)):
    print(" ".join(element_arr[x]))
