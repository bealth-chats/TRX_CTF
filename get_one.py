import socket
import sys

def connect():
    s = socket.socket()
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
    return s

s = connect()
print(s.recv(1024).decode())

s.send(b'1\n')
print(s.recv(1024).decode())

s.send(f"{ord('T'):02x}\n".encode())

res1 = b""
while b']' not in res1:
    res1 += s.recv(4096)
print("Got char encryption")

s.send(b'2\n')
res2 = b""
while b']' not in res2:
    res2 += s.recv(4096)
print("Got flag encryption")

s.close()
print("Success")
