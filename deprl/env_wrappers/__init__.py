import deprl, myutils  # noqa
from deprl.env_wrappers.dm_wrapper import DMWrapper, OstrichDMWrapper
from deprl.env_wrappers.gym_wrapper import GymWrapper
from deprl.env_wrappers.scone_wrapper import SconeWrapper
from myutils.environments.custom_wrapper import MyWrapper, ActuatorWarpper


def apply_wrapper(env):
    if 'fix' in str(env).lower():
        return SconeWrapper(env)
    elif "act" in str(env).lower() or 'motor' in str(env).lower():
        return ActuatorWarpper(env)
    elif "1922" in str(env).lower():
        return MyWrapper(env)
    elif "scone" in str(env).lower():
        return SconeWrapper(env)
    else:
        return GymWrapper(env)


def env_tonic_compat(env, id=5, parallel=1, sequential=1):
    """
    Applies wrapper for tonic and passes random seed.
    """
    return apply_wrapper(eval(env))


__all__ = [env_tonic_compat, apply_wrapper]
