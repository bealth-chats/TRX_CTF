import numpy as np

with open("flag_ct.txt", "rb") as f:
    data = f.read()

start = data.find(b'[')
end = data.rfind(b']') + 1
list_str = data[start:end].replace(b'np.complex128', b'complex')

ct = eval(list_str.decode('utf-8', errors='ignore'))
blocks = [ct[i*256 : (i+1)*256] for i in range(len(ct) // 256)]

# Can we determine if sum(sort(|b|)) is the same for a char regardless of the secret?
# I already tested this and found:
# Sum of sorted mags for secret1: 14.387926500903319
# Sum of sorted mags for secret2: 14.236238295798463
#
# But wait! I tested THIS for `char = 0` (null byte)!
# Let's see if for a SPECIFIC connection, all `pt` have UNIQUE sum of sorted magnitudes?
# Yes! And because `pt` is the ONLY input, the sorted magnitudes are a unique fingerprint of `pt` GIVEN the secret!
# But we don't know the secret.

# Is there anything else?
