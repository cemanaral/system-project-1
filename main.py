# Cem Anaral 150119761

# Global variables to reduce boilerplate parameters
INPUT_FILE     = "input.txt"     # Name of the input file which will be taken as input
INT_SIZE       = 2               # Default size for integers is 2 bytes
INT_SIZE_BITS  = INT_SIZE * 8    # Integer size in bits

# Lambda functions for checks
is_unsigned    = lambda line: 'u' in line
is_float       = lambda line: '.' in line
is_big_end     = lambda symbol: symbol == 'b'
is_little_end  = lambda symbol: symbol == 'l'



def unsigned_to_binary(number: str):
    """Converts base-10 unsigned int to binary"""   
    binary = ''

    # Conversion algorithm
    decimal = int(number.rstrip('u\n'))
    while decimal > 0:
        binary = str(decimal % 2) + binary
        decimal = int(decimal // 2)

    # If sizes are not equal adds zeros to left
    if len(binary) < INT_SIZE_BITS:
        left_zeros = (INT_SIZE_BITS - len(binary)) * '0'
        binary = left_zeros + binary
    # If input is bigger than UMax
    elif len(binary) > INT_SIZE_BITS:
        raise OverflowError(f"{number} can not be represented in {INT_SIZE} bytes.")

    return binary
    


def evaluate(line, byte_ordering, float_size):
    """Evaluates read line"""

    print("------------------------------------------------")
    if is_unsigned(line):
        print("Decimal Unsigned int:\t", line.strip())
        print("Binary Unsigned int:\t", unsigned_to_binary(line))
        
    
    elif is_float(line):
        print("Decimal Float:", line)
    
    # Else, signed int
    else:
        print("Decimal Signed int:", line)
    print("------------------------------------------------")
    


def main():
    print("Systems Programming Assignment 1")
 
    byte_ordering = input("Please enter byte ordering type (l: little endian b: big endian)\n? ")
    float_size = int(input("Please enter float size in bytes (1, 2, 3, 4)\n? "))

    # Input checks
    if not is_little_end(byte_ordering) and not is_big_end(byte_ordering):
        raise ValueError("Invalid byte ordering type")
    if not (1 <= float_size <= 4):
        raise ValueError("Invalid float size")

    # Reads INPUT_FILE
    with open(INPUT_FILE, 'r') as file:
        for line in file:
            evaluate(line, byte_ordering, float_size)


if __name__ == '__main__':
    main()
