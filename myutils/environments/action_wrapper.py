"""Environment wrappers."""

import gym
import numpy as np
import logging


# Configure logging to save the output to a file
logging.basicConfig(filename='log.log', level=logging.DEBUG)

class ActionRescaler(gym.ActionWrapper):
    """Rescales actions from [-1, 1]^n to the true action space.
    The baseline agents return actions in [-1, 1]^n."""

    def __init__(self, env):
        assert isinstance(env.action_space, gym.spaces.Box)
        super().__init__(env)
        high = np.ones(env.action_space.shape, dtype=np.float32)
        high[-3:] = 30
        self.action_space = gym.spaces.Box(low=-high, high=high)
        true_low = env.action_space.low
        true_high = env.action_space.high
        self.bias = (true_high + true_low) / 2
        self.scale = (true_high - true_low) / 2
        # logging.info(f'bias: {self.bias}')
        # logging.info(f'scale: {self.scale}')

    def action(self, action):
        # muscle, lumbar = action[:-3], action[-3:]
        # # muscle = 0.5 + 0.5 * muscle # 0~1로 변환
        # lumbar = 30*lumbar # -2~2로 변환
        # action = np.concatenate([muscle, lumbar])
        return self.bias + self.scale * np.clip(action, -1, 1)