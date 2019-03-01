from npc import Robot2D
from error import *
from filterpy.kalman import KalmanFilter
import numpy as np


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    dt = 0.05
    kf = KalmanFilter(4, 2, 1)
    r = Robot2D()

    r.move(10, (3, 0))
    r.move(1, (0, 3))
    kf.x = r.cur_state #+ np.array([0, 0, 50, 0]).reshape(4, 1)
    kf.F = r.get_F_and_B(dt)[0]
    kf.H = r.get_H()
    kf.R = np.diag([1e6, 1e6])

    gts = []
    priors = []
    posts = []
    noised = []
    errors = []
    vars = []
    diffs = []
    for idx in xrange(500):
        r.move(dt, (1, 0))
        kf.predict()
        priors.append(kf.x_prior)
        e = normal_error(0, 100, (2, 1))
        # e = np.array([[jump_error(0.2, 50)], [0]]) + normal_error(0, 1, (2, 1))
        z = r.cur_state[:2] + e
        noised.append(z)
        kf.update(r.cur_state[:2] + e)

        # diff = kf.x_post - kf.x_prior
        # if np.linalg.norm(diff[2:]) > .5:  # speed diff
        #     suppressed_diff = diff[2:] / np.linalg.norm(diff[2:]) * .5
        #     kf.x[2:] = kf.x_prior[2:] + suppressed_diff
        # if np.linalg.norm(diff[:2]) > 3:
        #     suppressed_diff = diff[:2] / np.linalg.norm(diff[:2]) * 3
        #     kf.x[:2] = kf.x_prior[:2] + suppressed_diff

        gts.append(r.cur_state)
        posts.append(kf.x)
        errors.append(kf.x_prior - r.cur_state)
        vars.append(kf.P)
        diffs.append(kf.x - kf.x_prior)

    ts = r.history_ts
    gts = np.array(gts).squeeze()
    posts = np.array(posts).squeeze()
    priors = np.array(priors).squeeze()
    noised = np.array(noised).squeeze()
    var_conds = np.array([np.linalg.cond(p) for p in vars])
    diffs = np.array(diffs).squeeze()

    fig, axs = plt.subplots(4, 1, sharex=True)
    axs[0].plot(gts[:, 0], gts[:, 1], label='gt')
    axs[0].plot(posts[:, 0], posts[:, 1], label='update')
    axs[0].plot(priors[:, 0], priors[:, 1], label='predict')
    axs[0].plot(noised[:, 0], noised[:, 1], '*', label='obs')
    axs[0].legend(loc='best')
    axs[0].set_title('position')

    axs[1].plot(gts[:, 0], gts[:, 2], label='gt')
    axs[1].plot(posts[:, 0], posts[:, 2], label='update')
    axs[1].plot(priors[:, 0], priors[:, 2], label='predict')
    axs[1].legend(loc='best')
    axs[1].set_title('x speed')

    errors = np.array(errors).squeeze()
    axs[2].plot(gts[:, 0], np.linalg.norm(errors[:, :2], axis=1), label='loc error')
    axs[2].plot(gts[:, 0], np.linalg.norm(diffs[:, :2], axis=1), label='loc update')
    # var_ax = axs[2].twinx()
    # var_ax.plot(gts[:, 0], var_conds, label='condition # of P')
    axs[2].legend(loc='best')

    axs[3].plot(gts[:, 0], np.linalg.norm(errors[:, 2:], axis=1), label='speed error')
    axs[3].plot(gts[:, 0], np.linalg.norm(diffs[:, 2:], axis=1), label='speed update')
    axs[3].legend(loc='best')

    plt.xlabel('x')
    plt.suptitle('normal kf w/ jump error & large measurement noise')
    plt.show()
    plt.waitforbuttonpress(-1)
