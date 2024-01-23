from myutils.kwargs_utils import _sum_weight_and_rwd
from . import first

DEFAULT_WEIGHTS ={
    'grfdelta': -1,
    'grf' : 0,
}
def totalreward(model,head_body,grf,prev_excs,**kwargs):
    '''
    여기서는 크게 3가지로 나눠서 계산한다.
    '''
    typesdelta = kwargs.get('grf_types',None)
    grfdelta = kwargs.get('grf_grfdelta',None)
    Grf = kwargs.get('grf_grf',None)
    temp = kwargs.get('grf_temp',None)
    
    reward_dict = dict()
    if grfdelta:
        DEFAULT_WEIGHTS['grfdetla'] = grfdelta
    if Grf:
        DEFAULT_WEIGHTS['grf'] = Grf
    if temp:
        DEFAULT_WEIGHTS['temp'] = temp

    for key in DEFAULT_WEIGHTS:
        function = getattr(first,key,False)
        if function:
            reward_dict[key] = function(model,head_body,grf)
    
    return _sum_weight_and_rwd(weights=DEFAULT_WEIGHTS,rwd_dict=reward_dict)