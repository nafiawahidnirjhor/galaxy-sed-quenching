import numpy as np
import matplotlib.pyplot as plt


def plot_sfh(age, tau, massformed, output_file=None):
    """
    Plot the delayed-tau star formation history.

    Shows:
    - SFH curve
    - Peak SFR
    - Current SFR
    - Time since SFH peak
    """

    mass = 10 ** massformed

    integral = tau**2 * (
        1.0 - (1.0 + age / tau) * np.exp(-age / tau)
    )

    normalization = mass / integral

    time = np.linspace(0.0, age, 500)

    sfr = (
        normalization
        * time
        * np.exp(-time / tau)
        / 1e9
    )

    peak_sfr = (
        normalization
        * tau
        * np.exp(-1.0)
        / 1e9
    )

    current_sfr = (
        normalization
        * age
        * np.exp(-age / tau)
        / 1e9
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        time,
        sfr,
        linewidth=2,
        label="Fitted SFH"
    )

    ax.scatter(
        [tau],
        [peak_sfr],
        s=60,
        zorder=5,
        label=f"Peak SFR = {peak_sfr:.2f} M☉/yr"
    )

    ax.scatter(
        [age],
        [current_sfr],
        s=60,
        zorder=5,
        label=f"Current SFR = {current_sfr:.2f} M☉/yr"
    )

    ax.axvline(
        tau,
        linestyle="--",
        alpha=0.5
    )

    ax.set_xlabel(
        "Time since onset of star formation [Gyr]"
    )

    ax.set_ylabel(
        "SFR [M☉ yr⁻¹]"
    )

    ax.set_title(
        "Fitted Delayed-τ Star Formation History"
    )

    ax.legend()

    ax.grid(
        alpha=0.3
    )

    fig.tight_layout()

    if output_file is not None:
        fig.savefig(
            output_file,
            dpi=150,
            bbox_inches="tight"
        )
        plt.close(fig)

    return fig, ax
