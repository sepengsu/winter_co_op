

DEFAULT_WEIGHTS ={
    'grfdelta': 1,
    'grf' : 0
}
def totalreward(model,head_hody,grf,prev_excs,**kwargs):
    '''
    여기서는 크게 3가지로 나눠서 계산한다.
    '''
    typesdelta = kwargs.get('grf_types',None)
    grfdelta = kwargs.get('grf_grfdelta',None)
    Grf = kwargs.get('grf_grf',None)
    if grfdelta:
        DEFAULT_WEIGHTS['grfdetla'] = grfdelta
    if Grf:
        DEFAULT_WEIGHTS['grf'] = Grf
    