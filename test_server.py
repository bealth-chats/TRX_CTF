import socket

def test():
    s = socket.socket()
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
    print("Connected")
    data = s.recv(1024)
    print("Received banner")

    s.send(b'1\n')
    data = s.recv(1024)
    print("Received prompt 1:", data.decode())

    s.send(f"{ord('T'):02x}\n".encode())

    res1 = b""
    while b']' not in res1:
        chunk = s.recv(4096)
        if not chunk: break
        res1 += chunk
    print("Received res1 length:", len(res1))

    # Let's read until we see the menu again
    res1 = res1[res1.find(b']')+1:]
    while b'>' not in res1:
        chunk = s.recv(4096)
        if not chunk: break
        res1 += chunk
    print("Received menu again")

    s.send(b'2\n')
    res2 = b""
    while b']' not in res2:
        chunk = s.recv(4096)
        if not chunk: break
        res2 += chunk
    print("Received res2 length:", len(res2))
    s.close()

test()
