from npc import *
from error import *
from filterpy.kalman import KalmanFilter
import numpy as np


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    dt = 0.05
    kf = KalmanFilter(2, 1, 1)
    r = Robot1D(x0=(0, 30))

    kf.x = r.cur_state + np.array([0, 30]).reshape(2, 1)
    kf.F = r.get_F_and_B(dt)[0]
    kf.H = r.get_H()
    kf.R = np.diag([1e3])

    measure_errors = [discrete([.2, .8], [50, 0]) + gaussian(0, 1) for _ in xrange(30)] + [0] * 200
    gts = []
    priors = []
    posts = []
    noised = []
    errors = []
    vars = []
    diffs = []
    for idx, e in enumerate(measure_errors):
        r.move(dt, 0)
        kf.predict()
        priors.append(kf.x_prior)
        z = r.cur_state[0] + e
        noised.append(z)
        kf.update(r.cur_state[0] + e)

        diff = kf.x_post - kf.x_prior
        if abs(diff[1]) > .5:  # speed diff
            suppressed_diff = diff[1] / np.linalg.norm(diff[1]) * .5
            kf.x[1] = kf.x_prior[1] + suppressed_diff
        if abs(diff[0]) > 3:
            suppressed_diff = diff[0] / np.linalg.norm(diff[0]) * 3
            kf.x[0] = kf.x_prior[0] + suppressed_diff

        gts.append(r.cur_state)
        posts.append(kf.x)
        errors.append(kf.x_prior - r.cur_state)
        vars.append(kf.P)
        diffs.append(kf.x - kf.x_prior)

    ts = r.history_ts[1:]
    gts = np.array(gts).squeeze()
    posts = np.array(posts).squeeze()
    priors = np.array(priors).squeeze()
    noised = np.array(noised).squeeze()
    var_conds = np.array([np.linalg.cond(p) for p in vars])
    diffs = np.array(diffs).squeeze()

    fig, axs = plt.subplots(4, 1, sharex=True)
    axs[0].plot(ts, gts[:, 0], label='gt')
    axs[0].plot(ts, posts[:, 0], label='update')
    axs[0].plot(ts, priors[:, 0], label='predict')
    axs[0].plot(ts, noised, '*', label='obs')
    axs[0].legend(loc='best')
    axs[0].set_title('position')

    axs[1].plot(ts, gts[:, 1], label='gt')
    axs[1].plot(ts, posts[:, 1], label='update')
    axs[1].plot(ts, priors[:, 1], label='predict')
    axs[1].legend(loc='best')
    axs[1].set_title('speed')

    errors = np.array(errors).squeeze()
    axs[2].plot(ts, errors[:, 0], label='loc error')
    axs[2].plot(ts, diffs[:, 0], label='loc update')
    # var_ax = axs[2].twinx()
    # var_ax.plot(gts[:, 0], var_conds, label='condition # of P')
    axs[2].legend(loc='best')

    axs[3].plot(ts, errors[:, 1], label='speed error')
    axs[3].plot(ts, diffs[:, 1], label='speed update')
    axs[3].legend(loc='best')

    plt.xlabel('ts')
    plt.suptitle('normal kf w/ jump error & large measurement noise')
    plt.show()
    plt.waitforbuttonpress(-1)
