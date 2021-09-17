from itertools import combinations 

def combos(set, num):
    combs = []
    for i in range(2** len(set)): 
        temp = str(bin(i))[::-1]
        print(temp)
        split_temp = temp.split()
    
        index = []
        for j in range(len(split_temp)):
            if(split_temp[j] == "1") :
                index.append[j]
        if len(index) == num:
            strTemp = ""
            for k in index:
                strTemp += set[k]
            combs.append(strTemp)
    print(combs)
    return combs

set = input()
strings = set.split(" ")

for i in range (0, len(strings) + 1):
    for element in combos(strings, i):
        print(element)


#[a b c d e]
# 0 0 0 0 0





