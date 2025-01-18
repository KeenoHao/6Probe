# convert IPv6 str to numpy seeds1.npy

import numpy as np
from IPy import IP
import sys


with open("random10w2") as f:
    arrs = []
    for ip in f.read().splitlines():
        arrs.append([int(x, 16)
                    for x in IP(ip).strFullsize().replace(":", "")])

    np.save("seeds.npy", np.array(arrs, dtype=np.uint8))
