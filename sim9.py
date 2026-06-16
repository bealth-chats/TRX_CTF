import socket

s = socket.socket()
s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
print("Connected")
print("Banner:", s.recv(1024).decode())
s.send(b"2\n")
res = b""
while b']' not in res:
    res += s.recv(8192)
print("Res length:", len(res))

# try sending 2 again
res = res[res.find(b']')+1:]
while b'>' not in res:
    res += s.recv(1024)

s.send(b"2\n")
res2 = b""
while b']' not in res2:
    res2 += s.recv(8192)
print("Res 2 length:", len(res2))
