letters = input()

output_string = ""
outputs = []

#3 ^ alphabet number of combonations
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

for i in outputs:
    print(i)

