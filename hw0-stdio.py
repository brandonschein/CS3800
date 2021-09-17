try:
    string = input()
except EOFError:
    string = ""
except:
    print("invalid input")
for i in range(3):
    print(string)
