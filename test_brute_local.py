import numpy as np

# We know the flag starts with TRX{
# The flag ends with }
# Can we use the fact that the sum of the magnitudes of the amplitudes of the output state is a characteristic of the input state?
# Wait! In sim2.py we found that:
# Block 0 sorted sum: 14.156350565246967
# Block 1 sorted sum: 14.147079575466046
# Block 2 sorted sum: 14.22919443643589
# Block 3 sorted sum: 14.33973899364566
# Wait, but is this sorted sum independent of the secret?
# Let's check!
