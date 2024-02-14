"""Environment wrappers."""

import gym
import numpy as np
import logging

class ActionRescaler(gym.ActionWrapper):
    """Rescales actions from [-1, 1]^n to the true action space.
    The baseline agents return actions in [-1, 1]^n."""

    def __init__(self, env):
        assert isinstance(env.action_space, gym.spaces.Box)
        super().__init__(env)
        high = np.ones(env.action_space.shape, dtype=np.float32)
        high[-3:] = 1000
        self.action_space = gym.spaces.Box(low=-high, high=high)
        true_low = env.action_space.low
        true_high = env.action_space.high
        self.bias = (true_high + true_low) / 2
        self.scale = (true_high - true_low) / 2

    def action(self, action):
        lumbar = action[-3:]
        muscle = action[:-3]
        muscle = self.bias[:-3] + self.scale[:-3] * np.clip(muscle, -1, 1)
        action = np.concatenate([muscle, lumbar])
        return action

class ActionRescaler22(gym.ActionWrapper):
    def __init__(self, env):
        assert isinstance(env.action_space, gym.spaces.Box)
        super().__init__(env)
        high = np.ones(env.action_space.shape, dtype=np.float32)
        high[-3:] = 1000
        self.action_space = gym.spaces.Box(low=-high, high=high)
        true_low = env.action_space.low
        true_high = env.action_space.high
        self.bias = (true_high + true_low) / 2
        self.scale = (true_high - true_low) / 2
        
    def action(self, action):
        return self.bias + self.scale * np.clip(action, -1, 1)