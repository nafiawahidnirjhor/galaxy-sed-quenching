import numpy as np


def calculate_diagnostics(age, tau, massformed):
    """
    Calculate delayed-tau SFR and quenching diagnostics.

    Parameters
    ----------
    age : float
        Galaxy age in Gyr.
    tau : float
        Delayed-tau timescale in Gyr.
    massformed : float
        log10 of formed stellar mass in solar masses.
    """

    mass = 10 ** massformed

    integral = tau**2 * (
        1.0 - (1.0 + age / tau) * np.exp(-age / tau)
    )

    normalization = mass / integral

    current_sfr = (
        normalization
        * age
        * np.exp(-age / tau)
        / 1e9
    )

    peak_sfr = (
        normalization
        * tau
        * np.exp(-1.0)
        / 1e9
    )

    ssfr = current_sfr / mass

    current_to_peak = current_sfr / peak_sfr

    return {
        "stellar_mass": mass,
        "sfr": current_sfr,
        "ssfr": ssfr,
        "peak_sfr": peak_sfr,
        "current_to_peak_sfr": current_to_peak,
        "time_since_peak": max(age - tau, 0.0),
    }
