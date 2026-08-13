from src.fitting import run_sed_fit


GALAXY_ID = 1237648720142401611


print("===== BACKEND TEST =====")
print("Galaxy:", GALAXY_ID)
print("Starting BAGPIPES fit...")


fit = run_sed_fit(
    galaxy_id=GALAXY_ID,
    run_name="backend_test",
    n_posterior=500,
)


print("\n===== BACKEND FIT COMPLETE =====")
print("Fit object:", type(fit))
print("Backend successfully completed.")
