import bagpipes
import numpy as np

model_components = {
    "redshift": 0.05,

    "delayed": {
        "age": 5.0,
        "tau": 2.0,
        "massformed": 10.0,
        "metallicity": 1.0,
    },

    "dust": {
        "type": "Calzetti",
        "Av": 0.5,
    },

    "nebular": {
        "logU": -3.0,
    },
}

model = bagpipes.model_galaxy(model_components)

sfh = model.sfh

print("\n===== BAGPIPES TIME GRID =====")

print("Age of Universe:")
print(sfh.age_of_universe)

print("\nAge grid:")
print("minimum =", sfh.ages.min())
print("maximum =", sfh.ages.max())
print("number of points =", len(sfh.ages))

print("\nFirst 10 ages:")
print(sfh.ages[:10])

print("\nLast 10 ages:")
print(sfh.ages[-10:])

print("\nAge widths:")
print("minimum =", sfh.age_widths.min())
print("maximum =", sfh.age_widths.max())

print("\nFirst 10 age widths:")
print(sfh.age_widths[:10])

print("\nDerived quantities:")
print("stellar_mass =", sfh.stellar_mass)
print("formed_mass =", sfh.formed_mass)
print("SFR =", sfh.sfr)
print("sSFR =", sfh.ssfr)
print("mass_weighted_age =", sfh.mass_weighted_age)
print("tform =", sfh.tform)
print("tquench =", sfh.tquench)
