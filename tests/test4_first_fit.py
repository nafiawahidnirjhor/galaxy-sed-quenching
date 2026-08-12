import pandas as pd
import numpy as np
import bagpipes
import os

# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = "data/raw/sdss_specphoto_100.csv"

TARGET_ID = 1237648720142401611

FILTER_LIST = [
    "data/filters/u.dat",
    "data/filters/g.dat",
    "data/filters/r.dat",
    "data/filters/i.dat",
    "data/filters/z.dat",
]

# ============================================================
# LOAD SDSS DATA
# ============================================================

df = pd.read_csv(DATA_FILE, skiprows=1)
df["objID"] = df["objID"].astype(np.int64)

target = df[df["objID"] == TARGET_ID].iloc[0]
redshift = float(target["z"])

print("===== TARGET =====")
print("ID:", TARGET_ID)
print("Redshift:", redshift)

# ============================================================
# BAGPIPES LOAD FUNCTION
# ============================================================

bands = ["u", "g", "r", "i", "z"]


def load_data(ID):

    ID = int(ID)

    row = df[df["objID"] == ID].iloc[0]

    fluxes = []
    errors = []

    for band in bands:

        mag = float(row[f"modelMag_{band}"])
        mag_err = float(row[f"modelMagErr_{band}"])

        # AB magnitude -> microJy
        flux = 10 ** ((23.9 - mag) / 2.5)

        # Magnitude error -> flux error
        flux_err = (
            flux * np.log(10) / 2.5 * mag_err
        )

        fluxes.append(flux)
        errors.append(flux_err)

    return np.column_stack([
        np.array(fluxes),
        np.array(errors)
    ])


# ============================================================
# DISPLAY PHOTOMETRY
# ============================================================

photometry = load_data(TARGET_ID)

print("\n===== PHOTOMETRY =====")

for i, band in enumerate(bands):

    print(
        f"{band}: "
        f"{photometry[i, 0]:.4f} +/- "
        f"{photometry[i, 1]:.4f} microJy"
    )


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
    out_units="ergscma"
)

print("\n===== BAGPIPES INPUT =====")
print("Galaxy created successfully.")
print("Photometry shape:", galaxy.photometry.shape)
print(galaxy.photometry)


# ============================================================
# FIT INSTRUCTIONS
# ============================================================

fit_instructions = {

    "delayed": {
        "age": (0.1, 10.0),
        "tau": (0.1, 10.0),
        "metallicity": (0.0, 2.5),
        "massformed": (7.0, 12.0)
    },

    "dust": {
        "type": "Calzetti",
        "Av": (0.0, 3.0)
    },

    "nebular": {
        "logU": (-3.0, -1.0)
    },

    "redshift": redshift
}


# ============================================================
# RUN FIT
# ============================================================

RUN_DIR = "test4_first_fit"

os.makedirs(RUN_DIR, exist_ok=True)

print("\n===== BAGPIPES FIT =====")
print("Starting fit...")

fit = bagpipes.fit(
    galaxy,
    fit_instructions,
    run=RUN_DIR,
    n_posterior=500
)

fit.fit(verbose=True)

print("\n===== FIT COMPLETE =====")
print("BAGPIPES fitting finished successfully.")


# ============================================================
# OUTPUT
# ============================================================

print("\n===== FIT OUTPUT =====")

try:

    fit.plot_spectrum_posterior(
        show=True
    )

except Exception as e:

    print("Spectrum posterior plot unavailable:")
    print(e)

try:

    fit.plot_corner(
        show=True
    )

except Exception as e:

    print("Corner plot unavailable:")
    print(e)

print("\n===== DONE =====")
