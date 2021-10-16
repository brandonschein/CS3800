import sys 
raw_input = sys.stdin.read()

S1 = raw_input.split(" ")

S2 = ["bat", "horse", "turtle", "fish", "squirrel", "bird"]

output_set = []

for i in S1:
    if (i not in S2):
        output_set.append(i)

output_string = ""

for i in output_set:
    output_string += i + " "

print(output_string)
