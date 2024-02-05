from myutils.kwargs_utils import _sum_weight_and_rwd
TIME_WETGHTS = {
    'livetime':0
}


def livetime():
    return 1

def totalreward(model,head_body,grf,prev_excs,**kwargs):
    '''
    model: env.model
    head_body: env.head_body
    grf: env.grf
    prev_excs: env.prev_excs
    weight: weight dictionary
    -> weight를 변경하기 위해서는 아래의 파라미터를 설정해야함
    kwargs: 
        - timealive_livetime : 1
    return: reward
    '''
    #change weight
    alive_livetime = kwargs.get('alive_livetime',False)
    if alive_livetime:
        TIME_WETGHTS['livetime'] = alive_livetime
    
    rwd_dict = dict()
    rwd_dict['livetime'] = livetime()

    return _sum_weight_and_rwd(TIME_WETGHTS,rwd_dict)
