import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import os

NQUBITS = 8
ROUNDS = 12
KEY1_INDEX = [3, 1, 6, 0, 5, 4, 7, 2]
PERMUTATION = [5, 2, 7, 0, 3, 1, 4, 6]
RXZ_INTERACTION = [(0, 3), (4, 5), (7, 2), (1, 6)]

def encrypt(pt, secret):
    state_string = bin(pt)[2:].rjust(8, '0')[::-1] + bin(secret[0])[2:].rjust(8, '0')[::-1]
    qc = QuantumCircuit(16)
    for i, b in enumerate(state_string):
        if b == '1':
            qc.x(i)

    for round in range(ROUNDS):
        for i in range(NQUBITS):
            qc.cry(np.pi/15, NQUBITS+KEY1_INDEX[i], i)
        for i in range(NQUBITS):
            qc.iswap(PERMUTATION[i], PERMUTATION[(i+1)%NQUBITS])
        for i in range(len(RXZ_INTERACTION)):
            qc.rzx(np.pi/np.e, RXZ_INTERACTION[i][0], RXZ_INTERACTION[i][1])

        bit_prev = bin(secret[round])[2:].rjust(8, '0')
        bit_new = bin(secret[round+1])[2:].rjust(8, '0')
        for i in range(8):
            if bit_prev[-i-1] != bit_new[-i-1]:
                qc.x(NQUBITS+i)

    ct_c = Statevector(qc).data
    index_ct = secret[-1]*256
    return ct_c[index_ct:index_ct+256]

secret1 = os.urandom(ROUNDS+1)

# Is the whole 256 vector the same if we just shift it? Wait, `index_ct` selects 256 amplitudes from 65536 amplitudes!
# Wait! secret[-1]*256 means we select a block of 256 amplitudes.
# There are 2^16 = 65536 amplitudes.
# secret[-1] is a byte (0-255).
# So we are just selecting one of the 256 blocks of 256 amplitudes!
# And this selection depends on secret[-1].


# Wait... the server generated ONE secret per connection!
# No, wait!
# class QCipher():
#     def __init__(self, nqubits, rounds):
#         ...
#         self.secret = urandom(self.rounds+1)
#
# def main():
#     ...
#     qcipher = QCipher(NQUBITS, ROUNDS)
#     while True:
#         ...
#
# Oh, `qcipher` is created ONCE per connection!
# So `secret` is FIXED per connection!
# BUT when we encrypt multiple times in ONE connection, the secret is the SAME!
# "if option == '1': ... ct = qcipher.encrypt(pt)"
# BUT queries_left = MAX_QUERIES = 1 !!!
# We can only use option 1 ONCE per connection!
# So we can encrypt 1 byte, and then we have to disconnect. Next connection will have a NEW secret!
# Option 2 (Get Encrypted Flag) can be used ANY number of times?
# "if option == '2': ct = qcipher.encrypt(FLAG); print(ct)"
# Yes! Option 2 doesn't decrement queries_left!
# So in ONE connection, we can:
# 1. Encrypt our chosen byte.
# 2. Get the encrypted flag.
# And they will share the SAME secret!

# Let's verify this theory by reading my previous test!
