# Climate and Atmospheric Conditions - Story

This repository contains an interactive Streamlit dashboard for exploring and visualizing climate and atmospheric conditions data.

---

## Overview

The application is built with Streamlit and follows a narrative-driven data visualization approach: Introduction → Analysis → Insights → Recommendations.

Key objectives:

- Time-series analysis of climate variables
- Variable relationship exploration (temperature, humidity, pressure, wind speed, etc.)
- Weather-type comparisons and anomaly detection
- Summary KPIs and data quality reporting

---

## Quick Start

Prerequisites:

- Python 3.8 or newer
- pip

Steps:

1. Clone the repository and enter the project directory:

```bash
git clone git@github.com:MM1ng/data_viz.git
cd data_viz_project
```

2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Place your CSV dataset into the `data/` folder. The app will load the first CSV file it finds. The original dataset is available on Kaggle:

https://www.kaggle.com/datasets/saadaliyaseen/climate-and-atmospheric-conditions-data/data

5. Run the app:

```bash
streamlit run app.py
```

Open the URL printed by Streamlit (typically `http://localhost:8501`).
2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Place your CSV data into the `data/` directory (or use sample data provided).

5. Run the app:

```bash
streamlit run app.py
```

Open the app at `http://localhost:8501` (or the local URL printed by Streamlit).

---

## Project Structure

```
data_viz_project/
├── app.py                 # Streamlit app
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── sections/              # page modules
├── utils/                 # helpers (load, prep, viz)
├── data/                  # folder for CSV files
└── assets/                # resources (logos etc.)
```

---

## Features

- Time series analysis
- Distributions & box plots
- Weather-type comparisons
- Correlation heatmap
- KPI metrics

---

## Dataset

- Name: Climate and Atmospheric Conditions Data
- Source: Kaggle — https://www.kaggle.com/datasets/saadaliyaseen/climate-and-atmospheric-conditions-data/data

Place your CSV in the `data/` folder; the app will automatically load the first CSV found.

---

## Development Notes

- Use `@st.cache_data` to cache data loading.
- Modular code: pages in `sections/`, helpers in `utils/`.

---

## Contact

- Jiaming Hu — jiaming.hu@efrei.net



