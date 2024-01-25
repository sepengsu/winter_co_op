from customreward.measureLua.grfdetla import GRFBefore
from customreward.measureLua import vector_scale
from customreward.measureLua.grfdetla import delta_all


def grfdelta(model,grf:GRFBefore):
    '''
    force는 contact_force를 활용함 
    기존코드에서는 normalize를 75.1646*9.80665을 활용함 
    이는 mass*gravity으로 보여짐 
    '''
    foot_l = model.bodies()[7]
    foot_r = model.bodies()[4]
    foot_l_force = foot_l.contact_force()
    foot_r_force = foot_r.contact_force()
    
    #norm_factor  = 75.1646*9.80665
    norm_factor = model.mass()*vector_scale(model.gravity().array())
   
    # 1. 계산
    impact_left = delta_all(foot_l_force,grf.calcn_l,norm_factor)
    impact_right = delta_all(foot_r_force,grf.calcn_r,norm_factor)
    
    return impact_left + impact_right

def grfdelta_x(model,grf:GRFBefore):
    '''
    force는 contact_force의 x부분만을 활용함 
    기존코드에서는 normalize를 75.1646*9.80665을 활용함 
    이는 mass*gravity으로 보여짐 
    '''
    norm_factor = model.mass()*vector_scale(model.gravity().array())
    foot_l = model.bodies()[7]
    foot_r = model.bodies()[4]
    foot_l_force = foot_l.contact_force().x
    foot_r_force = foot_r.contact_force().x

    impact_left = _x_all(foot_l_force,grf.calcn_l.x,norm_factor)   
    impact_right = _x_all(foot_r_force,grf.calcn_r.x,norm_factor)

    return impact_left + impact_right

def grf(model,grf:GRFBefore):
    return 0

def _x_all(foot_force,grf,norm_factor):
    '''
    foot_force : foot의 force
    grf : grf의 위치
    norm_factor : normalize factor
    '''
    return abs((foot_force-grf)/norm_factor)

