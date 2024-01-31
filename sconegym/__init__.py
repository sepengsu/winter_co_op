import os
from gym.envs.registration import register
curr_dir = os.path.dirname(os.path.abspath(__file__))

import os
from gym.envs.registration import register

#  New Environments
register(id="sconewalk_change_model-v1",
         entry_point="sconegym.gaitgym:GaitGym",
         kwargs={
             'model_file': curr_dir + '/data-v1/H1622_trunkfix.scone',
             'obs_type': '3D',
             'left_leg_idxs': [6, 7, 8, 9, 10],
             'right_leg_idxs': [11, 12, 13, 14, 15],
             'clip_actions': True,
             'run': False,
             'target_vel': 1.2,
             'leg_switch': True,
             'rew_keys':{
                "vel_coeff": 10,
                "grf_coeff": -0.07281,
                "joint_limit_coeff": -0.1307,
                "smooth_coeff": -0.097,
                "nmuscle_coeff": -1.57929,
                "self_contact_coeff": 0.0,
             }
         }
        )

register(id="sconewalk_h1622-range-v1",
         entry_point="sconegym.gaitgym:GaitGym",
         kwargs={
             'model_file': curr_dir + '/data-v1/H1622.scone',
             'obs_type': '3D',
             'left_leg_idxs': [6, 7, 8, 9, 10],
             'right_leg_idxs': [11, 12, 13, 14, 15],
             'clip_actions': True,
             'run': False,
             'target_vel': [1.2-0.1, 1.2+0.1],
             'leg_switch': True,
             'rew_keys':{
                "vel_coeff": 10,
                "grf_coeff": -0.07281,
                "joint_limit_coeff": -0.1307,
                "smooth_coeff": -0.097,
                "nmuscle_coeff": -1.57929,
                "self_contact_coeff": 0.0,
             }
         }
        )


register(id="sconewalk_h1922-v1",
         entry_point="sconegym.gaitgym:GaitGym",
         kwargs={
             'model_file': curr_dir + '/data-v1/H1922.scone',
             'obs_type': '3D',
             'left_leg_idxs': [6, 7, 8, 9, 10],
             'right_leg_idxs': [11, 12, 13, 14, 15],
             'clip_actions': True,
             'run': False,
             'target_vel': 1.2,
             'leg_switch': True,
             'rew_keys':{
                "vel_coeff": 10,
                "grf_coeff": -0.07281,
                "joint_limit_coeff": -0.1307,
                "smooth_coeff": -0.097,
                "nmuscle_coeff": -1.57929,
                "self_contact_coeff": 0.0,
             }
         }
        )

# Walk Environments
register(id="sconewalk_h0918-v1",
         entry_point="sconegym.gaitgym:GaitGym",
         kwargs={
             'model_file': curr_dir + '/data-v1/H0918.scone',
             'obs_type': '2D',
             'left_leg_idxs': [3, 4, 5],
             'right_leg_idxs': [6, 7, 8],
             'clip_actions': True,
             'run': False,
             'target_vel': 1.2,
             'leg_switch': True,
             'rew_keys':{
                "vel_coeff": 10,
                "grf_coeff": -0.07281,
                "joint_limit_coeff": -0.1307,
                "smooth_coeff": -0.097,
                "nmuscle_coeff": -1.57929,
                "self_contact_coeff": 0.0,
             }
         }
        )

register(id="sconewalk_h1622-v1",
         entry_point="sconegym.gaitgym:GaitGym",
         kwargs={
             'model_file': curr_dir + '/data-v1/H1622.scone',
             'obs_type': '3D',
             'left_leg_idxs': [6, 7, 8, 9, 10],
             'right_leg_idxs': [11, 12, 13, 14, 15],
             'clip_actions': True,
             'run': False,
             'target_vel': 1.2,
             'leg_switch': True,
             'rew_keys':{
                "vel_coeff": 10,
                "grf_coeff": -0.07281,
                "joint_limit_coeff": -0.1307,
                "smooth_coeff": -0.097,
                "nmuscle_coeff": -1.57929,
                "self_contact_coeff": 0.0,
             }
         }
        )

register(id="sconewalk_h2190-v1",
         entry_point="sconegym.gaitgym:GaitGym",
         kwargs={
             'model_file': curr_dir + '/data-v1/H2190.scone',
             'obs_type': '3D',
             'left_leg_idxs': [6, 7, 8, 9, 10, 11],
             'right_leg_idxs': [12, 13, 14, 15, 16, 17],
             'clip_actions': True,
             'run': False,
             'target_vel': 1.2,
             'leg_switch': True,
             'rew_keys':{
                "vel_coeff": 10,
                "grf_coeff": -0.07281,
                "joint_limit_coeff": -0.1307,
                "smooth_coeff": -0.097,
                "nmuscle_coeff": -1.57929,
                "self_contact_coeff": 0.0,
             }
         },
        )

