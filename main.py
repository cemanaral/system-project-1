# Cem Anaral 150119761


INPUT_FILE = "input.txt"

# Lambda functions for checks
isUnsignedInt = lambda line: 'u' in line
isFloat       = lambda line: '.' in line
isBigEnd      = lambda symbol: symbol == 'b'
isLittleEnd   = lambda symbol: symbol == 'l'


def evaluate(line):
    if isUnsignedInt(line):
        print("Unsigned int: ", end='')
    
    elif isFloat(line):
        print("Float: ", end='')
    
    # Else, signed int
    else: 
        print("Signed int: ", end='')
    
    print(line)


def main():
    print("Systems Programming Assignment 1")
 
    byte_ordering = input("Please enter byte ordering type (l: little endian b: big endian)\n? ")

    # If input is invalid
    if not isLittleEnd(byte_ordering) and not isBigEnd(byte_ordering):
        raise ValueError("Invalid byte ordering type")


    # Reads INPUT_FILE
    with open(INPUT_FILE) as file:
        for line in file:
            evaluate(line)


if __name__ == '__main__':
    main()
