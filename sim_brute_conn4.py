import socket
import string
import numpy as np

def connect():
    s = socket.socket()
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
    return s

def test_char(char):
    s = connect()

    # 1. Encrypt the character
    s.send(b'1\n')
    s.send(f"{ord(char):02x}\n".encode())

    res = b""
    while b']' not in res:
        res += s.recv(4096)

    start = res.find(b'[')
    end = res.find(b']') + 1
    list_str = res[start:end].replace(b'np.complex128', b'complex')
    ct_char = eval(list_str.decode('utf-8', errors='ignore'))

    # 2. Get the flag with the same secret
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

charset = string.ascii_letters + string.digits + "{}_-!@#$%^&*"
flag_len = 38
flag = ['?'] * flag_len

for char in charset:
    print(f"Testing {char}...", flush=True)
    try:
        matches = test_char(char)
        if matches:
            print(f"Found {char} at {matches}", flush=True)
            for m in matches:
                flag[m] = char
    except Exception as e:
        print(f"Error testing {char}: {e}", flush=True)

print("".join(flag))
