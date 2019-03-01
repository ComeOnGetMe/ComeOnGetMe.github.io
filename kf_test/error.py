import numpy as np


def gaussian(*args, **kwargs):
    return np.random.normal(*args, **kwargs)


def discrete(probs, vals, **kwargs):
    return np.random.choice(vals, p=probs, **kwargs)
