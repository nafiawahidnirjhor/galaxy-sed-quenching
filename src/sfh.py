import numpy as np


def delayed_sfh(age, tau, time):
    """
    Delayed-tau star formation history.

    Parameters
    ----------
    age : float
        Galaxy age in Gyr.
    tau : float
        SFH timescale in Gyr.
    time : array-like
        Time since onset of star formation in Gyr.

    Returns
    -------
    numpy.ndarray
        SFH shape, normalized to its maximum.
    """

    time = np.asarray(time, dtype=float)

    sfh = np.zeros_like(time)

    mask = (time >= 0.0) & (time <= age)

    t = time[mask]

    sfh[mask] = t * np.exp(-t / tau)

    if np.max(sfh) > 0:
        sfh /= np.max(sfh)

    return sfh
