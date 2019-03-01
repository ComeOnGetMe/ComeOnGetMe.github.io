import numpy as np


def normal_error(*args, **kwargs):
    return np.random.normal(*args, **kwargs)


def jump_error(p, jump):
    return (np.random.uniform(0, 1) < p) * jump
