import numpy as np
import matplotlib.pyplot as plt
import bagpipes as pipes


model_components = {
    "redshift": 0.05,

    "delayed": {
        "age": 5.0,
        "tau": 2.0,
        "massformed": 10.0,
        "metallicity": 1.0,
    },
}


model = pipes.model_galaxy(model_components)

print("BAGPIPES model generated successfully.")

print(f"Redshift: {model_components['redshift']}")
print(f"SFH age: {model_components['delayed']['age']} Gyr")
print(f"SFH tau: {model_components['delayed']['tau']} Gyr")
print(f"Formed stellar mass: 10^{model_components['delayed']['massformed']} Msun")
print(f"Metallicity: {model_components['delayed']['metallicity']} Zsun")

print()
print("Model attributes:")
print([x for x in dir(model) if not x.startswith("_")])

sfh = model.sfh.sfh
ages = model.sfh.ages / 1e9

print()
print(f"Number of SFH grid points: {len(ages)}")
print(f"SFH minimum: {sfh.min():.4e}")
print(f"SFH maximum: {sfh.max():.4e}")

plt.figure(figsize=(8, 5))

plt.plot(ages, sfh)

plt.xlabel("Stellar age / lookback time (Gyr)")
plt.ylabel("SFR (normalized)")
plt.title("BAGPIPES Delayed SFH Test")

plt.xscale("log")
plt.yscale("log")

plt.tight_layout()
plt.savefig("figures/test1_sfh.png", dpi=200)

print()
print("Saved: figures/test1_sfh.png")
