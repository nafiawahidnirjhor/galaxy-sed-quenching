# Galaxy SED Quenching Tool

A Python and Streamlit application for fitting galaxy Spectral Energy Distributions (SEDs) with BAGPIPES and interpreting delayed-τ star-formation histories.

The tool accepts SDSS broadband photometry, performs SED fitting, derives star-formation diagnostics, reconstructs the fitted SFH, and provides an interpretable classification of the galaxy's current star-formation state.

![Application interface](figures/app_interface.png)

## Scientific Goal

This project focuses on understanding the star-formation state of galaxies through broadband SED fitting.

The analysis specifically investigates:

* Star-formation history (SFH)
* Stellar population age
* Stellar mass
* Star-formation rate (SFR)
* Specific star-formation rate (sSFR)
* Delayed-τ timescale
* Peak SFR
* Current-to-peak SFR ratio
* Time since the SFH peak

The resulting classification is an SED-based diagnostic and does not by itself prove that star formation has completely stopped.

## Analysis Workflow

```text
SDSS Photometric Catalogue
          ↓
Catalogue Validation
          ↓
Magnitude → Flux Conversion
          ↓
BAGPIPES SED Fitting
          ↓
Posterior Parameter Extraction
          ↓
Delayed-τ SFH Reconstruction
          ↓
SFR and Quenching Diagnostics
          ↓
Galaxy Classification
          ↓
Streamlit Results Interface
```

## Model

The project uses a delayed-τ star-formation history:

```text
SFR(t) ∝ t exp(-t/τ)
```

The fitted model includes:

* Stellar population age
* Delayed-τ timescale
* Formed stellar mass
* Stellar metallicity
* Calzetti dust attenuation
* Nebular emission
* Galaxy redshift

BAGPIPES performs the SED fitting and produces posterior distributions for the fitted parameters.

## Input Data

The application accepts an SDSS photometric catalogue in **CSV format**.

The catalogue must contain these columns:

```text
objID
z
modelMag_u
modelMag_g
modelMag_r
modelMag_i
modelMag_z
modelMagErr_u
modelMagErr_g
modelMagErr_r
modelMagErr_i
modelMagErr_z
```

The current pipeline therefore requires:

* SDSS `u`, `g`, `r`, `i`, `z` photometry
* Model magnitudes
* Magnitude uncertainties
* Galaxy redshift
* Unique integer `objID`

The application validates the required columns and photometric values before fitting.

## Results

For each selected galaxy, the application reports the main fitted and derived quantities.

### Stellar Population

* Stellar mass
* Stellar population age
* Stellar metallicity
* Dust attenuation

### Star Formation

* Current SFR
* Specific SFR
* Peak SFR
* Current / peak SFR
* Time since SFH peak
* Delayed-τ timescale

The specific SFR is calculated as:

```text
sSFR = SFR / stellar mass
```

The current-to-peak SFR ratio is:

```text
current / peak SFR = current SFR / peak SFR
```

This ratio is used as a simple indicator of how strongly the current star-formation activity has declined relative to the fitted peak.

## Star-Formation Classification

The application currently uses the following diagnostic thresholds:

| Current / Peak SFR | Classification         |
| -----------------: | ---------------------- |
|             ≥ 0.50 | Actively star-forming  |
|          0.10–0.50 | Moderately declining   |
|          0.01–0.10 | Strongly declining     |
|             < 0.01 | Strongly quenched-like |

These thresholds are project-defined diagnostic categories, not universal physical definitions of galaxy quenching.

## Technical Implementation

The main Python modules are separated by function:

```text
src/
├── fitting.py
├── sfh.py
├── diagnostics.py
├── interpretation.py
├── pipeline.py
└── plotting.py
```

### `fitting.py`

Handles:

* SDSS catalogue loading
* Input validation
* Magnitude-to-flux conversion
* BAGPIPES galaxy construction
* SED fitting
* Posterior extraction
* Posterior file reading

### `sfh.py`

Contains the delayed-τ SFH calculation used to reconstruct the star-formation history.

### `diagnostics.py`

Derives:

* Stellar mass
* Current SFR
* sSFR
* Peak SFR
* Current-to-peak SFR
* Time since SFH peak

### `interpretation.py`

Converts the numerical diagnostics into an accessible description of the galaxy's star-formation state.

### `pipeline.py`

