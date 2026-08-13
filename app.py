import streamlit as st
import pandas as pd

from src.fitting import run_sed_fit
from src.pipeline import analyze_posterior
from src.interpretation import interpret_with_uncertainty


st.set_page_config(
    page_title="Galaxy SED Quenching",
    layout="wide"
)

st.title("Galaxy SED Quenching Tool")

uploaded_file = st.file_uploader(
    "Upload SDSS Photometric Catalogue",
    type=["csv"]
)


if uploaded_file is not None:

    uploaded_file.seek(0)

    first_line = uploaded_file.readline().decode(
        "utf-8",
        errors="ignore"
    )

    uploaded_file.seek(0)

    if first_line.startswith("#Table1") or "objID" not in first_line:
        df = pd.read_csv(
            uploaded_file,
            skiprows=1
        )
    else:
        df = pd.read_csv(uploaded_file)

    required_columns = [
        "objID",
        "z",
        "modelMag_u",
        "modelMag_g",
        "modelMag_r",
        "modelMag_i",
        "modelMag_z",
        "modelMagErr_u",
        "modelMagErr_g",
        "modelMagErr_r",
        "modelMagErr_i",
        "modelMagErr_z",
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        st.error(
            "This CSV is not compatible with the current SDSS pipeline."
        )

        st.write(
            "Missing columns:",
            missing
        )

        st.stop()

    df["objID"] = df["objID"].astype("int64")

    st.write(
        f"Galaxies detected: {len(df)}"
    )

    galaxy_id = st.selectbox(
        "Select Galaxy",
        df["objID"].tolist()
    )

    if st.button(
        "Run SED Fit",
        type="primary"
    ):

        with st.spinner(
            "Running BAGPIPES SED fitting..."
        ):

            try:

                run_sed_fit(
                    galaxy_id=galaxy_id,
                    data_file=uploaded_file.getvalue(),
                    run_name="web_fit",
                    n_posterior=300,
                )

                posterior_file = (
                    "pipes/posterior/web_fit/"
                    f"{galaxy_id}.h5"
                )

                result = analyze_posterior(
                    posterior_file
                )

                diagnostics = result["diagnostics"]
                posterior = result["posterior"]

                st.success(
                    "SED fitting completed."
                )

                # -------------------------------------------------
                # Galaxy overview
                # -------------------------------------------------

                st.header("Galaxy Results")

                st.caption(
                    f"Galaxy ID: {galaxy_id}"
                )

                # Determine qualitative state
                ratio = diagnostics[
                    "current_to_peak_sfr"
                ]

                if ratio >= 0.5:
                    state = "Actively star-forming"
                elif ratio >= 0.1:
                    state = "Moderately declining"
                elif ratio >= 0.01:
                    state = "Strongly declining"
                else:
                    state = "Strongly quenched-like"

                st.subheader(
                    f"Star-formation state: {state}"
                )

                # -------------------------------------------------
                # Main diagnostics
                # -------------------------------------------------

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Stellar Mass",
                    f"{diagnostics['stellar_mass']:.2e} M☉"
                )

                col2.metric(
                    "Current SFR",
                    f"{diagnostics['sfr']:.3f} M☉/yr"
                )

                col3.metric(
                    "sSFR",
                    f"{diagnostics['ssfr']:.2e} yr⁻¹"
                )

                col4.metric(
                    "Current / Peak SFR",
                    f"{ratio:.4f}"
                )

                # -------------------------------------------------
                # Quenching information
                # -------------------------------------------------

                st.subheader(
                    "Star-formation history"
                )

                qcol1, qcol2 = st.columns(2)

                qcol1.metric(
                    "Peak SFR",
                    f"{diagnostics['peak_sfr']:.3f} M☉/yr"
                )

                qcol2.metric(
                    "Time since SFH peak",
                    f"{diagnostics['time_since_peak']:.2f} Gyr"
                )

                # -------------------------------------------------
                # Posterior parameters
                # -------------------------------------------------

                st.subheader(
                    "Fitted stellar population parameters"
                )

                age = posterior["delayed:age"]
                tau = posterior["delayed:tau"]
                mass = posterior["delayed:massformed"]

                parameter_table = pd.DataFrame({
                    "Parameter": [
                        "Stellar population age",
                        "Delayed-τ timescale",
                        "Formed stellar mass",
                    ],
                    "Median": [
                        f"{age['median']:.2f} Gyr",
                        f"{tau['median']:.2f} Gyr",
                        f"10^{mass['median']:.2f} M☉",
                    ],
                    "16th percentile": [
                        f"{age['lower']:.2f} Gyr",
                        f"{tau['lower']:.2f} Gyr",
                        f"10^{mass['lower']:.2f} M☉",
                    ],
                    "84th percentile": [
                        f"{age['upper']:.2f} Gyr",
                        f"{tau['upper']:.2f} Gyr",
                        f"10^{mass['upper']:.2f} M☉",
                    ],
                })

                st.dataframe(
                    parameter_table,
                    hide_index=True,
                    use_container_width=True
                )

                # -------------------------------------------------
                # SFH plot
                # -------------------------------------------------

                st.subheader(
                    "Star Formation History"
                )

                if "sfh_plot" in result:
                    st.image(
                        result["sfh_plot"],
                        use_container_width=True
                    )
                else:
                    st.info(
                        "SFH plot is not available."
                    )

                # -------------------------------------------------
                # Simple explanation
                # -------------------------------------------------

                st.subheader(
                    "In simple words"
                )

                interpretation = interpret_with_uncertainty(
                    result,
                    galaxy_id
                )

                st.write(
                    interpretation
                )


            except Exception as e:

                error_message = str(e)

                if "too high redshift" in error_message.lower():

                    st.error(
                        "This galaxy has a redshift that is outside "
                        "the range currently supported by the SED model. "
                        "Please select another galaxy or use a catalogue "
                        "with valid SDSS redshift measurements."
                    )

                elif "missing required SDSS columns" in error_message:

                    st.error(
                        "This CSV does not contain the required SDSS "
                        "photometric columns."
                    )

                elif "invalid redshift" in error_message.lower():

                    st.error(
                        "This galaxy has an invalid redshift value."
                    )

                elif "photometric values" in error_message.lower():

                    st.error(
                        "This galaxy contains invalid or missing "
                        "photometric measurements."
                    )

                else:

                    st.error(
                        f"Analysis failed: {error_message}"
                    )
