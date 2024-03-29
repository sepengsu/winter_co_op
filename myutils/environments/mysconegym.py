import os
# Set non-random initial muscle activations
import sys
from abc import ABC, abstractmethod
from typing import Optional

import gym
import numpy as np
from myutils.actuator import flex

# Add sconepy folders to path
if sys.platform.startswith("win"):
    sys.path.append("C:/Program Files/SCONE/bin")
elif sys.platform.startswith("linux"):
    sys.path.append("/opt/scone/lib")
elif sys.platform.startswith('darwin'):
    sys.path.append("/Applications/SCONE.app/Contents/MacOS/lib")

from customreward import rewardfunction
from customreward import GRFBefore
from sconegym.gaitgym import GaitGym

import sconepy

def find_model_file(model_file):
    this_dir, this_file = os.path.split(__file__)
    return os.path.join(this_dir, "data", model_file)


DEFAULT_REW_KEYS = {
    "vel_coeff": 10,
    "grf_coeff": -0.073,
    "joint_limit_coeff": -0.131,
    "smooth_coeff": 0.0,
    "nmuscle_coeff": -1.579,
    "self_contact_coeff":0.0,
}

class Gait1925(GaitGym):
        
    def step(self, action):
        """
        takes an action and advances environment by 1 step.
        """
        muscle , lumbar = action[:-3] , action[-3:]
        if self.clip_actions:
            muscle = np.clip(muscle, 0, 0.5)
        else:
            muscle = np.clip(muscle, 0, 1.0)
        if not self.has_reset:
            raise Exception("You have to call reset() once before step()")
        
        action = np.concatenate([muscle, lumbar])
        if self.use_delayed_actuators:
            self.model.set_delayed_actuator_inputs(action)
        else:
            self.model.set_actuator_inputs(action)

        self.model.advance_simulation_to(self.time + self.step_size)
        reward = self._get_rew()
        obs = self._get_obs() # prev_acts, prev_excs, GRFBefore 업데이트 
        done = self._get_done()
        reward = self._apply_termination_cost(reward, done)
        self.time += self.step_size
        self.total_reward += reward
        if done : # done하는 경우 에피소드를 끝낸다.
            if self.store_next:
                self.model.write_results(
                    self.output_dir, f"{self.episode:05d}_{self.total_reward:.3f}"
                )
                self.store_next = False
            self.episode += 1
        # 그리고 한 step마다 grf를 업데이트 한다.
        return obs, reward, done, {}
    
    def _setup_action_observation_spaces(self):
        num_act = len(self.model.actuators())
        low = np.ones(shape=(num_act,))*-1
        low[-3:] = -1000
        high = np.ones(shape=(num_act,))
        high[-3:] = 1000
        self.action_space = gym.spaces.Box(
            low=low,high=high,dtype=np.float32
        )

        self.observation_space = gym.spaces.Box(
            low=-10000, high=10000, shape=self._get_obs().shape, dtype=np.float32
        )
    
    def _get_active_muscles(self, threshold):
        """
        Get the number of muscles whose activations is above the threshold.
        """
        return (
            np.sum(
                np.where(self.model.muscle_activation_array() > threshold)[0].shape[0]
            )
            / self.model.muscle_activation_array().shape[0]
        )
    


class Gait1922Actuator(Gait1925):
    def __init__(self, model_file,rwd_type_weights ='',rwd_weights='', *args, **kwargs):
        super().__init__(model_file, *args, **kwargs)
        self._resetup_action_observation_spaces()

    def get_actuator(self):
        torso = self.model.bodies()[-1]
        return flex.pdcontrol(torso)
    
    def _resetup_action_observation_spaces(self):
        num_act = len(self.model.muscles())
        self.action_space = gym.spaces.Box(
            low=np.zeros(shape=(num_act,)),
            high=np.ones(shape=(num_act,)),
            dtype=np.float32,
        )
        self.observation_space = gym.spaces.Box(
            low=-10000, high=10000, shape=self._get_obs().shape, dtype=np.float32
        )

    def step(self, action):
        """
        takes an action and advances environment by 1 step.
        """
        muscle = action 
        if self.clip_actions:
            muscle = np.clip(muscle, 0, 0.5)
        else:
            muscle = np.clip(muscle, 0, 1.0)
        if not self.has_reset:
            raise Exception("You have to call reset() once before step()")
        lumbar = self.get_actuator()
        action = np.concatenate([muscle, lumbar])
        if self.use_delayed_actuators:
            self.model.set_delayed_actuator_inputs(action)
        else:
            self.model.set_actuator_inputs(action)

        self.model.advance_simulation_to(self.time + self.step_size)
        reward = self._get_rew()
        obs = self._get_obs() # prev_acts, prev_excs, GRFBefore 업데이트 
        done = self._get_done()
        reward = self._apply_termination_cost(reward, done)
        self.time += self.step_size
        self.total_reward += reward
        if done : # done하는 경우 에피소드를 끝낸다.
            if self.store_next:
                self.model.write_results(
                    self.output_dir, f"{self.episode:05d}_{self.total_reward:.3f}"
                )
                self.store_next = False
            self.episode += 1
        # 그리고 한 step마다 grf를 업데이트 한다.
        return obs, reward, done, {}
    
    def _get_active_muscles(self, threshold):
        """
        Get the number of muscles whose activations is above the threshold.
        """
        return (
            np.sum(
                np.where(self.model.muscle_activation_array() > threshold)[0].shape[0]
            )
            / self.model.muscle_activation_array().shape[0]
        )
    

