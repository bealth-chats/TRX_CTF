import socket
import string
import numpy as np

def connect():
    s = socket.socket()
    s.settimeout(10)
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
    return s

def test_char(char):
    s = connect()
    data = s.recv(1024)

    # Wait for the first prompt
    while b'>' not in data:
        data += s.recv(1024)

    s.send(b'1\n')
    data = s.recv(1024)
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

print("Testing T...")
print(test_char('T'))
