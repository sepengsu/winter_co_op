import os
# Set non-random initial muscle activations
import sys
from abc import ABC, abstractmethod
from typing import Optional

import gym
import numpy as np
from . import measureLua as lua
from . import balance
from . import deprlpaper as dep

# Add sconepy folders to path
if sys.platform.startswith("win"):
    sys.path.append("C:/Program Files/SCONE/bin")
elif sys.platform.startswith("linux"):
    sys.path.append("/opt/scone/lib")
elif sys.platform.startswith('darwin'):
    sys.path.append("/Applications/SCONE.app/Contents/MacOS/lib")

import sconepy

DEFAULT_WEIGHTS = {'Gait': 100,
 'Effort': -1.3079,
 'ActivationSquared': -0.0009657,
 'HeadAcceleration': -1.1628,
 'GRFJerk': -0.2494,
 'KneeLimitForce': -0.25,
 'DoLimits': -0.1}

'''
아래 함수들은 나중에 Gaitgym.py에서 custom_reward에서 이를 설정하면 된다!!!!
'''
def rewardfunction(model,head_hody, grf,prev_excs):
    '''
    종합
    '''
    #reward = reward_from_lua(model,head_hody,grf) + balance_reward(model,head_hody,grf)
    #reward = reward_from_lua(model,head_hody,grf)
    reward = dep.total_reward(model,head_hody,prev_excs)
    return reward

def reward_from_lua(model,head_body,grf,weights = DEFAULT_WEIGHTS,eff_type = 'TotalForce'):
    ''' 
    논문에 제시되어 있는 함수를 lua로 코딩되어 있는 것들을 파이썬으로 바꾼다. 
    참조 논문: https://www.sciencedirect.com/science/article/pii/S0021929021003110?via%3Dihub
    coefficient는 추후 수정 예정
    input 설명
    model: env.model, head_body: env.head_body

    # 2024.01.02
    GRF 미분을 위하여 전 step에서의 grf 정보를 추가함 (함수에서 grf으로 추가)
    # 2024.01.02
    python_scone에서 파일 수정 및 함수 적용 완료
     
    # 2024.01.03
    coeff 관련 문제가 발생함. 중요도에 따른 조정해야함 
    '''
    rwd_dict = dict()
    names = list(DEFAULT_WEIGHTS.keys())
    #1. Gait measure
    rwd_dict[names[0]] = lua.gait_measure(model)
    #2. Effort
    rwd_dict[names[1]] = lua.efforts(model, eff_type)
    #3. ActivationSquared
    rwd_dict[names[2]] = lua.muscle_activation_squared(model)
    #4. HeadAcceleration
    rwd_dict[names[3]] = lua.head_accelration(head_body)
    #5. GRF
    rwd_dict[names[3]] = lua.derivative_grf(model,grf)
    #6. KneeLimitForce
    rwd_dict[names[4]] = 0 
    #7. DoLimits
    rwd_dict[names[5]] = 0
    return _sum_weight_and_rwd(weights,rwd_dict)

BALANCE_WEIGHTS = {'velocity':-0.1,
                   'position':-0.01,
                   'upright':0.1}


def balance_reward(model,head_body,grf,weights = BALANCE_WEIGHTS):
    rwd_dict = dict()
    names = list(BALANCE_WEIGHTS.keys())    
    #1. Velocity Z
    rwd_dict[names[0]] = 0
    #2. Position Z
    rwd_dict[names[1]] = balance.absposition(model,head_body)

    #3. upright_reward
    # https://arxiv.org/ftp/arxiv/papers/2308/2308.04462.pdf 참고
    rwd_dict[names[2]] = balance.upright_reward(model,head_body)

    return _sum_weight_and_rwd(weights,rwd_dict)   

def _sum_weight_and_rwd(weights:dict,rwd_dict:dict):
    '''이 함수는 weight x reward를 계산하는 함수이다.'''
    return sum(weights[key] * rwd_dict[key] for key in weights if key in rwd_dict)
