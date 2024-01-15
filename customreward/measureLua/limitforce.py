import os
# Set non-random initial muscle activations
import sys
from abc import ABC, abstractmethod
from typing import Optional
import gym
import numpy as np
from ..measureLua import vector_scale

# Add sconepy folders to path
if sys.platform.startswith("win"):
    sys.path.append("C:/Program Files/SCONE/bin")
elif sys.platform.startswith("linux"):
    sys.path.append("/opt/scone/lib")
elif sys.platform.startswith('darwin'):
    sys.path.append("/Applications/SCONE.app/Contents/MacOS/lib")
import sconepy

def Knee_limit_force(model,min=0,max=0):
    '''
    논문 기준으로 limit_toque 사용
    '''
    joints = model.joints()
    left =vector_scale(joints[1].limit_torque().array())
    right =vector_scale(joints[4].limit_torque().array())
    return left + right

def ankle_angle(model,min=-60,max=60):
    ''' 
    여기는 lua 코드를 기반으로 하고 있음
    '''
    