import os
import h5py
import numpy as np
import pandas as pd
import bagpipes


DATA_FILE = "data/raw/sdss_specphoto_100.csv"

FILTER_LIST = [
    "data/filters/u.dat",
    "data/filters/g.dat",
    "data/filters/r.dat",
    "data/filters/i.dat",
    "data/filters/z.dat",
]

BANDS = ["u", "g", "r", "i", "z"]

REQUIRED_COLUMNS = [
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


def validate_catalog(df):
    """Validate an SDSS photometric catalogue before fitting."""

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "CSV is missing required SDSS columns: "
            + ", ".join(missing)
        )

    if len(df) == 0:
        raise ValueError(
            "The uploaded catalogue contains no galaxies."
        )

    try:
        df["objID"] = df["objID"].astype(np.int64)
    except Exception:
        raise ValueError(
            "The objID column contains invalid galaxy IDs."
        )

    if df["objID"].duplicated().any():
        duplicated = df.loc[
            df["objID"].duplicated(),
            "objID"
        ].tolist()

        raise ValueError(
            "The catalogue contains duplicate galaxy IDs. "
            f"Example: {duplicated[:3]}"
        )

    # Check redshift
    z = pd.to_numeric(
        df["z"],
        errors="coerce"
    )

    if z.isna().any():
        raise ValueError(
            "The catalogue contains missing or invalid redshift values."
        )

    if (~np.isfinite(z)).any():
        raise ValueError(
            "The catalogue contains non-finite redshift values."
        )

    if (z < 0).any():
        raise ValueError(
            "The catalogue contains negative redshift values."
        )

    # Check photometry
    for band in BANDS:

        mag_col = f"modelMag_{band}"
        err_col = f"modelMagErr_{band}"

        mag = pd.to_numeric(
            df[mag_col],
            errors="coerce"
        )

        err = pd.to_numeric(
            df[err_col],
            errors="coerce"
        )

        if mag.isna().any() or err.isna().any():
            raise ValueError(
                f"Band {band} contains missing or invalid "
                "photometric values."
            )

        if (~np.isfinite(mag)).any():
            raise ValueError(
                f"Band {band} contains non-finite magnitudes."
            )

        if (~np.isfinite(err)).any():
            raise ValueError(
                f"Band {band} contains non-finite magnitude errors."
            )

        if (mag <= 0).any():
            raise ValueError(
                f"Band {band} contains invalid magnitudes."
            )

        if (err <= 0).any():
            raise ValueError(
                f"Band {band} contains invalid magnitude errors."
            )

    return df


def load_sdss_catalog(data_file=DATA_FILE):

    df = pd.read_csv(
        data_file,
        skiprows=1
    )

    return validate_catalog(df)


def load_sdss_photometry(galaxy_id, df):

    galaxy_id = int(galaxy_id)

    matches = df[
        df["objID"] == galaxy_id
    ]

    if len(matches) == 0:
        raise ValueError(
            f"Galaxy ID {galaxy_id} not found in catalogue."
        )

    row = matches.iloc[0]

    fluxes = []
    errors = []

    for band in BANDS:

        mag = float(
            row[f"modelMag_{band}"]
        )

        mag_err = float(
            row[f"modelMagErr_{band}"]
        )

        flux = 10 ** (
            (23.9 - mag) / 2.5
        )

        flux_err = (
            flux
            * np.log(10)
            / 2.5
            * mag_err
        )

        if not np.isfinite(flux) or flux <= 0:
            raise ValueError(
                f"Invalid flux calculated for "
                f"galaxy {galaxy_id}, band {band}."
            )

        if not np.isfinite(flux_err) or flux_err <= 0:
            raise ValueError(
                f"Invalid flux uncertainty calculated for "
                f"galaxy {galaxy_id}, band {band}."
            )

        fluxes.append(flux)
        errors.append(flux_err)

    return np.column_stack([
        np.asarray(fluxes),
        np.asarray(errors),
    ])


