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
    'w1': 0.097, # action smoothing
    'w2': 1.579, # number of active muscles above 15% activity
    'w3': 0.131, # joint limit torque
    'w4': 0.073,  # GRFs above 1.2 BW
    "delta_alpha": 9e-4, # change in adaptation rate
    "theta" :1000, # performance threshold
    "beta" : 0.8,# running avg. smoothing
    "labmda": 0.9# decay term
}
from ..measureLua import limitforce

def total_reward(model, head_body,prev_excs,parameters = PARA):
    '''
    논문참조 : https://arxiv.org/pdf/2309.02976.pdf
    https://sites.google.com/view/naturalwalkingrl

    '''
    r = r_vel(model) - c_effort(model,head_body,prev_excs,parameters['w1'],parameters['w2'],parameters) - c_pain(model,model.bodies(),parameters['w3'],parameters['w4'])

    return r

def r_vel(model,v_target = 1.2):
    if model.com_vel().x <v_target:
        r = np.exp(-(model.com_vel().x-v_target)**2)
    else:
        r = 1
    return r

def c_effort(model,head_body,prev_excs,w1:float,w2:float,parameters:dict):
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

def c_pain(model,bodies:list,w3:float,w4:float):
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