
from deprl.utils.load_utils import load_checkpoint

def load(path, environment, checkpoint="last"):
    config, checkpoint_path, _ = load_checkpoint(path, checkpoint)
    header = config["tonic"]["header"]
    agent = config["tonic"]["agent"]
    # Run the header
    exec(header)
    # Build the agent.
    agent = eval(agent)
    # Adapt mpo specific settings
    if "mpo_args" in config:
        agent.set_params(**config["mpo_args"])
    # Initialize the agent.
    agent.initialize(
        observation_space=environment.observation_space,
        action_space=environment.action_space,
    )
    # Load the weights of the agent form a checkpoint.
    agent.load(checkpoint_path, only_checkpoint=True)
    return agent
