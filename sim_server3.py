import socket

s = socket.socket()
s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
s.send(b"1\n")
s.send(b"54\n")

res = b""
while b']' not in res:
    chunk = s.recv(8192)
    if not chunk: break
    res += chunk

res = res[res.find(b']')+1:]

s.send(b"2\n")
res2 = b""
while b']' not in res2:
    chunk = s.recv(8192)
    if not chunk: break
    res2 += chunk
    print(f"Received flag chunk {len(chunk)}, total {len(res2)}")
print("Done")
