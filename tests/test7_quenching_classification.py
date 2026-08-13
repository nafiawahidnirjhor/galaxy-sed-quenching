import h5py
import numpy as np

# ============================================================
# CONFIGURATION
# ============================================================

GALAXY_ID = 1237648720142401611

POSTERIOR = (
    f"pipes/posterior/test4_first_fit/"
    f"{GALAXY_ID}.h5"
)

# ============================================================
# LOAD POSTERIOR
# ============================================================

with h5py.File(POSTERIOR, "r") as f:

    samples = f["samples2d"][:]

# Columns from BAGPIPES posterior
age = samples[:, 0]          # Gyr
massformed = samples[:, 1]   # log10(Msun)
metallicity = samples[:, 2]
tau = samples[:, 3]          # Gyr
Av = samples[:, 4]
logU = samples[:, 5]

# ============================================================
# DELAYED SFH
# ============================================================

def sfr_at_time(t, tau):
    """
    Delayed exponential SFH:
        SFR(t) proportional to t exp(-t/tau)
    """
    return t * np.exp(-t / tau)


# Current SFR is evaluated at galaxy age.
sfr_now_relative = sfr_at_time(age, tau)

# Peak occurs at t = tau.
sfr_peak_relative = sfr_at_time(tau, tau)

# Ratio
sfr_ratio = sfr_now_relative / sfr_peak_relative

# ============================================================
# QUENCHING DIAGNOSTIC
# ============================================================

ratio50 = np.percentile(sfr_ratio, 50)
ratio16 = np.percentile(sfr_ratio, 16)
ratio84 = np.percentile(sfr_ratio, 84)

# ============================================================
# TIME SINCE PEAK
# ============================================================

time_since_peak = age - tau

tsp50 = np.percentile(time_since_peak, 50)
tsp16 = np.percentile(time_since_peak, 16)
tsp84 = np.percentile(time_since_peak, 84)

# ============================================================
# OUTPUT
# ============================================================

print("===== QUENCHING CLASSIFICATION =====")
print(f"Galaxy: {GALAXY_ID}")
print(f"Posterior samples: {len(samples)}")

print("\n===== SFR RATIO =====")
print(
    f"SFR_now / SFR_peak = "
    f"{ratio50:.4f} "
    f"[{ratio16:.4f}, {ratio84:.4f}]"
)

print("\n===== TIME SINCE SFH PEAK =====")
print(
    f"Age - tau = "
    f"{tsp50:.3f} "
    f"[{tsp16:.3f}, {tsp84:.3f}] Gyr"
)

print("\n===== SIMPLE DIAGNOSTIC =====")

if ratio84 < 0.1:
    print("Strongly declining / quenching candidate")
elif ratio50 < 0.3:
    print("Declining star formation")
else:
    print("Not strongly suppressed relative to peak")
