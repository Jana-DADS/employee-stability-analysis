# Stability of Employees 55+

**Jana Dolečková** · Data Analyst
- Research direction
- Data source selection
- Review and interpretation

**Claude** (Anthropic AI assistant)
- Data collection
- Code
- Chart generation
- Presentation design and build

## About the project

This analysis highlights the stability of employees aged 55+, based on real, publicly published data: how long they stay with their employer compared to younger age groups.

➡️ **[Open the notebook with the full analysis](notebooks/fluktuace_50plus_analyza.ipynb)**
➡️ **[Open the presentation](presentation/stability_55plus.pptx)**

## Key findings

1. Median tenure with an employer rises almost monotonically with age: 2.7 years (25–34) → 9.6–9.8 years (55+).
2. The trend is stable across 2014–2024, not a one-off blip.
3. It also holds for college-educated workers — education doesn't affect turnover nearly as much as age.
4. Only 10% of workers aged 55–64 are in a job less than a year old (vs. 48% for 20–24 year-olds); conversely 51% of them have been with their employer 10+ years.
5. In the Czech Republic (2025), 80.3% of employed 50–64 year-olds have been with their employer 5+ years, vs. 62.1% for a derived 25–49 group — a similar pattern to the U.S. (15–24 was excluded as mostly student/part-time jobs; 25–49 was computed from Eurostat's published headcounts, since no ready-made non-overlapping age band exists for this comparison.)

## Data sources analyzed here

| Source | Used for |
|---|---|
| [U.S. Bureau of Labor Statistics (BLS) — Employee Tenure Summary, January 2024](https://www.bls.gov/news.release/tenure.t01.htm) | Median years with employer by age, sex, and education |
| [BLS — The Economics Daily, October 2024](https://www.bls.gov/opub/ted/2024/median-tenure-with-current-employer-was-3-9-years-in-january-2024.htm) | Distribution of tenure length by age |
| [Eurostat — lfsa_egad, Employed persons by job tenure](https://ec.europa.eu/eurostat/databrowser/view/lfsa_egad/default/table) | Czech Republic tenure data by age and sex, 2025 |

## Note on methodology and data choice

The analysis was originally meant to be built on a Kaggle dataset simulating company HR data. After checking correlations (age vs. attrition: r = 0.008; age vs. salary: r = -0.003 on the `ziya07/employee-attrition-prediction-dataset`), it turned out to be purely randomly generated synthetic data with no built-in relationship between variables — no honest conclusion about age and turnover could be drawn from it. The analysis was reworked around real, officially published data from BLS and Eurostat instead. Unused datasets (including the IBM HR Attrition dataset) are kept in `data/nepouzito/` for reference only.

**Limitations:** BLS and Eurostat data are cross-sectional (one year), not an individual's timeline — you can't claim "today's 55-year-olds churned less when they were 25," only that "today's 55-year-olds churn less than today's 25-year-olds." The Eurostat table doesn't break down by education; the BLS age × education table is U.S.-only. Gaps between men and women are visible in the data (see notebook section 5c/7), but their causes aren't contained in the data and are left uninterpreted.

## Project structure

```
project_A_fluktuace/
├── data/
│   ├── bls/                      # processed data from BLS tables (CSV)
│   ├── eurostat_cz/              # processed Eurostat data for Czechia (CSV)
│   └── nepouzito/                # unused datasets (Kaggle, CZSO aggregates)
├── notebooks/
│   └── fluktuace_50plus_analyza.ipynb
├── presentation/
│   └── stability_55plus.pptx      # summary slide deck built from the notebook's charts
├── src/
│   └── analysis.py               # script generating all charts (Czech-labelled version)
├── visuals/                      # generated charts (PNG, English labels)
└── README.md
```

## How to run

This project uses a virtual environment (`venv/`) so the notebook always runs against the same, known set of package versions.

**First-time setup** (from the `project_A_fluktuace/` folder):

Windows:
```bash
setup_env.bat
```

macOS/Linux:
```bash
./setup_env.sh
```

This creates `venv/`, installs everything from `requirements.txt` into it, and registers a Jupyter kernel called **"Python (fluktuace)"**.

**Working with the notebook:** open `notebooks/fluktuace_50plus_analyza.ipynb` in Jupyter or VS Code and select the **"Python (fluktuace)"** kernel. To run it end-to-end from the command line instead:

```bash
venv\Scripts\activate          # Windows — use "source venv/bin/activate" on macOS/Linux
cd notebooks
jupyter execute fluktuace_50plus_analyza.ipynb --output=fluktuace_50plus_analyza.ipynb
```

`venv/` is git-ignored — each machine creates its own by running the setup script once.
