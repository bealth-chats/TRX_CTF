import socket
import ast

def connect():
    s = socket.socket()
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
    return s

s = connect()
print(s.recv(1024).decode())
s.send(b'2\n')
res = b""
while True:
    data = s.recv(4096)
    if not data:
        break
    res += data
    if b']' in data:
        break

with open("flag_ct.txt", "wb") as f:
    f.write(res)
print("Saved to flag_ct.txt")
