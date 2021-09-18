#using a try except block to account for empty input/invalid input
try:
    letters = input()
except EOFError:
    letters = ""
except:
    print("invalid argumenet")
output_string = ""
outputs = []

#3 ^ alphabet number of combonations *note to self* 
# these nested for loops will take care of building up the 
# output string one at a time. for instance the first loop would look
# like 0xx, and then the second 00x and the third 000, then strip away
# the last 0 so that it is 00x and go forward in the loop to get 001
for x in range(0, len(letters)):
    output_string += letters[x]
    for y in range(0, len(letters)):
        output_string += letters[y]
        
        for z in range (0, len(letters)):
            output_string += letters[z]
            outputs.append(output_string)
            output_string = output_string[:len(output_string)-1]

        output_string = output_string[:len(output_string)-1]
    output_string = ""

# now display the outputs in stdout
for i in outputs:
    print(i)