Connects posterior extraction, diagnostics, and SFH visualization into a single analysis workflow.

### `plotting.py`

Generates SFH visualizations from the fitted parameters.

### `app.py`

Provides the Streamlit web interface for uploading catalogues, selecting galaxies, running fits, and displaying results.

## Repository Structure

```text
galaxy-sed-quenching/
│
├── app.py
├── README.md
├── requirements.txt
├── environment.yml
├── CITATION.cff
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── fitting.py
│   ├── sfh.py
│   ├── diagnostics.py
│   ├── interpretation.py
│   ├── pipeline.py
│   └── plotting.py
│
├── tests/
│   ├── test1_single_model.py
│   ├── test2_sfh_inspection.py
│   ├── test3_sdss_bagpipes_input.py
│   ├── test4_first_fit.py
│   ├── test5_extract_posterior.py
│   ├── test6_derive_sfh.py
│   ├── test7_quenching_classification.py
│   ├── test8_plot_sfh.py
│   ├── test9_mock_generation.py
│   ├── test10_fit_mock.py
│   ├── test_backend_fit.py
│   ├── test_diagnostics.py
│   ├── test_pipeline.py
│   ├── test_plotting.py
│   └── test_posterior_backend.py
│
├── figures/
└── logs/
```

## Installation

The project was developed using Python 3.10 and a dedicated Conda environment.

Create the environment with:

```bash
conda env create -f environment.yml
conda activate bagpipes_env
```

Or install the required Python packages with:

```bash
pip install -r requirements.txt
```

## Main Dependencies

```text
Python 3.10
BAGPIPES 1.3.5
Streamlit 1.61.1
NumPy 2.2.0
Pandas 2.3.3
Matplotlib 3.10.8
Astropy 6.1.7
SciPy 1.15.3
h5py 3.16.0
Nautilus Sampler 1.0.6
Spectres 2.2.2
Corner 2.2.3
```

## Running the Application

From the project root:

```bash
streamlit run app.py
```

Then:

1. Upload a compatible SDSS CSV catalogue.
2. Select a galaxy from the detected `objID` values.
3. Click **Run SED Fit**.
4. Wait for BAGPIPES to complete the posterior fitting.
5. Inspect the fitted parameters, diagnostics, SFH plot, and interpretation.

## Screenshots

### Galaxy Selection

![Galaxy selection](figures/app_select.png)

### SED Fitting

![SED fitting](figures/app_fitting.png)

### Galaxy Results

![Galaxy results](figures/app_result.png)

### Detailed Results

![Detailed results](figures/app_result2.png)

### Summary

![Analysis summary](figures/app_summary.png)

### Star-Formation History

![SFH plot](figures/app_plot.png)

### Additional SFH Plot

![Additional SFH plot](figures/app_plot2.png)

### Results View

![Results view](figures/app_r3.png)

## Validation and Testing

The project includes tests and controlled experiments covering:

* SDSS photometric input validation
* BAGPIPES galaxy construction
* Posterior extraction
* Delayed-τ SFH reconstruction
* SFR calculations
* Quenching classification
* SFH plotting
* Backend fitting
* Mock delayed-τ photometry
* Mock parameter recovery
* End-to-end pipeline behaviour

Controlled mock-data tests were also used to verify whether the fitting pipeline could recover known delayed-τ parameters.

## Limitations

The current implementation has several important limitations.

It uses five-band SDSS broadband photometry and a single delayed-τ SFH parameterization. Real galaxy SFHs can be more complex than this model.

The quenching classification depends on the assumed SFH model and project-defined thresholds.

The derived SFR and stellar population properties are therefore model-dependent estimates rather than direct measurements.

More robust physical conclusions would benefit from additional photometric bands, spectroscopy, alternative SFH models, independent SFR indicators, and a larger statistically selected galaxy sample.

## Project Status

**Functional research prototype**

The repository currently contains:

* A working Streamlit application
* SDSS catalogue validation
* BAGPIPES SED fitting
* Delayed-τ SFH modelling
* Posterior analysis
* SFR and quenching diagnostics
* SFH visualization
* Mock-data validation
* Automated tests
* Reproducible environment specifications

The project is intended as a research and educational prototype for exploring galaxy star-formation histories through SED fitting.

## Citation

If you use this project or its code in research, please refer to the citation information provided in `CITATION.cff`.

## License

See the repository license information for usage and redistribution terms.
