import numpy as np
import os
import pandas as pd
# Get the path of the current directory
_current_dir = '\\'.join(str(__file__).split('\\')[:-1])

# Get the names of all subdirectories in the current directory
all_names = [name.split('\\')[-1] for name in os.listdir(_current_dir) if (not name.startswith('__')) and not (name=='reward.py')]

_dict_name = all_names
DEFAULT_WEIGHTS  = dict(zip(_dict_name,np.zeros(len(_dict_name))))

def settingtypeweight(type_weights = DEFAULT_WEIGHTS,setting = True): # 안씀
    '''
    weight를 설정하는 함수
    Parameters:
        type_weights: reward type별 weight - dictionary로 input 받음
        setting: weight를 설정할 것인지 묻는 파라미터
    '''
    if setting == False:
        print("weight를 변경하지 않았습니다.")
        return
    global DEFAULT_WEIGHTS
    for key in type_weights.keys():
        if key not in _dict_name:
            raise ValueError(f'Unknown argument: {key}')
        DEFAULT_WEIGHTS[key] = type_weights[key]
    print("weight가 변경되었습니다.")


DEFAULT_REWARD_WEIGHTS = dict()
def settingrewardweight(reward_weights,setting = True): # 안씀
    '''
    weight를 설정하는 함수
    Parameters:
        type_weights: reward type별 weight - dictionary로 input 받음
        kwargs: reward type별 weight를 변경하기 위한 파라미터
            ex) balance_position_z : position_z 의 weight를 변경
            즉, (reward type)_(weight name) = (weight)으로 변경해야한다.
    '''
    if setting == False:
        return
    global DEFAULT_REWARD_WEIGHTS
    for key in reward_weights.keys():
        DEFAULT_REWARD_WEIGHTS[key] = reward_weights[key]


def rewardfunction(model,head_body, grf,prev_excs,rwd_type_weights = DEFAULT_WEIGHTS,rwd_weights = DEFAULT_REWARD_WEIGHTS): 
    '''
    종합 reward function

    Parameters:
    type_weights: reward type별 weight - dictionary로 input 받음
    kwargs: reward type별 weight를 변경하기 위한 파라미터
        ex) balance_position_z : position_z 의 weight를 변경
        즉, (reward type)_(weight name) = (weight)으로 변경해야한다.
    '''
    Dict = dict(zip(_dict_name,np.zeros(len(_dict_name))))
    
    for key in rwd_type_weights.keys():
       string = f'import customreward.{key} as {key}'
       exec(string) 
       string = f'Dict[key] = {key}.totalreward(model,head_body,grf,prev_excs,**rd_weights)' 
       exec(string)

    reward = _sum_weight_and_rwd(rwd_type_weights,Dict)
    return reward

def showingweight():
    '''weight를 보여주는 함수'''
    print("type_weight를 보여줍니다.")
    if sum(DEFAULT_WEIGHTS.values()) == 0:
        print("customreward 함수를 사용하지 않았습니다.")
    else:
        print(pd.DataFrame.from_dict(DEFAULT_WEIGHTS, orient='index').reset_index().rename(columns={'index': 'Key', 0: 'Value'}))
    if sum(DEFAULT_REWARD_WEIGHTS.values()) == 0:
        print("reward weight를 변경하지 않았습니다.")
    else:
        print(pd.DataFrame.from_dict(DEFAULT_REWARD_WEIGHTS, orient='index').reset_index().rename(columns={'index': 'Key', 0: 'Value'}))
    
        
def _sum_weight_and_rwd(weights:dict,rwd_dict:dict):
    '''이 함수는 weight x reward를 계산하는 함수이다.'''
    return sum(weights[key] * rwd_dict[key] for key in weights if key in rwd_dict)



    