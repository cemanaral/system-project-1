from main import *

res = unsigned_to_binary("412u")
print(res)
assert len(res) == INT_SIZE_BITS
assert res == "0000000110011100"
