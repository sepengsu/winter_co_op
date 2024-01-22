from deprl.custom_distributed import Sequential, Parallel



class MySequential(Sequential):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setting(self, coeff_dict):
        self.coeff_dict = coeff_dict

class MyParallel(Parallel): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setting(self, coeff_dict):
        self.coeff_dict = coeff_dict


# 이 코드는 deprl/custom_distributed.py 에서 가져옴
def proc(
    action_pipe,
    output_queue,
    group_seed,
    build_dict,
    max_episode_steps,
    index,
    workers,
    env_args,
    header,
):
    """Process holding a sequential group of environments."""
    envs = MySequential(build_dict, max_episode_steps, workers, env_args, header)
    envs.initialize(group_seed)

    observations = envs.start()
    output_queue.put((index, observations))

    while True:
        actions = action_pipe.recv()
        out = envs.step(actions)
        output_queue.put((index, out))

def distribute(
    environment,
    tonic_conf,
    env_args,
    parallel=None,
    sequential=None,
):
    """Distributes workers over parallel and sequential groups."""
    parallel = tonic_conf["parallel"] if parallel is None else parallel
    sequential = tonic_conf["sequential"] if sequential is None else sequential
    build_dict = dict(
        env=environment, parallel=parallel, sequential=sequential
    )

    dummy_environment = build_env_from_dict(build_dict)
    max_episode_steps = dummy_environment._max_episode_steps
    del dummy_environmentd

    if parallel < 2:
        return MySequential(
            build_dict=build_dict,
            max_episode_steps=max_episode_steps,
            workers=sequential,
            env_args=env_args,
            header=tonic_conf["header"],
        )
    return MyParallel(
        build_dict,
        worker_groups=parallel,
        workers_per_group=sequential,
        max_episode_steps=max_episode_steps,
        env_args=env_args,
        header=tonic_conf["header"],
    )


def build_env_from_dict(build_dict):
    assert build_dict["env"] is not None
    if type(build_dict) == dict:
        from deprl import env_tonic_compat

        return env_tonic_compat(**build_dict)
    else:
        return build_dict()
