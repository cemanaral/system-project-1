# Cem Anaral 150119761

# Global variables to reduce boilerplate parameters
INPUT_FILE     = "input.txt"     # Name of the input file which will be taken as input
OUTPUT_FILE    = "output.txt"
INT_SIZE       = 2               # Default size for integers is 2 bytes
INT_SIZE_BITS  = INT_SIZE * 8    # Integer size in bits

# Lambda functions for typechecks
is_unsigned    = lambda line: 'u' in line
is_float       = lambda line: '.' in line
is_big_end     = lambda symbol: symbol == 'b'
is_little_end  = lambda symbol: symbol == 'l'
is_negative    = lambda number: number[0] == '-'

# Converts big endian hexadecimal to little endian
big_to_little  = lambda big: ' '.join(big.split()[::-1]) 

def unsigned_to_binary(number: str):
    """Converts base-10 unsigned int to binary"""   
    binary = ''
    decimal = int(number.rstrip('u\n'))
    
    # Conversion algorithm
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
    

def take_complement(binary_list: str):
    """Takes complement of binary number"""
    for i in range(len(binary_list)):
        bit = binary_list[i]
        if bit == '0':
            binary_list[i] = '1'
        else:
            binary_list[i] = '0'



def increment(binary_list: list):
    """Increments binary number"""
    
    # Starts from rightmost and loops until including first element
    for i in range(len(binary_list)-1, -1, -1):
        bit = binary_list[i]
        if bit == '1':
            binary_list[i] = '0'
        else: # if 0
            binary_list[i] = '1'
            break




def signed_to_binary(number: str):
    """Converts base-10 signed int to binary (two's complement) using 'Subtract Powers of Two' method"""

    binary_list = ['0'] * (INT_SIZE_BITS)
    decimal = int(number.strip())
    magnitude = -decimal if is_negative(number) else decimal # Find magnitude of decimal number
    i = -1  # index

    # Keep dividing by two until answer is zero
    while magnitude != 0:
        remainder = magnitude % 2
        binary_list[i] = str(remainder)
        magnitude = int(magnitude // 2)
        i -= 1

    # if original number was negative, take complement and add 1
    if is_negative(number):
        take_complement(binary_list)
        increment(binary_list)    

    return ''.join(binary_list)


def fraction_to_binary(decimal_fraction: str) -> str:
    """Converts fraction to binary"""
    binary = ''
    value = float(decimal_fraction)
    
    is_not_zero = lambda value: int(str(value).split('.')[1]) != 0

    # while fraction part of value is not zero
    while is_not_zero(value):
        if str(value * 2)[0] == '1':
            binary = binary + '1' 
        else:
            binary = binary + '0'

        value = float('0.' + str(value * 2).split('.')[1])

    return binary

# BUG: does not work with negative numbers
def float_to_binary(decimal, float_size):
    float_size = 4 # for testing purposes

    whole, fraction = decimal.split('.')
    binary_whole = signed_to_binary(whole).lstrip('0')
    binary_fraction = fraction_to_binary('0.' + fraction)

    # to prevent decimals like 0.5 to become .5 after lstrip('0')
    if binary_whole == '':
        binary_whole = '0'
    
    # for negative floats, we need to skim the 1s
    # from left such that there will be only one 1
    if is_negative(decimal):
        binary_whole = binary_whole.lstrip('0')
        binary_whole = '1' + binary_whole.lstrip('1')


    raw_binary_float = [*binary_whole] + ['.'] + [*binary_fraction]
    
    # shifts the point
    # and finds exponent
    old_point_index = raw_binary_float.index('.')

    for i in range(len(raw_binary_float)):
        bit = raw_binary_float[i]
        if bit == '1':
            new_point_index = i + 1
            break
    
    exponent = old_point_index - new_point_index
    binary_exponent = signed_to_binary(str(exponent))
    print("exponent:", exponent)
    print("binary", binary_exponent)

    raw_binary_float.insert(new_point_index, '.')
    del raw_binary_float[old_point_index + 1]
    
    return ''.join(raw_binary_float)

def evaluate(line, byte_ordering, float_size, result_list):
    """Evaluates read line"""
    result = ''

    if is_unsigned(line):
        result = binary_to_hex(unsigned_to_binary(line))    
    
    elif is_float(line):
        result = float_to_binary(line, float_size)
    
    # Else, signed int
    else:
        result = binary_to_hex(signed_to_binary(line))
    
    if is_little_end(byte_ordering):
        result = big_to_little(result)
    
    result_list.append(result)



def binary_to_decimal(binary: str) -> int:
    """Converts binary to decimal"""
    exponent = len(binary) - 1
    decimal = 0

    for bit in binary:
        if bit == '1':
            decimal += 2 ** exponent
        exponent -= 1
    
    return decimal


def binary_to_hex(binary: str) -> str:
    """Converts binary number to hexadecimal"""
    hex_dict = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F' }   # Key: decimal, Value: hexadecimal
    result = ''

    # Split binary into 4 parts
    for i in range(0, len(binary), 4):
        substring = binary[i: i+4]
        decimal = binary_to_decimal(substring)
        
        # Conversion to hexadecimal
        if decimal > 9:
            hex_value = hex_dict[decimal]
        else:
            hex_value = str(decimal)
        result = result + hex_value
    
    # Adds spaces between every byte (2 hex characters)
    return ' '.join( [result[i: i+2] for i in range(0, len(result), 2)] )


def main():
    print("**Systems Programming Assignment 1**")
    print("Cem Anaral")
 
    byte_ordering = input("Please enter byte ordering type (l: little endian b: big endian)\n? ")
    float_size = int(input("Please enter float size in bytes (1, 2, 3, 4)\n? "))

    # Input checks
    if not is_little_end(byte_ordering) and not is_big_end(byte_ordering):
        raise ValueError("Invalid byte ordering type")
    if not (1 <= float_size <= 4):
        raise ValueError("Invalid float size")

    # Evaluation results will be appended to this list
    # which will be later used for output.txt
    result_list = []

    # Reads INPUT_FILE
    with open(INPUT_FILE, 'r') as file:
        for line in file:
            evaluate(line, byte_ordering, float_size, result_list)

    # Writes results to OUTPUT_FILE
    with open(OUTPUT_FILE, 'w') as file:
        for result in result_list:
            file.write(result + '\n')

    print(result_list)

if __name__ == '__main__':
    main()
