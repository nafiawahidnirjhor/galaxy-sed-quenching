import pandas as pd
import numpy as np
import bagpipes

DATA_FILE = "data/raw/sdss_specphoto_100.csv"

# Keep SDSS objID as STRING. Never allow pandas to convert it to float.
df = pd.read_csv(
    DATA_FILE,
    skiprows=1,
    dtype={"objID": "string"}
)

df["objID"] = df["objID"].str.strip()


# ---------------------------------------------------------
# Select first galaxy
# ---------------------------------------------------------

target = df.iloc[0]
TARGET_ID = target["objID"]

print("===== SDSS GALAXY =====")
print("objID:", TARGET_ID)
print("redshift:", target["z"])


# ---------------------------------------------------------
# Magnitude -> microJy
# ---------------------------------------------------------

def mag_to_microjy(mag, mag_err):
    flux = 3631.0 * 10 ** (-0.4 * mag) * 1e6
    flux_err = flux * np.log(10) * 0.4 * mag_err
    return flux, flux_err


# ---------------------------------------------------------
# BAGPIPES data loader
# ---------------------------------------------------------

def load_data(ID):

    ID = str(ID)

    # BAGPIPES may pass the ID back as scientific notation.
    if "e" in ID.lower():
        ID = str(int(float(ID)))

    matches = df[df["objID"] == ID]

    if len(matches) == 0:
        raise ValueError(
            f"Galaxy ID not found: {ID}\n"
            f"Available first ID: {df.iloc[0]['objID']}"
        )

    galaxy = matches.iloc[0]

    mags = [
        galaxy["modelMag_u"],
        galaxy["modelMag_g"],
        galaxy["modelMag_r"],
        galaxy["modelMag_i"],
        galaxy["modelMag_z"],
    ]

    errors = [
        galaxy["modelMagErr_u"],
        galaxy["modelMagErr_g"],
        galaxy["modelMagErr_r"],
        galaxy["modelMagErr_i"],
        galaxy["modelMagErr_z"],
    ]

    photometry = []

    for mag, err in zip(mags, errors):
        flux, flux_err = mag_to_microjy(mag, err)
        photometry.append([flux, flux_err])

    return np.array(photometry)


# ---------------------------------------------------------
# Print photometry
# ---------------------------------------------------------

phot = load_data(TARGET_ID)

print("\n===== PHOTOMETRY =====")

for band, values in zip(
    ["u", "g", "r", "i", "z"],
    phot
):
    print(
        f"{band}: "
        f"{values[0]:.4f} +/- {values[1]:.4f} microJy"
    )


# ---------------------------------------------------------
# BAGPIPES galaxy object
# ---------------------------------------------------------

filt_list = [
    "data/filters/u.dat",
    "data/filters/g.dat",
    "data/filters/r.dat",
    "data/filters/i.dat",
    "data/filters/z.dat",
]

galaxy = bagpipes.galaxy(
    TARGET_ID,
    load_data=load_data,
    phot_units="mujy",
    spectrum_exists=False,
    photometry_exists=True,
    filt_list=filt_list,
)

print("\n===== BAGPIPES INPUT =====")
print("BAGPIPES galaxy created successfully.")
print("ID:", galaxy.ID)
print("Photometry shape:", galaxy.photometry.shape)
print("Photometry:")
print(galaxy.photometry)
