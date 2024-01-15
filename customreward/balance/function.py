import os
import numpy as np
# Set non-random initial muscle activations
import sys
# Add sconepy folders to path
if sys.platform.startswith("win"):
    sys.path.append("C:/Program Files/SCONE/bin")
elif sys.platform.startswith("linux"):
    sys.path.append("/opt/scone/lib")
elif sys.platform.startswith('darwin'):
    sys.path.append("/Applications/SCONE.app/Contents/MacOS/lib")

import sconepy

def absposition(model, head_body):
    pos = head_body.com_pos().z

    return abs(pos)

def upright_reward(model,head_body):
    pos_m = model.com_pos().z
    pos_h = head_body.com_pos().z
    r = np.exp(-(abs(pos_m-pos_h))**2)
    return r