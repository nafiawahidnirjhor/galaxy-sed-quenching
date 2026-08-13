import h5py
import numpy as np

# ============================================================
# CONFIGURATION
# ============================================================

GALAXY_ID = "1237648720142401611"

POSTERIOR_FILE = (
    f"pipes/posterior/test4_first_fit/"
    f"{GALAXY_ID}.h5"
)

PARAMETERS = [
    "delayed:age",
    "delayed:massformed",
    "delayed:metallicity",
    "delayed:tau",
    "dust:Av",
    "nebular:logU",
]

# ============================================================
# READ POSTERIOR
# ============================================================

with h5py.File(POSTERIOR_FILE, "r") as f:

    median = f["median"][:]
    conf_int = f["conf_int"][:]
    samples = f["samples2d"][:]

# ============================================================
# PRINT RESULTS
# ============================================================

print("===== POSTERIOR SUMMARY =====")
print("Galaxy:", GALAXY_ID)
print("Number of posterior samples:", samples.shape[0])
print("Number of parameters:", samples.shape[1])

print("\n===== PARAMETERS =====")

for i, name in enumerate(PARAMETERS):

    median_value = median[i]
    lower = conf_int[0, i]
    upper = conf_int[1, i]

    print(
        f"{name:25s} "
        f"{median_value:.4f} "
        f"[{lower:.4f}, {upper:.4f}]"
    )

# ============================================================
# SANITY CHECK
# ============================================================

print("\n===== SANITY CHECK =====")

print("Median array:")
print(median)

print("\nConfidence interval array:")
print(conf_int)

print("\nPosterior sample shape:")
print(samples.shape)
