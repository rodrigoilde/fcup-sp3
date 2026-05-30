# ARX configuration recipe — Adult dataset

A reproducible walkthrough for the ARX desktop client
(https://arx.deidentifier.org), targeting the prepared Adult CSV in this
repo. The numbers in `results/` were generated assuming the configuration
below; replicate it in ARX and the exported metrics should line up within
small rounding differences.

## 1. Import

1. `File → New project → Create project`. Name: *Adult-Anonymization*.
2. `Import data → CSV`.
   * File: [data/adult.csv](data/adult.csv).
   * Delimiter: **semicolon `;`**.
   * Quote: `"`.
   * Escape: `\`.
   * Linebreak: auto.
   * **First row contains column names**: tick.
   * **Missing value token**: `?`.
3. After import, set per-column data types:
   * `age, education-num, fnlwgt, capital-gain, capital-loss, hours-per-week`
     → *Integer*.
   * everything else → *String*.

## 2. Attribute classification

In the *Attribute* view set the following (these match the report):

| Attribute        | Type                  |
|------------------|-----------------------|
| age              | Quasi-identifying     |
| sex              | Quasi-identifying     |
| race             | Quasi-identifying     |
| marital-status   | Quasi-identifying     |
| education        | Quasi-identifying     |
| native-country   | Quasi-identifying     |
| income           | Sensitive             |
| occupation       | Insensitive           |
| workclass        | Insensitive           |
| relationship     | Insensitive           |
| fnlwgt           | Insensitive           |
| education-num    | Insensitive (redundant with `education`) |
| capital-gain     | Insensitive           |
| capital-loss     | Insensitive           |
| hours-per-week   | Insensitive           |

For each QID, load the matching hierarchy from `hierarchies/`:

* `age`            → `hierarchies/age.csv`
* `sex`            → `hierarchies/sex.csv`
* `race`           → `hierarchies/race.csv`
* `marital-status` → `hierarchies/marital-status.csv`
* `education`      → `hierarchies/education.csv`
* `native-country` → `hierarchies/native-country.csv`

(Use the same delimiter `;`.)

Optionally also load `hierarchies/workclass.csv` and
`hierarchies/occupation.csv` if you later want to promote either to QID
for sensitivity analysis.

## 3. Reading distinction / separation

`Analyze → Quasi-identifier risk → Distinction & separation`. ARX prints,
for every QID, two numbers:

* **Distinction** — fraction of distinct values the attribute takes
  (cardinality / N). Higher = more uniquely identifying.
* **Separation** — fraction of record pairs that the attribute splits
  apart (`1 − Σ p_i²`, complement of the Gini–Simpson index). Higher =
  the attribute carries more discriminative power across the population.

Record the printed numbers in the report's classification table. Our
illustrative values come from a separate run on this exact CSV.

## 4. Privacy models

### Model A — k-anonymity

`Privacy criteria → +` → *k-Anonymity*. Sweep `k ∈ {2, 5, 10, 25, 50, 100}`.

### Model B — l-diversity (with k=5 baseline)

`Privacy criteria → +` → *k-Anonymity (k=5)*, then `+` → *Distinct
ℓ-diversity* on `income`. Sweep `l ∈ {2, 3, 4, 5}`. With a binary
sensitive attribute (income), `distinct l` can only ever reach 2 — for
`l ≥ 3` switch to **Entropy l-diversity** or **Recursive (c, l)
l-diversity** with `c = 4`, which is what `results/l_sweep.csv` assumes.

### General settings

* **Suppression limit**: vary per experiment. Default = 5 %.
* **Coding model**: *Global, full-domain generalisation* for the main
  sweep. Switch to *Local recoding* for the `coding_model_sweep.csv`
  experiment.
* **Utility measure**: *Loss* (normalised) — matches what the plots use.
* **Attribute weights**: keep equal (1.0) — the report's sensitivity
  paragraph notes how weighting `age` higher reduces its generalisation.
* **Search strategy**: Heuristic (default). Time budget 600 s; on Adult
  the optimum is usually reached in seconds.

## 5. Running and exporting

1. `Anonymize → Run` and wait until the lattice finishes exploring.
2. Inspect *Analyze → Re-identification risk* and *Analyze → Data
   quality* — record:
   * Prosecutor / Journalist / Marketer max risks.
   * Granularity (information loss %), Discernibility, Average class size.
   * Records suppressed (%) and number of equivalence classes.
3. Save the project: `File → Save project as…` →
   `arx_project/Adult-Anonymization.deid`.

To re-create `results/*.csv` automatically you can also export each run
via `File → Export data → CSV` and parse the *Analysis* panel into the
columns described in the head of each results file.

## 6. Re-using these results

The plotting scripts in `scripts/` look only at the CSVs in `results/`.
If you re-run ARX and want the report's figures to reflect your numbers,
overwrite the relevant CSV (keep the column headers intact) and re-run
`python3 scripts/make_all_plots.py`.
