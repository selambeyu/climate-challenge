# Climate Challenge — Week 0

Exploratory data analysis of NASA POWER climate data for five African countries (Ethiopia, Kenya, Sudan, Tanzania, Nigeria) covering daily weather observations from January 2015 to March 2026.

## Project Structure

```
climate-challenge-week0/
├── data/
│   ├── Data Legend.txt      # Column definitions and data source documentation
│   ├── ethiopia.csv         # Raw daily climate data — Addis Ababa
│   ├── ethiopia_clean.csv   # Cleaned version after profiling
│   ├── kenya.csv            # Raw daily climate data — Nairobi
│   ├── nigeria.csv          # Raw daily climate data — Lagos
│   ├── sudan.csv            # Raw daily climate data — Khartoum
│   └── tanzania.csv         # Raw daily climate data — Dar es Salaam
├── notebooks/
│   ├── ethiopia_eda.ipynb   # EDA notebook for Ethiopia
│   └── kenya_eda.ipynb      # EDA notebook for Kenya
├── .github/
│   └── workflows/ci.yml     # GitHub Actions CI pipeline
└── requirements.txt
```

## Data Source

**NASA POWER** (Prediction of Worldwide Energy Resources) via the MERRA-2 reanalysis model.

- **Spatial resolution:** 0.5° × 0.625° grid; each country represented by its capital city coordinates
- **Temporal resolution:** Daily
- **Period:** 2015-01-01 — 2026-03-31 (~4,100 rows per country)

| Country  | Latitude  | Longitude | Location      |
|----------|-----------|-----------|---------------|
| Ethiopia | 9.0300°N  | 38.7400°E | Addis Ababa   |
| Kenya    | 1.2921°S  | 36.8219°E | Nairobi       |
| Sudan    | 15.5007°N | 32.5599°E | Khartoum      |
| Tanzania | 6.7924°S  | 39.2083°E | Dar es Salaam |
| Nigeria  | 6.5244°N  | 3.3792°E  | Lagos         |

### Key Variables

| Column         | Unit    | Description                          |
|----------------|---------|--------------------------------------|
| `T2M`          | °C      | Mean daily temperature at 2 m        |
| `T2M_MAX`      | °C      | Daily maximum temperature at 2 m     |
| `T2M_MIN`      | °C      | Daily minimum temperature at 2 m     |
| `T2M_RANGE`    | °C      | Diurnal temperature range            |
| `PRECTOTCORR`  | mm/day  | Bias-corrected precipitation         |
| `RH2M`         | %       | Relative humidity at 2 m             |
| `WS2M`         | m/s     | Mean wind speed at 2 m               |
| `WS2M_MAX`     | m/s     | Maximum wind speed at 2 m            |
| `PS`           | kPa     | Surface atmospheric pressure         |
| `QV2M`         | g/kg    | Specific humidity at 2 m             |

Missing values are encoded as `-999` in the raw NASA files and should be replaced with `NaN` before analysis.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Branches

| Branch          | Focus                        |
|-----------------|------------------------------|
| `main`          | Stable, reviewed work        |
| `eda-ethiopia`  | Ethiopia EDA and cleaning    |

## CI

GitHub Actions runs on push to `main`: installs dependencies with Python 3.10.
