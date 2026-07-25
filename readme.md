# Regression Model for Used Car Price Estimation

**Demonstration of model prediction:** https://car-price-prediction-eda-ml.onrender.com/

## Table of Contents
- [Overview](#overview)
- [Data](#data)
- [Model Variables](#model-variables)
- [Data Extraction and Transformation from JSON](#data-extraction-and-transformation-from-json)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Modeling Approach](#modeling-approach)
- [Results](#results)

## Overview
This project builds a model that estimates the value of used cars. The model uses data from the Polish car listing market.

The model looks at key technical and equipment features. It helps to find the real market value of a car.

This tool might be useful for professional sellers. It helps them set the right price for their offers. It is also useful for buyers. Buyers can use it to find good deals and avoid paying too much for a car.

## Data
The training data comes from public car listings on Otomoto. The data was collected only for non-commercial, academic purposes. Cleaned dataset has about 5000 records and 29 features including target (price).

## Model Variables
| Feature | Type | Description |
| :--- | :--- | :--- |
| **Car age** | Numerical | Number of years since the car's production year. |
| **Engine capacity** | Numerical | Engine displacement, in cubic centimeters (cm3). |
| **Mileage** | Numerical | Total distance driven by the car, in kilometers. |
| **Engine power** | Numerical | Power of the engine, in horsepower (HP). |
| **Equipment count** | Numerical | Number of extra equipment features in the car. |
| **Brand** | Categorical | Car manufacturer. It shows the car's prestige and market segment. |
| **Gearbox** | Categorical | Type of transmission (e.g., manual, automatic). |
| **Fuel type** | Categorical | Type of fuel (e.g., Petrol, Diesel, LPG, Hybrid, Electric). |
| **Drivetrain** | Categorical | Type of driven axle (e.g., front-wheel, rear-wheel, 4x4). |
| **Voivodeship** | Categorical | Polish region where the car is registered or sold. |
| **Body type** | Categorical | Type of car body (e.g., Sedan, Estate, SUV, Hatchback). |
| **Color** | Categorical | Color of the car's paint. |
| **Seller type** | Categorical | Professional or private seller. |
| **Leather upholstery** | Categorical | Shows if the seats have leather upholstery (Yes/No). |
| **Imported** | Categorical | Shows if the car is from a Polish dealership (Yes/No). |
| **Authorized service** | Categorical | Shows if the car had regular service at an Authorized Service Station (Yes/No). |
| **Panoramic roof** | Categorical | Shows if the car has a glass roof over the passenger space (Yes/No). |
| **LED headlights** | Categorical | Shows if the car has front headlights made with LED technology (Yes/No). |
| **First owner** | Categorical | Shows if the car has had only one owner since it was new (Yes/No). |
| **Automatic air conditioning** | Categorical | Shows if the car has an electronically controlled AC system (Yes/No). |
| **Rear view camera** | Categorical | Shows if the car has a video system that helps with reversing (Yes/No). |
| **Heated seats** | Categorical | Shows if the car has electric seat heating, front or rear (Yes/No). |
| **Cruise control** | Categorical | Shows if the car has a system for automatic speed control (Yes/No). |
| **Adaptive cruise control** | Categorical | Shows if the car has an advanced cruise control that keeps a safe distance (Yes/No). |
| **Traffic sign recognition** | Categorical | Shows if the car has a camera system that reads traffic signs (Yes/No). |
| **Wireless charger** | Categorical | Shows if the car has a wireless phone charging pad (Yes/No). |
| **LED rear lights** | Categorical | Shows if the car has rear lights made with LED technology (Yes/No). |
| **Android Auto** | Categorical | Shows if the car has a system that connects a smartphone to the media screen (Yes/No). |

## Data Extraction and Transformation from JSON
The data collection and processing has two steps. Scripts in the `data_prep` folder do this work:

1. **Data extraction** (`extract_data.py`): This script reads raw data from Otomoto in JSON format. It searches through the JSON structure. Then it builds a table (DataFrame) from the data. The script saves this table to `extracted_listings.csv`.

2. **Data transformation** (`transform_data.py`): After extraction, much of the data is in the wrong format. For example, some values have currency signs or units like "km" and "cm3". This script reads the `extracted_listings.csv` file. It cleans the data and saves the result to `cleaned_listings.csv`. This final file is ready for analysis.

## Explore the data

Open the notebook to see the exploratory data analysis (EDA):
```bash
jupyter notebook notebooks/exploratory_data_analysis.ipynb
```

## Project Structure
```
car-price-prediction-eda-ml/
├── data/                       # Local working directory — not part of this repository
│   ├── car_data/               # Input: raw Otomoto listings exported from an Apify scraper
│   ├── extracted_listings.csv  # Output of data_prep/extract_data.py
│   └── cleaned_listings.csv    # Output of data_prep/transform_data.py — input for training
├── data_prep/                  # Scripts for data extraction and cleaning
│   ├── extract_data.py
│   └── transform_data.py
├── notebooks/                  # Exploratory Data Analysis
│   └── exploratory_data_analysis.ipynb
├── src/                        # Core pipeline code
│   ├── config.py               # Project settings and constants
│   ├── pipeline.py             # Preprocessing pipeline
│   ├── transformers.py         # Custom transformers
│   ├── train.py                # Model training logic
│   └── evaluate.py             # Model evaluation metrics
├── optimization/               # Hyperparameter tuning
│   ├── hyperparameters.py
│   ├── run_tuning.py
│   └── tuning_results.json
├── models/                     # Saved model and metadata
│   ├── car_price_model.pkl
│   └── model_metadata.pkl
├── app/                        # FastAPI web application
│   ├── main.py                 # App setup, startup and error handling
│   ├── settings.py             # App configuration (CARAPI_* env variables)
│   ├── model_service.py        # Loads the model and serves predictions
│   ├── schemas.py              # Pydantic request and response models
│   ├── labels.py               # English labels for fields and categories
│   ├── routers/                # API endpoints
│   │   ├── predict.py          # POST /api/v1/predict
│   │   ├── metadata.py         # GET /api/v1/form-options, /api/v1/model-info
│   │   └── health.py           # GET /health, /health/ready
│   └── static/                 # Frontend form (HTML, CSS, JS)
│       ├── index.html
│       ├── styles.css
│       └── app.js
├── run_pipeline.py             # Main script: trains and saves the final model
├── requirements.txt
└── readme.md
```

The `data/` directory is excluded. The raw scraper export is a single ~365 MB JSON file covering about 10 500 listings, and the listing content itself belongs to Otomoto — it was collected for non-commercial academic use only and is not redistributed here.

## Modeling Approach
The project uses a `scikit-learn` pipeline to process the data before training. The pipeline has these steps:

1. **Outlier removal**: Removes cars with a price far from the normal range, based on brand.
2. **Missing value imputation**: Fills missing values. It uses the group median or group mode for related columns, and K-Nearest Neighbors (KNN) for some numerical columns.
3. **Rare category handling**: Groups rare brands and colors into an "Other" category.
4. **Feature engineering**: Creates new features, like the ratio of mileage to car age.
5. **Scaling**: Scales numerical features with `StandardScaler`.
6. **Encoding**: Converts categorical features into numbers with One-Hot Encoding.

The project tests three regression models:
- XGBoost
- Random Forest
- Linear Regression

Each model predicts the logarithm of the price. This helps because car prices do not follow an even distribution. The project uses `GridSearchCV` with 5-fold cross-validation to find the best hyperparameters for each model.

## Results
The table below shows the test set performance for each model, after hyperparameter tuning.

| Model | MAPE (%) | MAE (PLN) | RMSE (PLN) |
| :--- | :---: | :---: | :---: |
| **XGBoost** | **18.34** | **11 737.8** | **22 681.31** |
| Random Forest | 19.94 | 13 312.02 | 26 388.76 |
| Linear Regression | 21.18 | 14 092.82 | 27,846.51 |

XGBoost has the best performance on the test set. The project uses XGBoost as the final model. You can find the saved model in `models/car_price_model.pkl`, and its metadata in `models/model_metadata.pkl`.