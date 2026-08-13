import numpy as np
import pandas as pd
import bagpipes

# ============================================================
# CONFIGURATION
# ============================================================

MOCK_FILE = "data/mock/mock_delayed_tau.csv"

FILTER_LIST = [
    "data/filters/u.dat",
    "data/filters/g.dat",
    "data/filters/r.dat",
    "data/filters/i.dat",
    "data/filters/z.dat",
]

TARGET_ID = "mock_delayed_tau"

REDSHIFT = 0.05

# ============================================================
# LOAD MOCK DATA
# ============================================================

df = pd.read_csv(MOCK_FILE)

fluxes = df["flux_microJy"].to_numpy()
errors = df["error_microJy"].to_numpy()

print("===== MOCK DATA =====")
print("Fluxes:", fluxes)
print("Errors:", errors)

# ============================================================
# BAGPIPES LOAD FUNCTION
# ============================================================

def load_data(ID):
    return np.column_stack([fluxes, errors])

# ============================================================
# CREATE BAGPIPES GALAXY
# ============================================================

galaxy = bagpipes.galaxy(
    TARGET_ID,
    load_data=load_data,
    spectrum_exists=False,
    photometry_exists=True,
    filt_list=FILTER_LIST,
    phot_units="mujy",
    out_units="ergscma",
)

print("\n===== BAGPIPES INPUT =====")
print("Photometry:")
print(galaxy.photometry)

# ============================================================
# FIT INSTRUCTIONS
# ============================================================

fit_instructions = {
    "delayed": {
        "age": (0.5, 10.0),
        "tau": (0.1, 5.0),
        "metallicity": (0.0, 2.5),
        "massformed": (8.0, 12.0),
    },

    "dust": {
        "type": "Calzetti",
        "Av": (0.0, 3.0),
    },

    "nebular": {
        "logU": (-3.0, -1.0),
    },

    "redshift": REDSHIFT,
}

# ============================================================
# FIT
# ============================================================

print("\n===== MOCK RECOVERY FIT =====")
print("Starting BAGPIPES fit...")

fit = bagpipes.fit(
    galaxy,
    fit_instructions,
    run="test10_mock_recovery",
    n_posterior=500,
)

fit.fit(verbose=True)

print("\n===== FIT COMPLETE =====")
print("Mock recovery fit finished.")
