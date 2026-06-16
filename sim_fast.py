import socket
import string
import numpy as np

def connect():
    s = socket.socket()
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
    return s

def test_char(char):
    s = connect()
    data = s.recv(1024)

    # Send both requests at once to avoid waiting for prompts
    s.send(b'1\n')
    s.send(f"{ord(char):02x}\n".encode())
    s.send(b'2\n')

    res = b""
    while True:
        chunk = s.recv(8192)
        if not chunk: break
        res += chunk
        # We need to find two ']'
        if res.count(b']') >= 2:
            break

    s.close()

    first_end = res.find(b']') + 1
    res1 = res[:first_end]
    res2 = res[first_end:]

    start1 = res1.find(b'[')
    list_str1 = res1[start1:first_end].replace(b'np.complex128', b'complex')
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
