# Project Eventide

Applied Machine Learning (CSCI 5612) semester project by Samuel Meaux, CU Boulder MS in Data Science.

Project Eventide explores whether everyday Garmin wearable data can show patterns consistent with disrupted sleep and poor recovery in veterans and their families. The primary dataset comes from the Sleep Savant Program hosted by Elpis Alliance (98 participants, 18,728 nights after cleaning). A blood oxygen subset covers 47 participants and 8,729 nights. Data from a single individual was used for early exploration.

Live site: https://meauxcodes.github.io/applied-ml-project/

## Site pages

- `index.html` - Introduction
- `dataprep.html` - Data Prep / EDA
- `clustering.html` - Clustering
- `pca.html` - PCA
- `naivebayes.html` - Naive Bayes (low-recovery nights)
- `dectrees.html` - Decision Trees (low-oxygen nights)
- `regression.html`, `adaboost.html`, `gradientboosting.html`, `xgboost.html` - later modules (in progress)
- `conclusions.html` - Conclusions
- `about.html` - About
- `style.css` - shared styling

## Folders

- `data/raw` - de-identified joined cohort data and the single-participant Garmin data
- `data/clean` - cleaned datasets and the data dictionary, with one subfolder per method (`clustering`, `pca`, `naivebayes`, `decisiontree`) holding that method's labeled, training and testing files
- `scripts` - the data pipeline (stacking, respiration, pulse-ox, joining, de-identification, cleaning, labeling) and the personal Garmin pull and visualization code
- `scripts/notebooks` - analysis notebooks (EDA, labels, clustering, PCA, Naive Bayes, Decision Trees)
- `scripts/pulse_ox` - nightly blood oxygen values and pulse-ox notebooks
- `images` - figures used on the site, with one subfolder per page

## Data pipeline

`scripts/main.py` runs the cohort pipeline in order:

1. `cohort_stacking.py` - stacks the per-day LabFront CSVs into one table per data type
2. `cohort_respiration.py` - summarizes minute-by-minute sleep breathing into nightly values
3. `pulse_ox/pulse_ox_nightly_values.py` - summarizes blood oxygen into nightly values
4. `cohort_joining.py` - joins everything into one table per participant-night
5. `deidentify.py` - replaces real participant IDs with P1 to P98
6. `cohort_cleaning.py` - removes missing and impossible values
7. `labelling.py` - builds the low-recovery (Naive Bayes) and low-oxygen (Decision Trees) labels

## Privacy

The raw LabFront export and the joined table with real participant IDs are stored on an external drive and are never committed to this repository. Only de-identified data (P1 to P98) is kept here.

## Status

Modules 1 to 3 are complete (Introduction, Data Prep / EDA, Clustering, PCA, Naive Bayes, Decision Trees). The remaining method pages are placeholders until their modules. The graded Module 2 version of the site is preserved at the `module2-graded` tag.

## Hosting

The site is plain HTML/CSS and is served by GitHub Pages from the `main` branch (root folder). Pushing to `main` updates the live site within a couple of minutes.
