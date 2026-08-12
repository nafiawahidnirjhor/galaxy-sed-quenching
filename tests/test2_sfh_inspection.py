import numpy as np
import bagpipes as pipes

# --------------------------------------------------
# Minimal BAGPIPES model
# --------------------------------------------------

model_components = {
    "redshift": 0.05,

    "delayed": {
        "age": 5.0,
        "tau": 2.0,
        "massformed": 10.0,
        "metallicity": 1.0
    }
}

# --------------------------------------------------
# Generate model
# --------------------------------------------------

model = pipes.model_galaxy(model_components)

sfh = model.sfh

print("\n===== MODEL CHECK =====")

print("Redshift:", model_components["redshift"])

print("Age of Universe [Gyr]:",
      sfh.age_of_universe / 1e9)

print("Number of age grid points:",
      len(sfh.ages))

print("\n===== AGE GRID =====")

print("Minimum age [Gyr]:",
      np.min(sfh.ages) / 1e9)

print("Maximum age [Gyr]:",
      np.max(sfh.ages) / 1e9)

print("\n===== SFH =====")

print("Minimum SFR:",
      np.min(sfh.sfh))

print("Maximum SFR:",
      np.max(sfh.sfh))

print("\n===== DERIVED QUANTITIES =====")

print("Formed stellar mass log10(Msun):",
      sfh.formed_mass)

print("Current stellar mass log10(Msun):",
      sfh.stellar_mass)

print("Current SFR [Msun/yr]:",
      sfh.sfr)

print("sSFR:",
      sfh.ssfr)

print("Mass-weighted age [Gyr]:",
      sfh.mass_weighted_age)

print("Formation time [Gyr]:",
      sfh.tform)

print("Quenching time:",
      sfh.tquench)

print("\n===== FIRST 10 SFH VALUES =====")

for age, sfr in zip(sfh.ages[:10], sfh.sfh[:10]):
    print(
        f"Age = {age/1e9:.6f} Gyr   "
        f"SFR = {sfr:.6e}"
    )

print("\n===== LAST 10 SFH VALUES =====")

for age, sfr in zip(sfh.ages[-10:], sfh.sfh[-10:]):
    print(
        f"Age = {age/1e9:.6f} Gyr   "
        f"SFR = {sfr:.6e}"
    )

print("\nMODEL GENERATION TEST PASSED.")
