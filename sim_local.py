import numpy as np

with open("flag_ct.txt", "rb") as f:
    data = f.read()

start = data.find(b'[')
end = data.rfind(b']') + 1
list_str = data[start:end].replace(b'np.complex128', b'complex')

ct = eval(list_str.decode('utf-8', errors='ignore'))
print(f"Parsed {len(ct)} complex numbers.")

blocks = []
for i in range(len(ct) // 256):
    blocks.append(ct[i*256 : (i+1)*256])

for i in range(4):
    print(f"Block {i} (char: {'TRX{'[i]}): max amplitude {np.max(np.abs(blocks[i]))}, min amplitude {np.min(np.abs(blocks[i]))}")

# Can we determine something from the indices of the highest amplitudes?
for i in range(4):
    mags = np.abs(blocks[i])
    top_indices = np.argsort(mags)[-5:][::-1]
    print(f"Block {i} (char: {'TRX{'[i]}): top 5 indices {top_indices}")
