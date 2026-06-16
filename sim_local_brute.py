import numpy as np

with open("flag_ct.txt", "rb") as f:
    data = f.read()

start = data.find(b'[')
end = data.rfind(b']') + 1
list_str = data[start:end].replace(b'np.complex128', b'complex')
ct = eval(list_str.decode('utf-8', errors='ignore'))
blocks = [ct[i*256 : (i+1)*256] for i in range(len(ct)//256)]

same_blocks = {}
for i in range(len(blocks)):
    for j in range(i+1, len(blocks)):
        if np.allclose(blocks[i], blocks[j]):
            if i not in same_blocks:
                same_blocks[i] = []
            same_blocks[i].append(j)

for k, v in same_blocks.items():
    print(f"{k}: {v}")

# Knowns:
# 0: 'T'
# 1: 'R' -> same as 8, 33
# 2: 'X'
# 3: '{'

# So flag[1] = 'R', flag[8] = 'R', flag[33] = 'R'
flag = ['?'] * len(blocks)
flag[0] = 'T'
flag[1] = 'R'
flag[2] = 'X'
flag[3] = '{'

for k, v in same_blocks.items():
    for idx in v:
        if flag[k] != '?':
            flag[idx] = flag[k]
        elif flag[idx] != '?':
            flag[k] = flag[idx]

print("".join(flag))
