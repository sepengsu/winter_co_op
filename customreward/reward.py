import numpy as np
import customreward


_dict_name = customreward.all_names
DEFAULT_WEIGHTS  = dict(zip(_dict_name,np.zeros(len(_dict_name))))
DEFAULT_WEIGHTS['balance'] = 1


def rewardfunction(model,head_hody, grf,prev_excs,type_weights = DEFAULT_WEIGHTS,**kwargs):
    '''
    종합 reward function

    Parameters:
    type_weights: reward type별 weight - dictionary로 input 받음
    kwargs: reward type별 weight를 변경하기 위한 파라미터
        ex) balance_position_z : position_z 의 weight를 변경
        즉, (reward type)_(weight name) = (weight)으로 변경해야한다.
    '''
    Dict = dict(zip(_dict_name,np.zeros(len(_dict_name))))
    if type_weights.keys() != _dict_name:
        raise ValueError(f'Unknown argument: {type_weights.keys()}')
    
    for key in type_weights.keys():
       string = f'import customreward.{key} as {key}'
       exec(string) 
       string = f'Dict[key] = {key}.totalreward(model,head_hody,grf,prev_excs,**kwargs)' 
       exec(string)

    return _sum_weight_and_rwd(type_weights,Dict)
 
def _sum_weight_and_rwd(weights:dict,rwd_dict:dict):
    '''이 함수는 weight x reward를 계산하는 함수이다.'''
    return sum(weights[key] * rwd_dict[key] for key in weights if key in rwd_dict)



    