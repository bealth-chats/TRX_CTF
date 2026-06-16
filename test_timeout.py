import socket
import string
import numpy as np

def connect():
    s = socket.socket()
    s.settimeout(20)
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
    return s

def test_char(char):
    s = connect()
    data = b""

    # Wait for the first prompt
    while b'>' not in data:
        data += s.recv(1024)

    s.send(b'1\n')
    data = b""
    while b'wanna encrypt?' not in data:
        data += s.recv(1024)

    s.send(f"{ord(char):02x}\n".encode())

    res1 = b""
    while b']' not in res1:
        res1 += s.recv(8192)

    # Read until next prompt
    data = res1[res1.find(b']')+1:]
    while b'>' not in data:
        data += s.recv(1024)

    s.send(b'2\n')
    res2 = b""
    while b']' not in res2:
        res2 += s.recv(8192)

    s.close()

    start1 = res1.find(b'[')
    end1 = res1.find(b']') + 1
    list_str1 = res1[start1:end1].replace(b'np.complex128', b'complex')
    ct_char = eval(list_str1.decode('utf-8', errors='ignore'))

    start2 = res2.find(b'[')
    end2 = res2.find(b']') + 1
    list_str2 = res2[start2:end2].replace(b'np.complex128', b'complex')
    ct_flag = eval(list_str2.decode('utf-8', errors='ignore'))

    blocks = [ct_flag[i*256 : (i+1)*256] for i in range(len(ct_flag)//256)]

    match_indices = []
    for i, b in enumerate(blocks):
        if np.allclose(ct_char, b):
            match_indices.append(i)

    return match_indices

charset = string.ascii_letters + string.digits + "{}_-!@#$%^&*"
flag_len = 38
flag = ['?'] * flag_len
flag[0] = 'T'
flag[1] = 'R'
flag[2] = 'X'
flag[3] = '{'

# known mapping from sim_local_brute.py
# 1: [8, 33] -> R
# 4: [9, 30, 34]
# 5: [11, 25, 29]
# 7: [10, 19, 24, 32]
# 12: [31, 35]
# 13: [23, 27]
# 14: [17, 22]
# 15: [28]

for m in [8, 33]:
    flag[m] = 'R'

for char in charset:
    if char in ['T', 'R', 'X', '{']:
        continue
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
