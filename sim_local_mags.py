import numpy as np

with open("flag_ct.txt", "rb") as f:
    data = f.read()

start = data.find(b'[')
end = data.rfind(b']') + 1
list_str = data[start:end].replace(b'np.complex128', b'complex')

ct = eval(list_str.decode('utf-8', errors='ignore'))

blocks = []
for i in range(len(ct) // 256):
    blocks.append(ct[i*256 : (i+1)*256])

# Let's see if np.sort(np.abs(block)) is unique per byte and independent of the secret!
# Earlier I tested "Are sorted mags independent of secret? False"
# Wait! In sim_mags.py I tested:
# v0_1 = encrypt(0, secret1)
# v0_2 = encrypt(0, secret2)
# mag_v0_1 = np.sort(np.abs(v0_1))[::-1]
# mag_v0_2 = np.sort(np.abs(v0_2))[::-1]
# print("Are sorted mags independent of secret?", np.allclose(mag_v0_1, mag_v0_2))
# Let me re-run and check if the sum of sorted mags is the same, or if they are identical?
