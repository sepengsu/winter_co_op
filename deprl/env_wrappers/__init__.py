import deprl, myutils  # noqa
from deprl.env_wrappers.dm_wrapper import DMWrapper, OstrichDMWrapper
from deprl.env_wrappers.gym_wrapper import GymWrapper
from deprl.env_wrappers.scone_wrapper import SconeWrapper
from myutils.environments.custom_wrapper import MyWrapper, ActuatorWrapper, ClipCustomWrapper, MotorWarpper

def apply_wrapper(env):
    if 'fix_clip' in str(env).lower():
        return ClipCustomWrapper(env)
    elif "actuator" in str(env).lower():
        return ActuatorWrapper(env)
    elif 'motor' in str(env).lower():
        return MotorWarpper(env)
    elif "1925" in str(env).lower():
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
