#!/usr/bin/env python3
import sys 

def calculate_square(a, b):
    if b < 0:
        return calculate_square(1/a, -b)
    elif b == 0:
        return 1
    elif b == 1:
        return a
    elif b % 2 == 0:
        return calculate_square(a * a, b/2)
    elif b % 2 == 1:
        return a * calculate_square(a * a, (b - 1)/2)



######################

a, b, c, p = input().split(" ")
a = int(a)
b = int(b)
c = int(c)
p = int(p)

square = calculate_square(a, b)

if(square % p == c % p):
    print(1)
else:
    print(0)
