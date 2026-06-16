from Crypto.Util.number import bytes_to_long
import string

def encrypt_blocks(pt):
    nqubits = 8
    bits = bin(bytes_to_long(pt))[2:]
    bits = bits.rjust((len(bits)//nqubits + 1)*nqubits, '0')
    blocks = [bits[i:i+nqubits] for i in range(0, len(bits), nqubits)]
    return blocks

print("b'T':", encrypt_blocks(b'T'))
print("b'TRX{':", encrypt_blocks(b'TRX{'))
