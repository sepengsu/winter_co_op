MEASURELUA_WEIGHTS = {'Gait': 100,
 'Effort': -1.3079,
 'ActivationSquared': -0.0009657,
 'HeadAcceleration': -1.1628,
 'GRFJerk': -0.2494,
 'KneeLimitForce': -0.25,
 'DoLimits': -0.1}
import customreward.measureLua as lua
from myutils.kwargs_utils import _sum_weight_and_rwd

def totalreward(model,head_body,grf,prev_excs,**kwargs):
    ''' 제시되어
    논문에  있는 함수를 lua로 코딩되어 있는 것들을 파이썬으로 바꾼다. 
    참조 논문: https://www.sciencedirect.com/science/article/pii/S0021929021003110?via%3Dihub
    coefficient는 추후 수정 예정
    input 설명
    model: env.model, head_body: env.head_body
    grf: env.grf

    kwargs:
    - measureLua_Gait : Gait
    - measureLua_Effort: Effort
    - measureLua_ActivationSquared: ActivationSquared
    - measureLua_HeadAcceleration: HeadAcceleration
    - measureLua_GRFJerk: GRFJerk
    - measureLua_KneeLimitForce: KneeLimitForce
    - measureLua_DoLimits: DoLimits

    # 2024.01.02
    GRF 미분을 위하여 전 step에서의 grf 정보를 추가함 (함수에서 grf으로 추가)
    # 2024.01.02
    python_scone에서 파일 수정 및 함수 적용 완료
     
    # 2024.01.03
    coeff 관련 문제가 발생함. 중요도에 따른 조정해야함 
    '''
    #change weight
    eff_type = kwargs.get('measure_Lua_efftype','TotalForce')
    Gait = kwargs.get('measureLua_Gait',False)
    Effort = kwargs.get('measureLua_Effort',False)
    ActivationSquared = kwargs.get('measureLua_ActivationSquared',False)
    HeadAcceleration = kwargs.get('measureLua_HeadAcceleration',False)
    GRFJerk = kwargs.get('measureLua_GRFJerk',False)
    KneeLimitForce = kwargs.get('measureLua_KneeLimitForce',False)
    DoLimits = kwargs.get('measureLua_DoLimits',False)
    if Gait:
        MEASURELUA_WEIGHTS ['Gait'] = Gait
    if Effort:
        MEASURELUA_WEIGHTS ['Effort'] = Effort
    if ActivationSquared:
        MEASURELUA_WEIGHTS ['ActivationSquared'] = ActivationSquared
    if HeadAcceleration:
        MEASURELUA_WEIGHTS ['HeadAcceleration'] = HeadAcceleration
    if GRFJerk:
        MEASURELUA_WEIGHTS ['GRFJerk'] = GRFJerk
    if KneeLimitForce:
        MEASURELUA_WEIGHTS ['KneeLimitForce'] = KneeLimitForce
    if DoLimits:
        MEASURELUA_WEIGHTS ['DoLimits'] = DoLimits

    
    rwd_dict = dict()
    names = list(MEASURELUA_WEIGHTS.keys())
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
    return _sum_weight_and_rwd(MEASURELUA_WEIGHTS ,rwd_dict)