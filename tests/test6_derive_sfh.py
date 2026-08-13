import h5py
import numpy as np

GALAXY_ID = "1237648720142401611"

POSTERIOR_FILE = (
    f"pipes/posterior/test4_first_fit/"
    f"{GALAXY_ID}.h5"
)

AGE = 0
MASSFORMED = 1
TAU = 3


def delayed_sfh(t, age, tau, massformed):
    mass = 10**massformed

    norm = tau**2 * (
        1.0 - np.exp(-age / tau) * (1.0 + age / tau)
    )

    sfr_gyr = mass * t * np.exp(-t / tau) / norm

    return sfr_gyr / 1e9


def summary(values):
    return np.percentile(values, [16, 50, 84])


# ============================================================
# LOAD POSTERIOR
# ============================================================

with h5py.File(POSTERIOR_FILE, "r") as f:
    samples = f["samples2d"][:]


age = samples[:, AGE]
massformed = samples[:, MASSFORMED]
tau = samples[:, TAU]


# ============================================================
# CURRENT SFR
# ============================================================

current_sfr = delayed_sfh(
    age,
    age,
    tau,
    massformed
)


# ============================================================
# PEAK SFR
# ============================================================

peak_time = tau

peak_sfr = delayed_sfh(
    peak_time,
    age,
    tau,
    massformed
)


# ============================================================
# SPECIFIC SFR
# ============================================================

stellar_mass = 10**massformed

ssfr = current_sfr / stellar_mass


# ============================================================
# QUENCHING RATIO
# ============================================================

quenching_ratio = current_sfr / peak_sfr

decline_factor = peak_sfr / current_sfr


# ============================================================
# SUMMARIES
# ============================================================

sfr16, sfr50, sfr84 = summary(current_sfr)

peak16, peak50, peak84 = summary(peak_sfr)

tau16, tau50, tau84 = summary(tau)

ssfr16, ssfr50, ssfr84 = summary(ssfr)

ratio16, ratio50, ratio84 = summary(quenching_ratio)

decline16, decline50, decline84 = summary(decline_factor)


# ============================================================
# OUTPUT
# ============================================================

print("===== DERIVED SFH =====")
print("Galaxy:", GALAXY_ID)
print("Posterior samples:", len(samples))

print("\n===== CURRENT SFR =====")
print(
    f"SFR = {sfr50:.4f} "
    f"[{sfr16:.4f}, {sfr84:.4f}] Msun/yr"
)

print("\n===== PEAK SFR =====")
print(
    f"SFR_peak = {peak50:.4f} "
    f"[{peak16:.4f}, {peak84:.4f}] Msun/yr"
)

print("\n===== SFH TIMESCALE =====")
print(
    f"Tau / peak time = {tau50:.4f} "
    f"[{tau16:.4f}, {tau84:.4f}] Gyr"
)

print("\n===== SPECIFIC SFR =====")
print(
    f"sSFR = {ssfr50:.3e} "
    f"[{ssfr16:.3e}, {ssfr84:.3e}] yr^-1"
)

print("\n===== QUENCHING DIAGNOSTICS =====")
print(
    f"SFR_now / SFR_peak = {ratio50:.4f} "
    f"[{ratio16:.4f}, {ratio84:.4f}]"
)

print(
    f"SFR_peak / SFR_now = {decline50:.2f} "
    f"[{decline16:.2f}, {decline84:.2f}]"
)
