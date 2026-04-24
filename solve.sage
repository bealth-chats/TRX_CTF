from pwn import *
import re
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

context.log_level = 'debug'

while True:
    r = remote("hbkg.ctf.theromanxpl0.it", 9094)

    r.recvuntil(b"> ")
    r.sendline(b"1")
    r.recvuntil(b"x: ")
    r.sendline(b"1")
    r.recvuntil(b"y: ")
    r.sendline(b"0")
    r.recvuntil(b"z: ")
    r.sendline(b"0")

    v1_res = r.recvline().strip().decode()

    matches = set(re.findall(r'(\d+/\d+)\*pi', v1_res))
    print("Matches:", matches)

    fracs = list(matches)
    rot_theta_frac = None
    angle_fracs = []
    for frac in fracs:
        num, den = frac.split('/')
        if int(den) in [180, 90, 60, 45, 36, 30, 20, 18, 15, 12, 10, 9, 6, 5, 4, 3, 2]:
            rot_theta_frac = frac
        else:
            angle_fracs.append(frac)

    if len(angle_fracs) != 2:
        print("Could not parse 2 angles. Retrying...")
        r.close()
        continue

    # Notice from `v = vector([cos(theta)*sin(phi), sin(theta)*sin(phi), cos(phi)])`
    # The output v1_res actually has `sqrt(...)` which comes from v.norm().
    # Actually wait... `u = v / v.norm()`.
    # `cos(phi)` is just `cos(...)` without any `sin(...)` squared under it?
    # Actually let's just test both combinations randomly!
    # I'll just use the second permutation this time.

    theta_expr = angle_fracs[1] + "*pi"
    phi_expr = angle_fracs[0] + "*pi"

    x_str = f"cos({theta_expr})*sin({phi_expr})"
    y_str = f"sin({theta_expr})*sin({phi_expr})"
    z_str = f"cos({phi_expr})"

    r.recvuntil(b"> ")
    r.sendline(b"2")
    r.recvuntil(b"x: ")
    r.sendline(x_str.encode())
    r.recvuntil(b"y: ")
    r.sendline(y_str.encode())
    r.recvuntil(b"z: ")
    r.sendline(z_str.encode())

    enc_res = r.recvline().strip().decode()
    r.close()

    key = hashlib.sha256(b"0,0,0").digest()
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = unpad(cipher.decrypt(bytes.fromhex(enc_res)), AES.block_size)
        print("FLAG FOUND:", decrypted.decode())
        break
    except ValueError:
        print("Decryption failed! Retrying...")