def make_bagpipes_galaxy(galaxy_id, df):

    galaxy_id = int(galaxy_id)

    matches = df[
        df["objID"] == galaxy_id
    ]

    if len(matches) == 0:
        raise ValueError(
            f"Galaxy ID {galaxy_id} not found in catalogue."
        )

    row = matches.iloc[0]

    redshift = float(row["z"])

    if not np.isfinite(redshift) or redshift < 0:
        raise ValueError(
            f"Invalid redshift for galaxy {galaxy_id}: "
            f"{redshift}"
        )

    def load_data(ID):
        return load_sdss_photometry(
            ID,
            df
        )

    galaxy = bagpipes.galaxy(
        galaxy_id,
        load_data=load_data,
        spectrum_exists=False,
        photometry_exists=True,
        filt_list=FILTER_LIST,
        phot_units="mujy",
        out_units="ergscma",
    )

    return galaxy, redshift


def run_sed_fit(
    galaxy_id,
    data_file=DATA_FILE,
    run_name="sed_fit",
    n_posterior=500,
):

    if hasattr(data_file, "read"):

        data_file.seek(0)

        df = pd.read_csv(
            data_file,
            skiprows=1
        )

    elif isinstance(data_file, bytes):

        from io import BytesIO

        df = pd.read_csv(
            BytesIO(data_file),
            skiprows=1
        )

    else:

        df = load_sdss_catalog(
            data_file
        )

        # Already validated.
        galaxy, redshift = make_bagpipes_galaxy(
            galaxy_id,
            df
        )

        return _fit(
            galaxy,
            redshift,
            run_name,
            n_posterior
        )

    # Uploaded Streamlit files
    df = validate_catalog(df)

    galaxy, redshift = make_bagpipes_galaxy(
        galaxy_id,
        df
    )

    return _fit(
        galaxy,
        redshift,
        run_name,
        n_posterior
    )


def _fit(
    galaxy,
    redshift,
    run_name,
    n_posterior,
):

    fit_instructions = {

        "delayed": {
            "age": (0.1, 10.0),
            "tau": (0.1, 10.0),
            "metallicity": (0.0, 2.5),
            "massformed": (7.0, 12.0),
        },

        "dust": {
            "type": "Calzetti",
            "Av": (0.0, 3.0),
        },

        "nebular": {
            "logU": (-3.0, -1.0),
        },

        "redshift": redshift,
    }

    os.makedirs(
        run_name,
        exist_ok=True
    )

    fit = bagpipes.fit(
        galaxy,
        fit_instructions,
        run=run_name,
        n_posterior=n_posterior,
    )

    fit.fit(
        verbose=True
    )

    return fit


def extract_posterior(fit):

    names = [
        "delayed:age",
        "delayed:massformed",
        "delayed:metallicity",
        "delayed:tau",
        "dust:Av",
        "nebular:logU",
    ]

    result = {}

    for i, name in enumerate(names):

        result[name] = {
            "median": float(
                fit.posterior.median[i]
            ),
            "lower": float(
                fit.posterior.conf_int[0, i]
            ),
            "upper": float(
                fit.posterior.conf_int[1, i]
            ),
        }

    return result


def read_posterior(posterior_file):

    with h5py.File(
        posterior_file,
        "r"
    ) as f:

        median = f["median"][:]
        conf_int = f["conf_int"][:]
        samples = f["samples2d"][:]

    names = [
        "delayed:age",
        "delayed:massformed",
        "delayed:metallicity",
        "delayed:tau",
        "dust:Av",
        "nebular:logU",
    ]

    result = {}

    for i, name in enumerate(names):

        result[name] = {
            "median": float(
                median[i]
            ),
            "lower": float(
                conf_int[0, i]
            ),
            "upper": float(
                conf_int[1, i]
            ),
        }

    result["_samples"] = samples

    return result
