import sys

from deprl.custom_trainer import Trainer
from . import logger as logger
import time

import os
import numpy as np
import sys
import keyboard
from deprl.custom_test_environment import (
    test_dm_control,
    test_mujoco,
    test_scone,
)

def on_key_press(event):
    if event.name == 'q' and keyboard.is_pressed('ctrl'):
        logger.error("KeyboardInterrupt")
        raise KeyboardInterrupt
    
class MyTrainer(Trainer):
    '''
    내가 직접 만든 Trainer deprl에서 수정함te

    '''
    def __init__(self, steps=10000000, epoch_steps=20000, save_steps=500000, test_episodes=20, show_progress=False, replace_checkpoint=False):
        super().__init__(steps, epoch_steps, save_steps, test_episodes, show_progress, replace_checkpoint)
    
    def initialize(self, agent, environment, test_environment=None, full_save=False):
        return super().initialize(agent, environment, test_environment, full_save)
    
    def setting(self, reward_weight):
        self.environment.setting(reward_weight)
        self.test_environment.setting(reward_weight)

    def run(self, params, steps=0, epochs=0, episodes=0):
        """Runs the main training loop."""

        # Start the environments.
        observations, muscle_states = self.environment.start()

        num_workers = len(observations)
        scores = np.zeros(num_workers)
        lengths = np.zeros(num_workers, int)
        self.steps, epoch_steps = steps, 0
        steps_since_save = 0
        
        # start time
        self.total_starttime = time.time()
        self.epoch_starttime = time.time()
        
        while True:
                keyboard.on_press(on_key_press)
            # Select actions.
                if hasattr(self.agent, "expl"):
                    greedy_episode = (not episodes % self.agent.expl.test_episode_every)
                else:
                    greedy_episode = None
                assert not np.isnan(observations.sum())
                actions = self.agent.step(
                    observations, self.steps, muscle_states, greedy_episode
                )
                assert not np.isnan(actions.sum())
                logger.store("train/action", actions, stats=True)

                # Take a step in the environments.
                observations, muscle_states, info = self.environment.step(actions)
                if "env_infos" in info:
                    info.pop("env_infos")
                self.agent.update(**info, steps=self.steps)

                scores += info["rewards"]
                lengths += 1
                self.steps += num_workers
                epoch_steps += num_workers
                steps_since_save += num_workers
                # Check the finished episodes.
                for i in range(num_workers):
                    if info["resets"][i]:
                        logger.store("train/episode_score", scores[i], stats=True)
                        logger.store("train/episode_length", lengths[i], stats=True)
                        if i == 0:
                            # adaptive energy cost
                            if hasattr(self.agent.replay, "action_cost"):
                                logger.store(
                                    "train/action_cost_coeff",
                                    self.agent.replay.action_cost,
                                )
                                self.agent.replay.adjust(scores[i])
                        scores[i] = 0
                        lengths[i] = 0
                        episodes += 1

                # End of the epoch.
                if epoch_steps >= self.epoch_steps:
                    # Evaluate the agent on the test environment.
                    if self.test_environment:
                        if "control"in str(type(self.test_environment.environments[0].unwrapped)).lower():
                            _ = test_dm_control(self.test_environment, self.agent, steps, params)

                        elif "scone"in str(type(self.test_environment.environments[0].unwrapped)).lower():
                            _ = test_scone(self.test_environment, self.agent, steps, params)

                        else:
                            _ = test_mujoco(self.test_environment, self.agent, steps, params)

                    # Log the data.
                    epochs += 1
                    logger.store("train/episodes", episodes)
                    logger.store("train/epochs", epochs)
                    logger.store("train/epoch_steps", epoch_steps)
                    logger.store("train/steps", self.steps)
                    logger.store("First", True) if epochs==1 else logger.store("First", False)
                    
                    logger.dump()
                    # epoch time 출력
                    self.epoch_endtime = time.time()
                    logger.timeprinting(epochs,self.epoch_starttime,self.epoch_endtime)
                    #초기화
                    self.epoch_starttime = time.time()
                    epoch_steps = 0

                # End of training.
                stop_training = self.steps >= self.max_steps

                # Save a checkpoint.
                if stop_training or steps_since_save >= self.save_steps:
                    path = os.path.join(logger.get_path(), "checkpoints")
                    if os.path.isdir(path) and self.replace_checkpoint:
                        for file in os.listdir(path):
                            if file.startswith("step_"):
                                os.remove(os.path.join(path, file))
                    checkpoint_name = f"step_{self.steps}"
                    save_path = os.path.join(path, checkpoint_name)
                    # save agent checkpoint
                    self.agent.save(save_path, full_save=self.full_save)
                    # save logger checkpoint
                    logger.save(save_path)
                    # save time iteration dict
                    self.save_time(save_path, epochs, episodes)
                    steps_since_save = self.steps % self.save_steps
                    print("-" * 30)
                    logger.log(f"Saved a checkpoint when Epochs: {epochs}")
                    print("-" * 30)

                if stop_training:
                    self.close_mp_envs()
                    return scores
