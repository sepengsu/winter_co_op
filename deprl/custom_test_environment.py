import numpy as np

from deprl.vendor.tonic import logger


def test_mujoco(env, agent, steps, params=None, test_episodes=10):
    """
    Tests the agent on the test environment.
    """
    # Start the environment.
    if not hasattr(env, "test_observations"):
        # Dont use dep in evaluation
        env.test_observations, _ = env.start()
        assert len(env.test_observations) == 1

    eval_rwd_metrics = (
        True if hasattr(env.environments[0], "rwd_dict") else False
    )

    # Test loop.
    for _ in range(test_episodes):
        metrics = {
            "test/episode_score": 0,
            "test/episode_length": 0,
            "test/effort": 0,
            "test/terminated": 0,
        }
        if eval_rwd_metrics:
            rwd_metrics = {k: [] for k in env.environments[0].rwd_dict.keys()}

        while True:
            # Select an action.
            actions = agent.test_step(env.test_observations, steps)
            assert not np.isnan(actions.sum())
            logger.store("test/action", actions, stats=True)

            # Take a step in the environment.
            env.test_observations, _, info = env.step(actions)

            # Update metrics
            metrics["test/episode_score"] += info["rewards"][0]
            metrics["test/episode_length"] += 1

            if env.environments[0].sim.model.na > 0:
                metrics["test/effort"] += np.mean(
                    np.square(env.environments[0].unwrapped.sim.data.act)
                )
            metrics["test/terminated"] += int(info["terminations"])
            if eval_rwd_metrics:
                for k, v in env.environments[0].rwd_keys_wt.items():
                    rwd_metrics[k].append(v * env.environments[0].rwd_dict[k])

            if info["resets"][0]:
                break
        # Log the data.Average over episode length here
        metrics["test/terminated"] /= metrics["test/episode_length"]
        metrics["test/effort"] /= metrics["test/episode_length"]
        if eval_rwd_metrics:
            for k, v in rwd_metrics.items():
                metrics["test/rwd_metrics/" + k] = np.sum(v)
        # average over episodes in logger
        for k, v in metrics.items():
            logger.store(k, v, stats=True)
    return metrics


def test_dm_control(env, agent, steps, params=None, test_episodes=10):
    """
    Tests the agent on the test environment.
    """
    # Start the environment.
    if not hasattr(env, "test_observations"):
        # Dont use dep in evaluation
        env.test_observations, _ = env.start()
        assert len(env.test_observations) == 1

    max_reward = 0
    # Test loop.
    for _ in range(test_episodes):
        metrics = {
            "test/episode_score": 0,
            "test/episode_length": 0,
            "test/effort": 0,
            "test/terminated": 0,
        }

        while True:
            # Select an action.
            actions = agent.test_step(env.test_observations, steps)
            assert not np.isnan(actions.sum())
            logger.store("test/action", actions, stats=True)

            # Take a step in the environment.
            env.test_observations, _, info = env.step(actions)

            # Update metrics
            metrics["test/episode_score"] += info["rewards"][0]
            metrics["test/episode_length"] += 1
            metrics["test/effort"] += np.mean(
                np.square(env.environments[0].muscle_activity())
            )
            metrics["test/terminated"] += int(info["terminations"])
            max_reward = max(max_reward, info["rewards"][0])

            if info["resets"][0]:
                break
        # Log the data.Average over episode length here
        metrics["test/terminated"] /= metrics["test/episode_length"]
        metrics["test/effort"] /= metrics["test/episode_length"]
        # average over episodes in logger
        for k, v in metrics.items():
            logger.store(k, v, stats=True)
    # max over all episodes
    logger.store("test/max_reward", max_reward, stats=False)
    return metrics


def test_scone(env, agent, steps, params=None, test_episodes=10):
    """
    Tests the agent on the test environment.
    """
    # Start the environment.
    if not hasattr(env, "test_observations"):
        # Dont use dep in evaluation
        env.test_observations, _ = env.start()
        assert len(env.test_observations) == 1
    # this creates the rwd_dict
    env.environments[0].custom_reward()

    # eval_rwd_metrics = (
    #     True if hasattr(env.environments[0], "rwd_dict") else False
    # )
    eval_rwd_metrics =False #  metric 없애기

    # Test loop.
    for _ in range(test_episodes):
        metrics = {
            "test/episode_score": 0,
            "test/episode_length": 0,
            "test/effort": 0,
            "test/terminated": 0,
        }
        if eval_rwd_metrics:
            rwd_metrics = {k: [] for k in env.environments[0].rwd_dict.keys()}
        while True:
            # Select an action.
            actions = agent.test_step(env.test_observations, steps)
            assert not np.isnan(actions.sum())
            logger.store("test/action", actions, stats=True)

            # Take a step in the environment.
            env.test_observations, _, info = env.step(actions)

            # Update metrics
            metrics["test/episode_score"] += info["rewards"][0]
            metrics["test/episode_length"] += 1
            metrics["test/effort"] += np.mean(
                np.square(env.environments[0].model.muscle_activation_array())
            )
            metrics["test/terminated"] += int(info["terminations"])

            if eval_rwd_metrics:
                for k, v in env.environments[0].rwd_dict.items():
                    rwd_metrics[k].append(v)

            if info["resets"][0]:
                break
        # Log the data.Average over episode length here
        metrics["test/terminated"] /= metrics["test/episode_length"]
        metrics["test/effort"] /= metrics["test/episode_length"]

        if eval_rwd_metrics:
            for k, v in rwd_metrics.items():
                metrics["test/rwd_metrics/" + k] = np.sum(v)
        # average over episodes in logger
        for k, v in metrics.items():
            logger.store(k, v, stats=True)
    return metrics
