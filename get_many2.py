import socket
import ast
import numpy as np
import threading
import sys
import string

charset = string.ascii_letters + string.digits + "{}_-!@#$%^&*"
flag_len = 38
flag = ['?'] * flag_len
flag[0] = 'T'
flag[1] = 'R'
flag[2] = 'X'
flag[3] = '{'

known_map = {
    1: [8, 33], 4: [9, 30, 34], 5: [11, 25, 29], 7: [10, 19, 24, 32],
    12: [31, 35], 13: [23, 27], 14: [17, 22], 15: [28]
}
for k, v in known_map.items():
    if flag[k] != '?':
        for idx in v: flag[idx] = flag[k]

def test_char(char):
    try:
        s = socket.socket()
        s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))

        # We don't read the banner, we just send commands. But wait, TCP stream.
        # It's better to just send everything!
        # The prompt is sent, we can just blind send.
        s.send(b"1\n")
        s.send(f"{ord(char):02x}\n".encode())

        res = b""
        while b']' not in res:
            chunk = s.recv(8192)
            if not chunk: break
            res += chunk

        start = res.find(b'[')
        end = res.find(b']') + 1
        ct_char = eval(res[start:end].replace(b'np.complex128', b'complex').decode('utf-8', errors='ignore'))

        res = res[end:]

        s.send(b"2\n")
        res2 = res
        while b']' not in res2:
            chunk = s.recv(8192)
            if not chunk: break
            res2 += chunk

        s.close()

        start2 = res2.find(b'[')
        end2 = res2.find(b']') + 1
        ct_flag = eval(res2[start2:end2].replace(b'np.complex128', b'complex').decode('utf-8', errors='ignore'))

        blocks = [ct_flag[i*256 : (i+1)*256] for i in range(len(ct_flag)//256)]

        matches = []
        for i, b in enumerate(blocks):
            if np.allclose(ct_char, b):
                matches.append(i)

        if matches:
            print(f"Found {char} at {matches}", flush=True)
            for m in matches: flag[m] = char
    except Exception as e:
        print(f"Error {char}: {e}", flush=True)

import concurrent.futures
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = []
    for char in charset:
        if char in ['T', 'R', 'X', '{']: continue
        futures.append(executor.submit(test_char, char))
    concurrent.futures.wait(futures)

print("".join(flag))
