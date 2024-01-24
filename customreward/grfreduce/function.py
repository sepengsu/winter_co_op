from myutils.kwargs_utils import _sum_weight_and_rwd
from . import first

DEFAULT_WEIGHTS ={
    'grfdelta': 0,
    'grfdelta_x':0,
    'grf' : 0
}
def totalreward(model,head_body,grf,prev_excs,**kwargs):
    '''
    여기서는 크게 3가지로 나눠서 계산한다.
    '''
    typesdelta = kwargs.get('grf_types',None)
    grfdelta = kwargs.get('grf_grfdelta',None)
    grfdelta_x = kwargs.get('grf_grfdelta_x',None)
    Grf = kwargs.get('grf_grf',None)
    reward_dict = dict()
    if grfdelta:
        DEFAULT_WEIGHTS['grfdetla'] = grfdelta
    if grfdelta_x:
        DEFAULT_WEIGHTS['grfdelta_x'] = grfdelta_x
    if Grf:
        DEFAULT_WEIGHTS['grf'] = Grf

    for key in DEFAULT_WEIGHTS:
        function = getattr(first,key,False)
        if function:
            reward_dict[key] = function(model,grf)
    
    return _sum_weight_and_rwd(weights=DEFAULT_WEIGHTS,rwd_dict=reward_dict)