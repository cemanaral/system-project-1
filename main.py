# Cem Anaral 150119761


INPUT_FILE = "input.txt"

# Lambda functions for evaluation
isUnsignedInt = lambda line: 'u' in line
isFloat       = lambda line: '.' in line


def evaluate(line):
    if isUnsignedInt(line):
        print("Unsigned int: ", end='')
    
    elif isFloat(line):
        print("Float: ", end='')
    
    # Else, signed int
    else: 
        print("Signed int: ", end='')
    
    print(line)



def readFile():
    """Reads INPUT_FILE"""
    with open(INPUT_FILE) as file:
        for line in file:
            evaluate(line)


def main():
    readFile()    

if __name__ == '__main__':
    main()
