import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# CONFIGURATION
# ============================================================

GALAXY_ID = 1237648720142401611

POSTERIOR_FILE = (
    f"pipes/posterior/test4_first_fit/"
    f"{GALAXY_ID}.h5"
)

OUTPUT_FILE = (
    f"figures/{GALAXY_ID}_sfh_posterior.png"
)

# ============================================================
# LOAD BAGPIPES POSTERIOR
# ============================================================

with h5py.File(POSTERIOR_FILE, "r") as f:
    samples = f["samples2d"][:]

# BAGPIPES parameter order from test5
age = samples[:, 0]          # Gyr
massformed = samples[:, 1]   # log10(Msun)
metallicity = samples[:, 2]
tau = samples[:, 3]          # Gyr
Av = samples[:, 4]
logU = samples[:, 5]

print("===== SFH PLOT =====")
print(f"Galaxy: {GALAXY_ID}")
print(f"Posterior samples: {len(samples)}")

# ============================================================
# DELAYED SFH
# ============================================================
#
# SFR(t) = A * t * exp(-t/tau)
#
# For each posterior sample, normalize the SFH so that
# the integral from t=0 to t=age corresponds to the
# stellar mass formed.
#
# Massformed = log10(total formed stellar mass / Msun)
#
# ============================================================

# Common time grid
t_max = np.percentile(age, 99.5)

time = np.linspace(0.001, t_max, 500)

sfh_samples = np.zeros((len(samples), len(time)))

for i in range(len(samples)):

    current_age = age[i]
    current_tau = tau[i]
    current_mass = 10 ** massformed[i]

    # Only evaluate SFH inside the galaxy's formation interval
    valid = time <= current_age

    raw_sfh = np.zeros(len(time))

    raw_sfh[valid] = (
        time[valid]
        * np.exp(-time[valid] / current_tau)
    )

    # Normalize so integral = formed stellar mass
    integral = np.trapezoid(raw_sfh, time)

    if integral > 0:
        sfh_samples[i] = raw_sfh * current_mass / integral

# ============================================================
# CONVERT TO Msun / yr
# ============================================================

sfh_samples /= 1e9

# ============================================================
# POSTERIOR STATISTICS
# ============================================================

sfh_16 = np.percentile(sfh_samples, 16, axis=0)
sfh_50 = np.percentile(sfh_samples, 50, axis=0)
sfh_84 = np.percentile(sfh_samples, 84, axis=0)

# ============================================================
# MEDIAN AGE AND TAU
# ============================================================

age50 = np.percentile(age, 50)
tau50 = np.percentile(tau, 50)

age16 = np.percentile(age, 16)
age84 = np.percentile(age, 84)

tau16 = np.percentile(tau, 16)
tau84 = np.percentile(tau, 84)

# Delayed SFH peaks at t = tau
peak_time = tau50

# ============================================================
# CURRENT SFR
# ============================================================

# Find median SFH near the median age
current_index = np.argmin(np.abs(time - age50))
sfr_now = sfh_50[current_index]

# Peak SFR
peak_index = np.argmax(sfh_50)
sfr_peak = sfh_50[peak_index]

# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs("figures", exist_ok=True)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(8, 5.5))

plt.fill_between(
    time,
    sfh_16,
    sfh_84,
    alpha=0.25,
    label="16th–84th percentile"
)

plt.plot(
    time,
    sfh_50,
    linewidth=2,
    label="Posterior median"
)

# SFH peak
plt.axvline(
    peak_time,
    linestyle="--",
    linewidth=1.5,
    label=f"SFH peak = {peak_time:.2f} Gyr"
)

# Galaxy age
plt.axvline(
    age50,
    linestyle=":",
    linewidth=1.5,
    label=f"Galaxy age = {age50:.2f} Gyr"
)

# Current SFR marker
plt.scatter(
    [age50],
    [sfr_now],
    s=50,
    zorder=5,
    label=f"Current SFR = {sfr_now:.2f} M$_\\odot$ yr$^{{-1}}$"
)

# ============================================================
# AXES
# ============================================================

plt.xlabel("Time since onset of star formation [Gyr]")
plt.ylabel(r"SFR [$M_\odot$ yr$^{-1}$]")

plt.title(
    f"Posterior SFH: SDSS galaxy {GALAXY_ID}"
)

plt.yscale("log")

plt.xlim(0, max(age84 * 1.05, peak_time * 1.2))

plt.legend(
    fontsize=9,
    frameon=False
)

plt.tight_layout()

# ============================================================
# SAVE
# ============================================================

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ============================================================
# SUMMARY
# ============================================================

print("\n===== SFH SUMMARY =====")

print(
    f"Age = {age50:.3f} "
    f"[{age16:.3f}, {age84:.3f}] Gyr"
)

print(
    f"Tau = {tau50:.3f} "
    f"[{tau16:.3f}, {tau84:.3f}] Gyr"
)

print(
    f"SFH peak time = {peak_time:.3f} Gyr"
)

print(
    f"Current SFR ≈ {sfr_now:.4f} Msun/yr"
)

print(
    f"Peak SFR ≈ {sfr_peak:.4f} Msun/yr"
)

print(
    f"SFR_now / SFR_peak = "
    f"{sfr_now / sfr_peak:.4f}"
)

print("\n===== OUTPUT =====")
print(OUTPUT_FILE)

