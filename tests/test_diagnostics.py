from src.fitting import read_posterior
from src.diagnostics import calculate_diagnostics

POSTERIOR_FILE = (
    "pipes/posterior/backend_test/"
    "1237648720142401611.h5"
)

posterior = read_posterior(POSTERIOR_FILE)

age = posterior["delayed:age"]["median"]
tau = posterior["delayed:tau"]["median"]
massformed = posterior["delayed:massformed"]["median"]

result = calculate_diagnostics(
    age,
    tau,
    massformed
)

print("===== DIAGNOSTICS =====")

for key, value in result.items():
    print(f"{key:25s}: {value}")
