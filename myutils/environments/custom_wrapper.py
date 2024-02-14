from deprl.env_wrappers.scone_wrapper import SconeWrapper
import numpy as np
from deprl.vendor.tonic import logger

class MyWrapper(SconeWrapper):
    def __init__(self, env):
        super().__init__(env)
    
    def render(self, *args, **kwargs):
        pass

    def write_now(self):
        if self.unwrapped.store_next:
            self.model.write_results(
                self.output_dir, f"{self.episode:05d}_{self.total_reward:.3f}"
            )
        self.episode += 1
        self.unwrapped.store_next = False

    
    def step(self, action):
        try:
            observation, reward, done, info = self._inner_step(action)
            if np.any(np.isnan(observation)):
                raise self.error("NaN detected! Resetting.")

        except self.error as e:
            logger.log(f"Simulator exception thrown: {e}")
            observation = self.last_observation
            reward = 0
            done = 1
            info = {}
            self.reset()
        return observation, reward, done, info


    def _inner_step(self, action):
        """
        takes an action and advances environment by 1 step.
        Changed to allow for correct sto saving.
        """
        try:
            if not self.unwrapped.has_reset:
                raise Exception("You have to call reset() once before step()")
            muscle , lumbar = action[:-3] , action[-3:]
            if self.unwrapped.clip_actions:
                muscle= np.clip(muscle, 0, 0.5)
            else:
                muscle = np.clip(muscle, 0, 1.0)
                
            action = np.concatenate([muscle, lumbar])    
            if self.unwrapped.use_delayed_actuators:
                self.unwrapped.model.set_delayed_actuator_inputs(action)
            else:
                self.unwrapped.model.set_actuator_inputs(action)

            self.unwrapped.model.advance_simulation_to(self.time + self.step_size)
            reward = self.unwrapped._get_rew()
            obs = self.unwrapped._get_obs()
            done = self.unwrapped._get_done()
            self.unwrapped.time += self.step_size
            self.unwrapped.total_reward += reward
            return obs, reward, done, {}
        except Exception as e:
            raise e

    @property
    def _max_episode_steps(self):
        return 1000

    @property
    def results_dir(self):
        return self.unwrapped.results_dir
    
    
class ActuatorWarpper(SconeWrapper):
    def __init__(self, env):
        super().__init__(env)
    
    def render(self, *args, **kwargs):
        pass

    def write_now(self):
        if self.unwrapped.store_next:
            self.model.write_results(
                self.output_dir, f"{self.episode:05d}_{self.total_reward:.3f}"
            )
        self.episode += 1
        self.unwrapped.store_next = False

    
    def step(self, action):
        try:
            observation, reward, done, info = self._inner_step(action)
            if np.any(np.isnan(observation)):
                raise self.error("NaN detected! Resetting.")

        except self.error as e:
            logger.log(f"Simulator exception thrown: {e}")
            observation = self.last_observation
            reward = 0
            done = 1
            info = {}
            self.reset()
        return observation, reward, done, info


    def _inner_step(self, action):
        """
        takes an action and advances environment by 1 step.
        Changed to allow for correct sto saving.
        """
        try:
            if not self.unwrapped.has_reset:
                raise Exception("You have to call reset() once before step()")
            muscle = action
            if self.unwrapped.clip_actions:
                muscle= np.clip(muscle, 0, 0.5)
            else:
                muscle = np.clip(muscle, 0, 1.0)
            
            act = self.unwrapped.get_actuator()
            action = np.concatenate([muscle, act])
            if self.unwrapped.use_delayed_actuators:
                self.unwrapped.model.set_delayed_actuator_inputs(action)
            else:
                self.unwrapped.model.set_actuator_inputs(action)

            self.unwrapped.model.advance_simulation_to(self.time + self.step_size)
            reward = self.unwrapped._get_rew()
            obs = self.unwrapped._get_obs()
            done = self.unwrapped._get_done()
            self.unwrapped.time += self.step_size
            self.unwrapped.total_reward += reward
            return obs, reward, done, {}
        except Exception as e:
            raise e