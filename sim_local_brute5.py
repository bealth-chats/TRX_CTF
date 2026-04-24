import socket
import string
import numpy as np

charset = string.ascii_letters + string.digits + "{}_-!@#$%^&*"
flag_len = 38
flag = ['?'] * flag_len
flag[0] = 'T'
flag[1] = 'R'
flag[2] = 'X'
flag[3] = '{'
flag[-1] = '}'

known_map = {
    1: [8, 33], 4: [9, 30, 34], 5: [11, 25, 29], 7: [10, 19, 24, 32],
    12: [31, 35], 13: [23, 27], 14: [17, 22], 15: [28]
}

for k, v in known_map.items():
    if flag[k] != '?':
        for idx in v: flag[idx] = flag[k]

def test_char(char):
    s = socket.socket()
    s.settimeout(20)
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))

    # Wait for prompt
    data = b""
    while b'>' not in data:
        data += s.recv(1024)

    s.send(b"1\n")
    data = b""
    while b'encrypt?' not in data:
        data += s.recv(1024)

    s.send(f"{ord(char):02x}\n".encode())
    res1 = b""
    while b']' not in res1:
        chunk = s.recv(8192)
        if not chunk: break
        res1 += chunk

    start = res1.find(b'[')
    end = res1.find(b']') + 1
    list_str = res1[start:end].replace(b'np.complex128', b'complex')
    ct_char = eval(list_str.decode('utf-8', errors='ignore'))

    res1 = res1[end:]
    while b'>' not in res1:
        chunk = s.recv(1024)
        if not chunk: break
        res1 += chunk

    s.send(b"2\n")
    res2 = b""
    while b']' not in res2:
        chunk = s.recv(8192)
        if not chunk: break
        res2 += chunk

    start = res2.find(b'[')
    end = res2.find(b']') + 1
    list_str = res2[start:end].replace(b'np.complex128', b'complex')
    ct_flag = eval(list_str.decode('utf-8', errors='ignore'))
    s.close()

    blocks = [ct_flag[i*256 : (i+1)*256] for i in range(len(ct_flag)//256)]
    matches = []
    for i, b in enumerate(blocks):
        if np.allclose(ct_char, b):
            matches.append(i)
    return matches

for char in charset:
    if char in ['T', 'R', 'X', '{', '}']: continue
    print(f"Testing {char}...", flush=True)
    try:
        matches = test_char(char)
        if matches:
            print(f"Found {char} at {matches}", flush=True)
            for m in matches: flag[m] = char
    except Exception as e:
        print(f"Error {char}: {e}", flush=True)

print("".join(flag))
