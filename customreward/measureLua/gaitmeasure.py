import os
# Set non-random initial muscle activations
import sys
from abc import ABC, abstractmethod
from typing import Optional
import gym
import numpy as np

# Add sconepy folders to path
if sys.platform.startswith("win"):
    sys.path.append("C:/Program Files/SCONE/bin")
elif sys.platform.startswith("linux"):
    sys.path.append("/opt/scone/lib")
elif sys.platform.startswith('darwin'):
    sys.path.append("/Applications/SCONE.app/Contents/MacOS/lib")
import sconepy

def gait_measure(model):
    vel = model.com_vel().x
    return vel 