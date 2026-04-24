import socket
import numpy as np

s = socket.socket()
s.settimeout(20)
s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))

data = b""
while b'>' not in data:
    data += s.recv(1024)

s.send(b"1\n")
data = b""
while b'encrypt?' not in data:
    data += s.recv(1024)

s.send(f"{ord('}'):02x}\n".encode())
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

print("Matches for '}':", matches)
