def interpret_with_uncertainty(result, galaxy_id):

    d = result["diagnostics"]

    ratio = d["current_to_peak_sfr"]

    if ratio >= 0.5:
        conclusion = (
            f"Galaxy {galaxy_id} is still forming stars at a substantial "
            f"fraction of its fitted peak rate. Its current star-formation "
            f"activity is about {ratio * 100:.1f}% of the fitted peak, so "
            f"the results do not indicate strong quenching."
        )

    elif ratio >= 0.1:
        conclusion = (
            f"Galaxy {galaxy_id} has experienced a noticeable decline in "
            f"star formation. Its current activity is about {ratio * 100:.1f}% "
            f"of the fitted peak, indicating a moderately declining "
            f"star-formation history rather than strong quenching."
        )

    elif ratio >= 0.01:
        conclusion = (
            f"Galaxy {galaxy_id} shows strong suppression of recent star "
            f"formation. Its current activity is only about {ratio * 100:.1f}% "
            f"of the fitted peak, indicating a strongly declining or "
            f"quenched-like star-formation history."
        )

    else:
        conclusion = (
            f"Galaxy {galaxy_id} shows extremely strong suppression of "
            f"recent star formation. Its current activity is only about "
            f"{ratio * 100:.2f}% of the fitted peak, indicating a very "
            f"strongly quenched-like star-formation history."
        )

    peak_time = d["time_since_peak"]

    conclusion += (
        f" The fitted star-formation peak occurred approximately "
        f"{peak_time:.2f} Gyr ago."
    )

    conclusion += (
        " This interpretation comes from the fitted delayed-τ "
        "star-formation history and available broadband photometry. "
        "It does not by itself prove that star formation has completely "
        "stopped."
    )

    return conclusion
