from customreward.measureLua.grfdetla import GRFBefore
from customreward.measureLua import vector_scale
from customreward.measureLua.grfdetla import delta_all


def grfdelta(model,head_body,grf:GRFBefore):
    '''
    force는 contact_force를 활용함 
    기존코드에서는 normalize를 75.1646*9.80665을 활용함 
    이는 mass*gravity으로 보여짐 
    
    '''
    foot_l = model.bodies()[7]
    foot_r = model.bodies()[4]
    foot_l_force = foot_l.contact_load()
    foot_r_force = foot_r.contact_load()
   
    # 1. 계산
    impact_left = delta_all(foot_l_force,grf.calcn_l,1.0)
    impact_right = delta_all(foot_r_force,grf.calcn_r,1.0)

    # update grf
    grf.update(model)

    return impact_left + impact_right

def grf(model,head_body,grf):
    return 0

