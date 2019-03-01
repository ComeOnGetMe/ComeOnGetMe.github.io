import numpy as np
import logging


class RobotBase(object):
    def __init__(self, t0=0., x0=None):
        self.x0 = x0
        self.t0 = t0

        self._t = self.t0
        self._x = np.reshape(np.array(self.x0), (-1, 1))
        self._history_ts = [self._t]
        self._history_states = [self._x]
        self._actions = []

        self.dim_x = len(self._x)
        self.dim_z = len(self._x) / 2
        self.dim_u = len(self._x) / 2

    @property
    def cur_ts(self):
        return self._t

    @property
    def cur_state(self):
        return self._x

    @property
    def history_ts(self):
        return self._history_ts

    @property
    def history_states(self):
        return self._history_states

    @classmethod
    def get_F_and_B(cls, dt):
        raise NotImplementedError()

    @classmethod
    def get_H(cls):
        raise NotImplementedError()

    def move(self, dt, u=None):
        _u = np.array(u).reshape(self.dim_u, 1)
        self._actions.append((self._t, dt, _u))

        self._t += dt
        F, B = self.get_F_and_B(dt)
        self._x = F.dot(self._x) + B.dot(_u)

        self._history_ts.append(self._t)
        self._history_states.append(self._x)


class Robot1D(RobotBase):
    def __init__(self, t0=0., x0=(0, 0)):
        super(Robot1D, self).__init__(t0=t0, x0=x0)

    @classmethod
    def get_F_and_B(cls, dt):
        F = np.array([[1, dt],
                      [0, 1]])
        B = np.array([[dt ** 2 / 2.],
                      [dt]])
        return F, B

    @classmethod
    def get_H(cls):
        return np.array([[1, 0]])


class Robot2D(RobotBase):
    logger = logging.getLogger('Robot2D')

    def __init__(self, t0=0., x0=(0, 0, 0, 0)):
        super(Robot2D, self).__init__(t0=t0, x0=x0)

    @classmethod
    def get_F_and_B(cls, dt):
        F = np.array([[1, 0, dt, 0],
                      [0, 1, 0, dt],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])
        B = np.array([[dt ** 2 / 2., 0],
                      [0, dt ** 2 / 2.],
                      [dt, 0],
                      [0, dt]])
        return F, B

    @classmethod
    def get_H(cls):
        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0]])