class Gait1922Motor(GaitGym):
    def __init__(self, model_file,rwd_type_weights ='',rwd_weights='', *args, **kwargs):
        super().__init__(model_file, *args, **kwargs)
        self._resetup_action_observation_spaces()
        self.rwd_type_weights = rwd_type_weights if len(rwd_type_weights)>0 else None
        self.rwd_weights = rwd_weights if len(rwd_weights)>0 else None

    def _resetup_action_observation_spaces(self):
        num_act = len(self.model.muscles())
        self.action_space = gym.spaces.Box(
            low=np.zeros(shape=(num_act,)),
            high=np.ones(shape=(num_act,)),
            dtype=np.float32,
        )
        self.observation_space = gym.spaces.Box(
            low=-10000, high=10000, shape=self._get_obs().shape, dtype=np.float32
        )
    
    def _get_active_muscles(self, threshold):
        """
        Get the number of muscles whose activations is above the threshold.
        """
        return (
            np.sum(
                np.where(self.model.muscle_activation_array() > threshold)[0].shape[0]
            )
            / self.model.muscle_activation_array().shape[0]
        )
    
    def step(self, action):
        """
        takes an action and advances environment by 1 step.
        """
        if self.clip_actions:
            action = np.clip(action, 0, 0.5)
        else:
            action = np.clip(action, 0, 1.0)
        if not self.has_reset:
            raise Exception("You have to call reset() once before step()")
        lumbar = np.array([0,0,0])
        action = np.concatenate([action, lumbar])
        if self.use_delayed_actuators:
            self.model.set_delayed_actuator_inputs(action)
        else:
            self.model.set_actuator_inputs(action)

        self.model.advance_simulation_to(self.time + self.step_size)
        reward = self._get_rew()
        obs = self._get_obs() # prev_acts, prev_excs, GRFBefore 업데이트 
        done = self._get_done()
        reward = self._apply_termination_cost(reward, done)
        self.time += self.step_size
        self.total_reward += reward
        if done : # done하는 경우 에피소드를 끝낸다.
            if self.store_next:
                self.model.write_results(
                    self.output_dir, f"{self.episode:05d}_{self.total_reward:.3f}"
                )
                self.store_next = False
            self.episode += 1
        # 그리고 한 step마다 grf를 업데이트 한다.
        return obs, reward, done, {}

class GaitClipCustom(GaitGym):
    def __init__(self, model_file,clip_actions = True, max_activation = 0.5,*args, **kwargs):
        super().__init__(model_file, *args, **kwargs)
        self._setup_action_observation_spaces()
        self.clip_actions = clip_actions
        self.max_activation = max_activation

    def step(self, action):
        """
        takes an action and advances environment by 1 step.
        """
        if self.clip_actions:
            action = np.clip(action, 0, self.max_activation)
        else:
            action = np.clip(action, 0, 1.0)
        if not self.has_reset:
            raise Exception("You have to call reset() once before step()")
        
        if self.use_delayed_actuators:
            self.model.set_delayed_actuator_inputs(action)
        else:
            self.model.set_actuator_inputs(action)

        self.model.advance_simulation_to(self.time + self.step_size)
        reward = self._get_rew()
        obs = self._get_obs() # prev_acts, prev_excs, GRFBefore 업데이트 
        done = self._get_done()
        reward = self._apply_termination_cost(reward, done)
        self.time += self.step_size
        self.total_reward += reward
        if done : # done하는 경우 에피소드를 끝낸다.
            if self.store_next:
                self.model.write_results(
                    self.output_dir, f"{self.episode:05d}_{self.total_reward:.3f}"
                )
                self.store_next = False
            self.episode += 1
        # 그리고 한 step마다 grf를 업데이트 한다.
        return obs, reward, done, {}

        