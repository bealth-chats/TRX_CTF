import socket

s = socket.socket()
s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
print("Connected")
print("Banner:", s.recv(1024).decode())
s.send(b"1\n")
print("Prompt 1:", s.recv(1024).decode())
s.send(b"54\n")
res = b""
while b']' not in res:
    res += s.recv(8192)
print("Res 1 length:", len(res))

res = res[res.find(b']')+1:]
while b'>' not in res:
    res += s.recv(1024)
print("Prompt 2:", res.decode())

s.send(b"2\n")
res2 = b""
while b']' not in res2:
    res2 += s.recv(8192)
print("Res 2 length:", len(res2))
