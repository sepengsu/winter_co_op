
def _make_dict(**kwargs):
    """
    주어진 키워드 인수를 기반으로 딕셔너리를 생성합니다.

    Args:
        **kwargs: 보상 유형과 유형을 지정하는 키워드 인수입니다.

    Returns:
        dict: 지정된 보상 유형과 유형을 포함하는 딕셔너리입니다.

    Raises:
        ValueError: 알 수 없는 인수가 제공된 경우입니다.

    Example:
        >>> _make_dict(reward_type='position', types='head')
        {'head_position': 0}
    """
    Dict = dict()
    reward_type = kwargs.get('reward_type')
    types = kwargs.get('types')
    
    if reward_type == 'position':
        if types == 'head':
            Dict['head_position'] = 0
        elif types == 'body':
            Dict['body_position'] = 0
        elif types == 'both':
            Dict['head_position'] = 0
            Dict['body_position'] = 0
        else:
            raise ValueError(f'Unknown argument: {types}')
    elif reward_type == 'velocity':
        if types == 'head':
            Dict['head_velocity'] = 0
        elif types == 'body':
            Dict['body_velocity'] = 0
        elif types == 'both':
            Dict['head_velocity'] = 0
            Dict['body_velocity'] = 0
        else:
            raise ValueError(f'Unknown argument: {types}')
    elif reward_type == 'both':
        if types == 'head':
            Dict['head_position'] = 0
            Dict['head_velocity'] = 0
        elif types == 'body':
            Dict['body_position'] = 0
            Dict['body_velocity'] = 0
        elif types == 'both':
            Dict['head_position'] = 0
            Dict['head_velocity'] = 0
            Dict['body_position'] = 0
            Dict['body_velocity'] = 0
        else:
            raise ValueError(f'Unknown argument: {types}') 
    else:
        raise ValueError(f'Unknown argument: {reward_type}')
    return Dict

def _sum_weight_and_rwd(weights:dict,rwd_dict:dict):
    '''이 함수는 weight x reward를 계산하는 함수이다.'''
    return sum(weights[key] * rwd_dict[key] for key in weights if key in rwd_dict)      