import numpy as np


def monetary_reward_per_timestep(agent_vars):
    """
    Calculate the sum of monetary reward per timestep in the simulation.
    The rewards are as follows
        - unsuccessful: 0
        - successful & fraudulent: -amount
        - successful & genuine: 0.25*amount + 0.25
    :param agent_vars: 
    :return: 
    """
    num_steps = 366*24
    rewards = np.zeros(num_steps)
    for step in range(num_steps):
        try:
            success = np.array(agent_vars.loc[step]['Success'], dtype=float)
            fraud = np.array(agent_vars.loc[step]['Target'], dtype=float)
            amount = np.array(agent_vars.loc[step]['Amount'], dtype=float)

            # calculate reward
            reward = fraud * (-amount)
            reward += (1 - fraud) * (0.025 * amount + 0.25)
            reward *= success

            rewards[step] = np.sum(reward)
        except KeyError:
            pass
    return rewards


def satisfaction_reward_per_timestep(agent_vars):
    """
    Get the satisfaction reward (i.e., estimated satisfaction from view
    of the agent) per timestep.
    The rewards are as follows:
        - transaction aborted, >0 authentication: 0
        - genuine transaction, 0 authentication: +1
        - fraudulent transaction, 0 authentication: -1
        - genuine transaction, >0 authentication: -0.5
    :param agent_vars: 
    :return: 
    """
    num_steps = 366*24
    rewards = np.zeros(num_steps)
    for step in range(num_steps):
        try:
            success = np.array(agent_vars.loc[step]['Success'], dtype=float)
            auth_steps = np.array(agent_vars.loc[step]['AuthSteps'], dtype=float)
            fraud = np.array(agent_vars.loc[step]['Target'], dtype=float)

            # calculate reward
            reward = - fraud * np.array(auth_steps == 0, dtype=int)
            reward += (1 - fraud) * np.array(auth_steps == 0, dtype=int)
            reward += 0.5 * (1 - fraud) * np.array(auth_steps > 0, dtype=int)
            reward *= success

            rewards[step] = np.sum(reward)
        except KeyError:
            pass
    return rewards


def satisfaction_per_timestep(model_vars):
    """
    Get the true mean satisfaction of the users per timestep.
    :param model_vars: 
    :return: 
    """
    num_steps = 366*24
    sum_satisfactions = np.zeros(num_steps)
    for step in range(num_steps):
        try:
            satisfaction = model_vars.loc[step]['Satisfaction']
            sum_satisfactions[step] = np.sum(satisfaction)
        except KeyError:
            pass
    return sum_satisfactions
