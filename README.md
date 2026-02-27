# Real Estate AI Suite

> A full-stack ML web application for Gurgaon real estate — price prediction, analytics, and AI-powered property recommendations.

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-multipage-red)](https://streamlit.io)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML%20Pipeline-orange)](https://scikit-learn.org)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-purple)](https://plotly.com)

> 🌐 **Live Demo:** [realestate-analysis-ml.streamlit.app](https://realestate-analysis-ml.streamlit.app/)

---

## What is this?

An end-to-end data science project built on Gurgaon real estate data — from raw web-scraped data to a deployed multi-page Streamlit app. Covers the full ML lifecycle: data collection → preprocessing → EDA → feature engineering → model selection → deployment.

---

## Architecture

```
Raw Data (99acres web scrape)
        │
        ▼
Data Collection Notebooks
        │
        ▼
Data Preprocessing + Outlier/Missing Value Treatment
        │
        ▼
EDA + Feature Engineering
        │
        ├──────────────────────────────────┐
        ▼                                  ▼
ML Pipeline (Price Predictor)    Similarity Matrices (Recommender)
  • Encoding + Scaling             • Cosine Similarity (3 matrices)
  • Random Forest / XGBoost        • Location distance matrix
  • Log-transform target (expm1)   • Weighted ensemble scoring
        │
        ▼
Streamlit Multi-page App (3 modules)
  ├── 📊 Analytics Dashboard
  ├── 🔮 Price Predictor
  └── 🤖 Property Recommender
```

---

## The Three Modules

### 📊 Analytics Dashboard
Interactive Plotly visualizations built on cleaned Gurgaon property data.
- **Sector map** — price per sqft and built-up area plotted on a live Mapbox map
- **Area vs Price scatter** — filterable by flat/house, colored by BHK
- **Price distribution** — histogram + box plot comparing flats vs houses
- **BHK analysis** — donut chart + box plot, filtered to ≤4 BHK
- **Feature word cloud** — most common property amenities at a glance
- **Live key stats** — total properties, avg price, avg price/sqft, most common BHK

### 🔮 Price Predictor
Predicts Gurgaon property prices using a pre-trained scikit-learn pipeline.

**Input Features (12 total):**
| Feature | Type |
|---|---|
| Property Type (flat/house) | Categorical |
| Sector | Categorical (location) |
| Bedrooms, Bathrooms, Balconies | Ordinal |
| Built-up Area (sqft) | Continuous |
| Servant Room, Store Room | Binary |
| Furnishing Type | Categorical |
| Luxury Category | Ordinal |
| Floor Category | Ordinal |
| Age/Possession Status | Categorical |

**Pipeline:**
- Categorical encoding (OneHot/Ordinal via ColumnTransformer)
- Log-transform on target price → `np.expm1` on output
- Output: price range = `[predicted - 0.22 Cr, predicted + 0.22 Cr]`
- Model stored as `pipeline.pkl` (loaded via Google Drive using `gdown`)

### 🤖 Property Recommender
Content-based recommender using three cosine similarity matrices.

**Similarity scoring:**
```
final_score = 0.5 × cosine_sim1  (location/proximity features)
            + 0.8 × cosine_sim2  (price features)
            + 1.0 × cosine_sim3  (amenities/property features)
```
- Location search: finds all properties within a user-defined radius (km) using a precomputed distance matrix
- Recommendations: top-N properties sorted by weighted similarity score
- Match scores displayed as progress bars

---

## ML Details

| Aspect | Details |
|---|---|
| Dataset | Gurgaon properties scraped from 99acres |
| Target Variable | Price (Crores INR), log-transformed |
| Feature Engineering | Luxury score, floor category, age buckets, built-up area imputation |
| Outlier Treatment | IQR-based, sector-stratified |
| Model Selection | Compared Linear Regression, Ridge, Lasso, Random Forest, XGBoost, Gradient Boosting |
| Final Model | Best performer selected via cross-validation (see `Model Selection/` notebooks) |
| Deployment | `pipeline.pkl` hosted on Google Drive, loaded at runtime via `gdown` |

---

## Project Structure

```
Real_Estate/
├── Data Collection/              # Web scraping notebooks (99acres)
├── Data Preprocessing/           # Cleaning, merging, type fixing
├── Outlier-Missing_values/       # IQR outlier treatment, missing value imputation
├── EDA/                          # Exploratory analysis notebooks
├── Feature_selection-engineering/ # Feature creation, encoding strategy
├── Model Selection/              # Model comparison, cross-validation, final selection
├── pages/
│   ├── Analysis_App.py           # Analytics Dashboard page
│   ├── Price_Predictor.py        # Price Predictor page
│   ├── Recommender.py            # Recommender System page
│   ├── Analysis_datasets/        # CSVs and pickles for analytics
│   │   ├── data_viz1.csv
│   │   └── feature_text.pkl
│   ├── Recommender_System/       # Cosine similarity + location distance matrices
│   │   ├── cosine_sim1.pkl
│   │   ├── cosine_sim2.pkl
│   │   ├── cosine_sim3.pkl
│   │   └── location_distance.pkl
│   └── df.pkl                    # Cleaned dataframe for predictor dropdowns
├── Home.py                       # Streamlit entry point + navigation
├── requirements.txt
└── README.md
```

---

## Setup & Run

```bash
# 1. Clone
git clone https://github.com/DEVJHAWAR11/Real_Estate.git
cd Real_Estate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run Home.py
```

> Note: `pipeline.pkl` is downloaded automatically at runtime from Google Drive via `gdown`. No manual setup needed.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web App | Streamlit (multi-page) |
| ML Pipeline | Scikit-learn (ColumnTransformer + Estimator) |
| Data Processing | Pandas, NumPy |
| Visualizations | Plotly Express, Matplotlib, Seaborn, WordCloud |
| Model Storage | Google Drive + gdown |
| Deployment | Streamlit Community Cloud |

---

## Author

**Dev Jhawar** — [GitHub](https://github.com/DEVJHAWAR11) | KIIT University
