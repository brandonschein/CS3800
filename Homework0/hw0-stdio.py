# using this try except block to deal with empty input case/invalid input
try:
    string = input()
except EOFError:
    string = ""
except:
    print("invalid input")

#prints the string 3 times
for i in range(3):
    print(string)
