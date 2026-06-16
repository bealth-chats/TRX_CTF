import socket
import string
import numpy as np

def connect():
    s = socket.socket()
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
    return s

def test_char(char):
    s = connect()
    prompt = s.recv(4096) # Welcome... What do you wanna do?

    s.send(b'1\n')
    # Server expects prompt "What do you wanna encrypt? (one hex byte)"
    # We can just send the byte. But it might wait. Let's send everything!
    s.send(f"{ord(char):02x}\n".encode())

    res = b""
    while b']' not in res:
        res += s.recv(4096)

    start = res.find(b'[')
    end = res.find(b']') + 1
    list_str = res[start:end].replace(b'np.complex128', b'complex')
    ct_char = eval(list_str.decode('utf-8', errors='ignore'))

    # Send request for flag
    s.send(b'2\n')

    res = b""
    while b']' not in res:
        res += s.recv(4096)

    start = res.find(b'[')
    end = res.find(b']') + 1
    list_str = res[start:end].replace(b'np.complex128', b'complex')
    ct_flag = eval(list_str.decode('utf-8', errors='ignore'))
    s.close()

    blocks = [ct_flag[i*256 : (i+1)*256] for i in range(len(ct_flag)//256)]

    match_indices = []
    for i, b in enumerate(blocks):
        if np.allclose(ct_char, b):
            match_indices.append(i)

    return match_indices

print(test_char('T'))
