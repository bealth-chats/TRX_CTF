import socket
import ast
import numpy as np

def connect():
    s = socket.socket()
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
    return s

s = connect()
prompt = s.recv(4096)

s.send(b'1\n')
s.send(f"{ord('T'):02x}\n".encode())
res1 = b""
while b']' not in res1:
    res1 += s.recv(4096)

print("Got T_1")

s.send(b'1\n')
s.send(f"{ord('T'):02x}\n".encode())
res2 = b""
while b']' not in res2:
    res2 += s.recv(4096)

print("Got T_2")

start1 = res1.find(b'[')
end1 = res1.find(b']') + 1
ct1 = eval(res1[start1:end1].replace(b'np.complex128', b'complex').decode('utf-8', errors='ignore'))

start2 = res2.find(b'[')
end2 = res2.find(b']') + 1
ct2 = eval(res2[start2:end2].replace(b'np.complex128', b'complex').decode('utf-8', errors='ignore'))

print("Same?", np.allclose(ct1, ct2))
