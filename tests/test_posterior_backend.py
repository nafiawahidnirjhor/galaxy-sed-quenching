from src.fitting import read_posterior

POSTERIOR_FILE = (
    "pipes/posterior/backend_test/"
    "1237648720142401611.h5"
)

result = read_posterior(POSTERIOR_FILE)

print("===== BACKEND POSTERIOR TEST =====")

for name, values in result.items():
    if name == "_samples":
        print("\nPosterior samples shape:", values.shape)
        continue

    print(
        f"{name:25s}"
        f"{values['median']:.4f}"
        f" [{values['lower']:.4f}, {values['upper']:.4f}]"
    )
