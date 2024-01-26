import os
import numpy as np
# Set non-random initial muscle activations
import sys
# Add sconepy folders to path
if sys.platform.startswith("win"):
    sys.path.append("C:/Program Files/SCONE/bin")
elif sys.platform.startswith("linux"):
    sys.path.append("/opt/scone/lib")
elif sys.platform.startswith('darwin'):
    sys.path.append("/Applications/SCONE.app/Contents/MacOS/lib")

import sconepy
PARA={
    'w1': 0, # action smoothing
    'w2': 0, # number of active muscles above 15% activity
    'w3': 0, # joint limit torque
    'w4': 0.073,  # GRFs above 1.2 BW
    "delta_alpha": 0, # change in adaptation rate
    "theta" :0, # performance threshold
    "beta" : 0,# running avg. smoothing
    "labmda": 0# decay term
}
def totalreward(model, head_body,grf,prev_excs,**kwargs):
    '''
    논문참조 : https://arxiv.org/pdf/2309.02976.pdf
    https://sites.google.com/view/naturalwalkingrl
    Sconegym에 구현되어 있음 - 그대로 사용 

    keyward arguments:
    model: env.model
    head_body: env.head_body
    prev_excs: env.prev_excs
    ** kwargs:
        deprlpaper_w1: w1 - action smoothing
        deprlpaper_w2: w2 - number of active muscles above 15% activity
        deprlpaper_w3: w3 - joint limit torque
        deprlpaper_w4: w4 - GRFs above 1.2 BW
        deprlpaper_delta_alpha: delta_alpha - change in adaptation rate
        deprlpaper_theta: theta - performance threshold
        deprlpaper_beta: beta - running avg. smoothing
        deprlpaper_labmda: labmda - decay term
    '''
    w1 = kwargs.get('deprlpaper_w1',False)
    w2 = kwargs.get('deprlpaper_w2',False)
    w3 = kwargs.get('deprlpaper_w3',False)
    w4 = kwargs.get('deprlpaper_w4',False)
    delta_alpha = kwargs.get('deprlpaper_delta_alpha',False)
    theta = kwargs.get('deprlpaper_theta',False)
    beta = kwargs.get('deprlpaper_beta',False)
    labmda = kwargs.get('deprlpaper_labmda',False)

    if w1:
        PARA['w1'] = float(w1)
    if w2:
        PARA['w2'] = float(w2)
    if w3:
        PARA['w3'] = float(w3)
    if w4:
        PARA['w4'] = float(w4)
    if delta_alpha:
        PARA['delta_alpha'] = float(delta_alpha)
    if theta:
        PARA['theta'] = float(theta)
    if beta:
        PARA['beta'] = float(beta)
    if labmda:
        PARA['labmda'] = float(labmda)
    
    r = r_vel(model) - c_effort(model,prev_excs,PARA['w1'],PARA['w2']) - c_pain(model,PARA['w3'],PARA['w4'])

    return r

def r_vel(model,v_target = 1.2):
    if model.com_vel().x <v_target:
        r = np.exp(-(model.com_vel().x-v_target)**2)
    else:
        r = 1
    return r

def c_effort(model,prev_excs,w1:float,w2:float):
    #a =np.sqrt(np.sum(model.muscle_excitation_array()**2))**3
    a = 0
    u= model.muscle_excitation_array()
    u_prev = prev_excs
    delta_excs = u-u_prev
    delta_excs = _vector_sum(delta_excs)
    N_active = _vector_sum(model.muscle_activation_array())
    c = a**3 +w1*(delta_excs)**2 + w2*N_active
    #c  = alpha_t()a**3 +w1*(u-u_prev)**2 + w2*N_active
    return c

def c_pain(model,w3:float,w4:float):
    limit_torque = [item.limit_torque().array() for item in model.joints()]
    sum_tau = all_com_sum(limit_torque)
    foot_l = model.bodies()[7].contact_force().array()
    foot_r = model.bodies()[4].contact_force().array()
    sum_f = _vector_sum(foot_l)+ _vector_sum(foot_r)
    c = w3*sum_tau + w4*sum_f
    return c


def all_com_sum(List: list):
    s = 0
    for item in List:
        s+= _vector_sum(item)
    return s
def _vector_sum(vector:np.array):
    return np.sqrt(np.sum(vector**2))