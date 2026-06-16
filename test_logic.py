import socket
import ast
import numpy as np

def get_mapping_for_char(char):
    s = socket.socket()
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))

    # Read banner
    while b'>' not in s.recv(4096):
        pass

    # Option 1: encrypt char
    s.send(b'1\n')
    s.send(f"{ord(char):02x}\n".encode())

    res1 = b""
    while b']' not in res1:
        res1 += s.recv(4096)

    start = res1.find(b'[')
    end = res1.find(b']') + 1
    list_str = res1[start:end].replace(b'np.complex128', b'complex')
    ct_char = eval(list_str.decode('utf-8', errors='ignore'))

    # Read until next prompt
    res1 = res1[end:]
    while b'>' not in res1:
        data = s.recv(4096)
        if not data: break
        res1 += data

    # Option 2: encrypt flag
    s.send(b'2\n')
    res2 = b""
    while True:
        data = s.recv(4096)
        if not data: break
        res2 += data
        if b']' in data: break

    start = res2.find(b'[')
    end = res2.find(b']') + 1
    list_str = res2[start:end].replace(b'np.complex128', b'complex')
    ct_flag = eval(list_str.decode('utf-8', errors='ignore'))

    s.close()

    blocks = [ct_flag[i*256:(i+1)*256] for i in range(len(ct_flag)//256)]

    positions = []
    for i, b in enumerate(blocks):
        if np.allclose(ct_char, b):
            positions.append(i)

    return positions

print("Positions for 'T':", get_mapping_for_char('T'))
