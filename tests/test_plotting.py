from src.fitting import read_posterior
from src.plotting import plot_sfh

POSTERIOR_FILE = "pipes/posterior/backend_test/1237648720142401611.h5"
OUTPUT_FILE = "figures/backend_sfh.png"

posterior = read_posterior(POSTERIOR_FILE)

age = posterior["delayed:age"]["median"]
tau = posterior["delayed:tau"]["median"]
massformed = posterior["delayed:massformed"]["median"]

plot_sfh(age, tau, massformed, OUTPUT_FILE)

print("SFH plot saved:", OUTPUT_FILE)
