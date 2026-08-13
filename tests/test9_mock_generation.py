import os
import numpy as np
import bagpipes

FILTER_LIST = [
    "data/filters/u.dat",
    "data/filters/g.dat",
    "data/filters/r.dat",
    "data/filters/i.dat",
    "data/filters/z.dat",
]

MOCK_DIR = "data/mock"
os.makedirs(MOCK_DIR, exist_ok=True)

redshift = 0.05

model_components = {
    "redshift": redshift,

    "delayed": {
        "age": 5.0,
        "tau": 1.0,
        "massformed": 10.5,
        "metallicity": 0.2,
    },

    "dust": {
        "type": "Calzetti",
        "Av": 0.8,
    },

    "nebular": {
        "logU": -2.0,
    },
}

print("===== MOCK GALAXY GENERATION =====")
print("Redshift:", redshift)

model = bagpipes.model_galaxy(
    model_components,
    filt_list=FILTER_LIST,
    phot_units="mujy",
)

model_flux = np.asarray(model.photometry)
effective_wavelengths = np.asarray(model.filter_set.eff_wavs)

print("\n===== MODEL OUTPUT =====")
print("Photometry:", model_flux)
print("Photometry shape:", model_flux.shape)

bands = ["u", "g", "r", "i", "z"]

print("\n===== SYNTHETIC PHOTOMETRY =====")

for band, wavelength, flux in zip(
    bands,
    effective_wavelengths,
    model_flux
):
    print(
        f"{band}: "
        f"{wavelength:.2f} A, "
        f"{flux:.6f} microJy"
    )

fractional_error = 0.05
errors = model_flux * fractional_error

rng = np.random.default_rng(12345)

observed_flux = rng.normal(
    model_flux,
    errors
)

print("\n===== NOISY MOCK OBSERVATION =====")

for band, flux, error in zip(
    bands,
    observed_flux,
    errors
):
    print(
        f"{band}: "
        f"{flux:.6f} +/- {error:.6f} microJy"
    )

output_file = os.path.join(
    MOCK_DIR,
    "mock_delayed_tau.csv"
)

data = np.column_stack([
    effective_wavelengths,
    observed_flux,
    errors,
])

np.savetxt(
    output_file,
    data,
    delimiter=",",
    header="wavelength_A,flux_microJy,error_microJy",
    comments=""
)

print("\n===== SAVED =====")
print(output_file)
