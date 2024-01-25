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


class GRFBefore():
    def __init__(self,model):
        self.calcn_l = model.bodies()[7].contact_force()
        self.calcn_r=  model.bodies()[4].contact_force()

    def left(self):
        return self.calcn_l
    
    def right(self):
        return self.calcn_r


def derivative_grf(model,grf:GRFBefore):
    '''
    force는 contact_force를 활용함 
    기존코드에서는 normalize를 75.1646*9.80665을 활용함 
    이는 mass*gravity으로 보여짐 
    
    '''
    foot_l = model.bodies()[7]
    foot_r = model.bodies()[4]
    foot_l_force = foot_l.contact_force()
    foot_r_force = foot_r.contact_force()
    
    #norm_factor  = 75.1646*9.80665
    norm_factor = model.mass()*vector_scale(model.gravity().array())
   
    # 1. 계산
    impact_left = delta_all(foot_l_force,grf.calcn_l,norm_factor)
    impact_right = delta_all(foot_r_force,grf.calcn_r,norm_factor)

    return impact_left + impact_right

def vector_scale(vector:np.array):
    '''
    vector 크기 나타내기
    '''
    return np.sqrt(sum(vector**2))

def delta_all(force,grf,norm_factor):
    x = force.x-grf.x
    y = force.y-grf.y
    z = force.z-grf.z
    return abs(x)/norm_factor+abs(y)/norm_factor+abs(z)/norm_factor


if __name__=='__main__':
    pass