import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import os

NQUBITS = 8
ROUNDS = 12
KEY1_INDEX = [3, 1, 6, 0, 5, 4, 7, 2]
PERMUTATION = [5, 2, 7, 0, 3, 1, 4, 6]
RXZ_INTERACTION = [(0, 3), (4, 5), (7, 2), (1, 6)]

secret = os.urandom(ROUNDS+1)

def encrypt(pt):
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

v0 = encrypt(0)
v1 = encrypt(1)
v2 = encrypt(2)

print("Max amplitude of v0:", np.max(np.abs(v0)))
print("Index of max amplitude of v0:", np.argmax(np.abs(v0)))

print("Max amplitude of v1:", np.max(np.abs(v1)))
print("Index of max amplitude of v1:", np.argmax(np.abs(v1)))

print("Max amplitude of v2:", np.max(np.abs(v2)))
print("Index of max amplitude of v2:", np.argmax(np.abs(v2)))
