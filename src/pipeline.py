import os

from src.fitting import read_posterior
from src.diagnostics import calculate_diagnostics
from src.plotting import plot_sfh


def analyze_posterior(posterior_file, output_dir="figures"):
    posterior = read_posterior(posterior_file)

    age = posterior["delayed:age"]["median"]
    tau = posterior["delayed:tau"]["median"]
    massformed = posterior["delayed:massformed"]["median"]

    diagnostics = calculate_diagnostics(
        age,
        tau,
        massformed
    )

    os.makedirs(output_dir, exist_ok=True)

    sfh_file = os.path.join(
        output_dir,
        "sfh.png"
    )

    plot_sfh(
        age,
        tau,
        massformed,
        sfh_file
    )

    return {
        "posterior": posterior,
        "diagnostics": diagnostics,
        "sfh_plot": sfh_file,
    }
