import os
# Set non-random initial muscle activations
import sys

import gym
import sconegym
import numpy as np

# Add sconepy folders to path
if sys.platform.startswith("win"):
    sys.path.append("C:/Program Files/SCONE/bin")
elif sys.platform.startswith("linux"):
    sys.path.append("/opt/scone/lib")
elif sys.platform.startswith('darwin'):
    sys.path.append("/Applications/SCONE.app/Contents/MacOS/lib")

import sconepy

def head_accelration(head_body):
    acc = head_body.com_acc()
    sums  = abs(acc.x) +abs(acc.y) +abs(acc.z)
    return sums
    