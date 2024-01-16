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

class MyBalance():
        def __init__(self,weight_dict,model,head_body):
            self.weight_dict = weight_dict
            self.model = model
            self.head_body = head_body
            self.rwd_dict = dict()
    
        def diff_position_z(self):
            pos_m = self.model.com_pos().z
            pos_h = self.head_body.com_pos().z
            r = np.exp(-(abs(pos_m-pos_h))**2)
            return r
        
        def position_z(self):
            pos = self.head_body.com_pos().z
            r = np.exp(-abs(pos))
            return 

        def velocity_z(self):
            wm = 0.3
            wh = 1-wm
            vel_m = self.model.com_vel().z
            vel_h = self.head_body.com_vel().z
            return wm*vel_m+wh*vel_h

   
        def return_reward(self):
            for name in self.weight_dict:
                self.rwd_dict[name] = getattr(self,name)()
            
            return _sum_weight_and_rwd(self.weight_dict,self.rwd_dict)

def _sum_weight_and_rwd(weights:dict,rwd_dict:dict):
    '''이 함수는 weight x reward를 계산하는 함수이다.'''
    return sum(weights[key] * rwd_dict[key] for key in weights if key in rwd_dict)      