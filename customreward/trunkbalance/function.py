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
    'position_z': 0,
    'com_z': 0,
}
from myutils.kwargs_utils import _sum_weight_and_rwd

class TrunkBalance():
        def __init__(self,weight_dict,model,head_body):
            self.weight_dict = weight_dict
            self.model = model
            self.head_body = head_body
            self.rwd_dict = dict()
        
        def position_z(self):
            pos = self.head_body.com_pos().z
            r = abs(pos)-abs(-0.1) if abs(pos) > 0.1 else 0
            return r
        
        def com_z(self):
            pos = self.model.com_pos().z
            r = abs(pos)-abs(-0.1) if abs(pos) > 0.1 else 0
            return r
    
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
    position_z = kwargs.get('trunkbalance_position_z',False)
    com_z = kwargs.get('trunkbalance_com_z',False)
    if position_z:
        BALANCE_WEIGHTS['position_z'] = position_z
    if com_z:
        BALANCE_WEIGHTS['com_z'] = com_z

    #calculate reward
    balance = TrunkBalance(BALANCE_WEIGHTS,model,head_body)
    return balance.return_reward()

