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

BALANCE_WEIGHTS = {
    'diff_position_z':  0,
    'position_z':0,
    'velocity_z': 0,
}
from myutils.kwargs_utils import _sum_weight_and_rwd

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
            r = np.exp(-abs(pos)**2)
            return r

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
        
def totalreward(model,head_body,grf,prev_excs,**kwargs):
    '''
    model: env.model
    head_body: env.head_body
    grf: env.grf
    prev_excs: env.prev_excs
    weight: weight dictionary
    -> weight를 변경하기 위해서는 아래의 파라미터를 설정해야함
    kwargs: 
        - balance_position_z : position_z
        - balance_diff_position_z: diff_position_z
        - balance_velocity_z: velocity_z

    return: reward
    '''
    #change weight
    position_z = kwargs.get('balance_position_z',False)
    diff_position_z = kwargs.get('balance_diff_position_z',False)
    velocity_z = kwargs.get('balance_velocity_z',False)
    if position_z:
        BALANCE_WEIGHTS['position_z'] = position_z
    if diff_position_z:
        BALANCE_WEIGHTS['diff_position_z'] = diff_position_z
    if velocity_z:
        BALANCE_WEIGHTS['velocity_z'] = velocity_z

    #calculate reward
    balance = MyBalance(BALANCE_WEIGHTS,model,head_body)
    return balance.return_reward()

