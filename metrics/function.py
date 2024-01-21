
from . import z
from myutils.kwargs_utils import _make_dict

def reward_function(model, head_body, **kwargs):
    """
    주어진 모델과 헤드-바디 객체를 사용하여 보상을 계산하는 함수입니다.

    Parameters:
    - model: 보상 계산에 사용할 모델 객체
    - head_body: 보상 계산에 사용할 헤드-바디 객체
    - kwargs: 추가적인 인자를 받을 수 있는 가변 키워드 인자입니다.
        - reward_type (str): 보상 유형을 지정합니다. 'position' 또는 'velocity'를 사용할 수 있습니다.
        - types (str): 보상을 계산할 대상을 지정합니다. 'head', 'body', 또는 'both'를 사용할 수 있습니다.

    Returns:
    - 주어진 모델과 헤드-바디 객체의 상태에 따른 보상값
    """
    reward_dict= _make_dict(**kwargs)
    for key in kwargs:
        if key == 'reward_type':
            reward_type = kwargs[key]
        elif key == 'types':
            types = kwargs[key]
        else:
            raise ValueError(f'Unknown argument: {key}')
        
    if reward_type == 'position':
        if types == 'head':
            reward_dict['head_position'] = z.head_position(head_body)
        elif types == 'body':
            reward_dict['body_position'] = z.body_position(model)
        elif types == 'both':
            reward_dict['head_position'] = z.head_position(head_body)
            reward_dict['body_position'] = z.body_position(model)
        else:
            raise ValueError(f'Unknown argument: {types}')
        
    elif reward_type == 'velocity':
        if types == 'head':
            reward_dict['head_velocity'] = z.head_velocity(head_body)
        elif types == 'body':
            reward_dict['body_velocity'] = z.body_velocity(model)
        elif types == 'both':
            reward_dict['head_velocity'] = z.head_velocity(head_body)
            reward_dict['body_velocity'] = z.body_velocity(model)
        else:
            raise ValueError(f'Unknown argument: {types}')
    elif reward_type == 'both':
        if types == 'head':
            reward_dict['head_position'] = z.head_position(head_body)
            reward_dict['head_velocity'] = z.head_velocity(head_body)
        elif types == 'body':
            reward_dict['body_position'] = z.body_position(model)
            reward_dict['body_velocity'] = z.body_velocity(model)
            
        elif types == 'both':
            reward_dict['head_position'] = z.head_position(head_body)
            reward_dict['head_velocity'] = z.head_velocity(head_body)
            reward_dict['body_position'] = z.body_position(model)
            reward_dict['body_velocity'] = z.body_velocity(model)
        else:
            raise ValueError(f'Unknown argument: {types}')
    else:
        raise ValueError(f'Unknown argument: {reward_type}')
    
    return reward_dict
