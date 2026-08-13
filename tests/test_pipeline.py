from src.pipeline import analyze_posterior

POSTERIOR_FILE = (
    "pipes/posterior/backend_test/"
    "1237648720142401611.h5"
)

result = analyze_posterior(POSTERIOR_FILE)

print("===== COMPLETE ANALYSIS =====")

print("\nPosterior:")
for key, value in result["posterior"].items():
    if key != "_samples":
        print(
            f"{key}: "
            f"{value['median']:.4f} "
            f"[{value['lower']:.4f}, {value['upper']:.4f}]"
        )

print("\nDiagnostics:")
for key, value in result["diagnostics"].items():
    print(f"{key}: {value}")
