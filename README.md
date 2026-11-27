# Healthy Air Analysis & Alerts

### Project Overview

Healthy Air is a machine learning project that analyses air quality data, categorises quality levels, predicts air-quality category one hour into the future. The classification task uses historical environmental measurements from the UCI Air Quality Dataset. Hourly air quality measurements collected from a monitoring device located in an urban Italian environment between March 2004 and February 2005. Ethical considerations include potential bias arising from data collected at a single location.

A reproducible design, the data pipeline obtains the raw dataset and stores it in Google Cloud Storage. This dataset will be retained unchanged, separately from processed datasets so that the processing steps can be reproduced. GCS will be used for object storage, with clear paths/versioning for the raw and processed data. Python scripts/notebooks will document the data acquisition, exploration, cleaning, storage and splitting procedures. For example, the creation of chronological train/evaluation/test datasets for time aware predictions. Ultimately, the project will investigate whether machine-learning classification can predict air quality categories, (GOOD/MODERATE/POOR) for an urban area, using recent environmental measurements. “What is the air quality now and what prediction in an hour’s time?”

### Sample classification task, with time-aware prediction:

Current time: 12:00 
↓
Information available at 12:00 
↓
CO, NO₂, NOx, benzene, temperature,
humidity, previous measurements, 
time features 
↓
Model 
↓
Predicted category at 13:00 
↓
GOOD / MODERATE / POOR/

### Project Pipeline

Raw Data(GCS)
↓
Validation
↓
Data Quality Checks
↓
Cleaning & Transformation
↓
Target-Label Creation
↓
Feature Engineering
↓
Train / Validation / Test Splits
↓
Model-Ready Dataset

### Project Structure

healthyair/
│
├── data
│   ├── features
│   │   └── air_quality_features.parquet
│   ├── processed
│   │   ├── air_quality_cleaned.csv
│   │   ├── air_quality_cleaned.parquet
│   │   ├── cross_validation
│   │   ├── evaluation.parquet
│   │   ├── test.parquet
│   │   └── train.parquet
│   └── raw
│       └── AirQualityUCI.csv
├── environment.yml
├── image.png
├── milestones
│   ├── Milestone 2.docx
│   └── Milestone1.docx
├── notebooks
│   ├── Untitled.ipynb
│   ├── data_cleaning.ipynb
│   ├── data_exploration.ipynb
│   ├── data_storage_gcs.ipynb
│   ├── feature_engineering.ipynb
│   ├── model_training.ipynb
│   └── model_training_mlflow.ipynb
├── reports
│   ├── HealthyAirBibliography.rtf
│   └── learning_curve.png
├── requirements.txt
├── src
│   ├── config.py
│   ├── data_cleaning.py
│   ├── data_quality.py
│   ├── data_splits.py
│   ├── feature_engineering.py
│   ├── gcs_storage.py
│   ├── gcs_utils.py
│   ├── modelling.py
│   ├── pipeline.py
│   └── training_pipeline.py
└── tests
|    └── tests.py
│
├── environment.yml
│
├── .env.example
|
├── requirements.txt
|
├── README.md
|
└── .gitignore

### Requirements and Setup

Clone repo
↓
Create .env from .env.example
↓
Configure GCP project + bucket
↓
Authenticate
↓
Run data_storage_gcs.ipynb or pipeline.py
↓
Generate processed/features datasets
↓
Train model

The project can be reproduced locally or Full GCS Pipeline This option reproduces the project's complete MLOps workflow.

First clone the repository:

git clone https://github.com/ChloeKC/healthyair.git

OR

https://github.com/ChloeKC/healthyair/archive/refs/heads/main.zip

Then:

Using a Python virtual environment



### Running HealthyAir


*Option 1:* Local Mode

The repository includes local copies of the dataset and generated artefacts, no Google Cloud setup is required.

All datasets necessary to reproduce the analysis are included in the repository.

*Option 2:* Google Cloud Storage Mode

Configure Google Cloud Project and Storage Bucket by creating a .env file from .env.example.

### Option 1. Python Virtual Environment (Local)

1. Open a terminal in the project folder:

   cd healthyair

2. Create a virtual environment:

   python -m venv .venv

3. Activate the environment:

   .venv\Scripts\Activate.ps1
   or
   source .venv/bin/activate

4. Install project requirements:

   pip install -r requirements.txt

5. Start JupyterLab

   jupyter lab



### Option 2 — Python Virtual Environment (GCS)

1. Open a terminal in the project folder:

   cd healthyair

2. Create a virtual environment:

   python -m venv .venv

3. Activate the environment:

   .venv\Scripts\Activate.ps1
   or
   source .venv/bin/activate

4. Install project requirements:

   pip install -r requirements.txt

5. Create a Google Cloud Project.
   Create a Google Cloud Storage bucket.

6. Copy .env.example to .env.

   cp .env.example .env

7. Update:
   PROJECT_ID=your-project-id BUCKET_NAME=your-bucket-name LOCATION=EU

8. Authenticate:

   gcloud auth login
   gcloud auth application-default login

10. Start JupyterLab

   jupyter lab

**Software**

Windows, macOS or Linux

Python 3.12.3

Github

JupyterLab

**Python libraries**

NumPy
Pandas
Matplotlib
SciPy
Scikit-learn
JupyterLab
IPykernel
Google Cloud Storage
Google Cloud BigQuery
gcsfs

### Google Cloud - Optional Google Cloud Storage Configuration 

Google Cloud Storage (GCS)

BigQuery

Google Cloud Application Default Credentials can be configured using:

gcloud auth login

gcloud auth application-default login

gcloud config set project healthy-air-analysis

gcloud services enable storage.googleapis.com


### Dataset

The project uses the UCI Air Quality Dataset.
Hourly air quality measurements collected from a monitoring device located in an urban Italian environment between March 2004 and February 2005.

URL: https://www.kaggle.com/datasets/dakshbhalala/uci-air-quality-dataset/data

Dataset: Air Quality (AirQualityUCI) Dataset

Original Source: UCI Machine Learning Repository
Archive: https://archive.ics.uci.edu/dataset/387/air+quality


Stored Data GCS:

gs://BUCKET/

├── raw/

│   ── uci-air-quality/

│       ── v1/

│           ── AirQualityUCI.csv

└── processed/

|         ── v1/
    
|         ── airquality.parquet

### GitHub

After making changes:

git status
git add .
git commit -m "..."
git push

### Reproducibility

HealthyAir provides two environment setup options:

requirements.txt — users using standard Python and venv

environment.yml — setup for users using Conda, etc.

python3 data_storage_gcs.py (Linux)

python data_storage_gcs.py

### Overall Shell User Guide 

User


   ├── Clone HealthyAir

   ├── Create Python .venv

   ├── pip install -r requirements.txt

   ├── Authenticate to Google Cloud

   ├── Access HealthyAir GCS bucket

   └── Run pipeline
   

