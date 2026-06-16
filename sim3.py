import numpy as np

# Let's inspect the SAME blocks in the real ciphertext
same_blocks = {1: [8, 33], 4: [9, 30, 34], 5: [11, 25, 29], 7: [10, 19, 24, 32], 8: [33], 9: [30, 34], 10: [19, 24, 32], 11: [25, 29], 12: [31, 35], 13: [23, 27], 14: [17, 22], 15: [28], 17: [22], 19: [24, 32], 23: [27], 24: [32], 25: [29], 30: [34], 31: [35]}

# Block 0: 'T'
# Block 1: 'R' -> same as 8, 33
# Block 2: 'X'
# Block 3: '{'
# Block 37: '}'? It's the last block, length is 38.
# Let's verify block 37 is '}'
