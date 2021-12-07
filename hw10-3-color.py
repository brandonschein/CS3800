#!/usr/bin/env python3
import sys 

edges = []
graph = {}

def populate_edges(m, input_arr):
    for i in range(1, m + 1):
        edges.append(input_arr[i].split(" "))
        
def populate_graph(coloring):
    for i in range(len(coloring)):
        graph[i + 1] = int(coloring[i])

def checkvalid():
    for node in graph:
        temp_seen = set()
        temp_seen.add(graph[node])
        for e in edges:
            if(int(e[0]) == node):
                prev_length = len(temp_seen)
                temp_seen.add(graph[int(e[1])])
                if(prev_length == len(temp_seen)):
                    return False
    return True
        

###################
input_arr = sys.stdin.read().split("\n ")

input_arr[len(input_arr) - 1] = input_arr[len(input_arr) - 1].split("\n")[0]

#print(input_arr)

n, m = input_arr[0].split(" ")
n = int(n)
m = int(m)

populate_edges(m, input_arr)
#print(edges)

populate_graph(input_arr[len(input_arr) - 1].split())
#print(graph)

if(checkvalid()):
    print(1)
else:
    print(0)

