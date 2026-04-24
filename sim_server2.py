import socket

s = socket.socket()
s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
print("Connected")
s.send(b"1\n")
print("Sent 1")
s.send(b"54\n")
print("Sent 54")

res = b""
while b']' not in res:
    chunk = s.recv(8192)
    if not chunk: break
    res += chunk
    print(f"Received {len(chunk)}, total {len(res)}")
print("Done receiving")
