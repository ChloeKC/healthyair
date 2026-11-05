# Healthy Air Analysis & Alerts

### Project Overview

Healthy Air is a machine learning project that analyses air quality data, categorises quality levels, predicts air-quality category one hour into the future. The classification task uses historical environmental measurements from the UCI Air Quality Dataset. Hourly air quality measurements collected from a monitoring device located in an urban Italian environment between March 2004 and February 2005. Ethical considerations include potential bias arising from data collected at a single location.

A reproducible design, the data pipeline obtains the raw dataset and stores it in Google Cloud Storage. This dataset will be retained unchanged, separately from processed datasets so that the processing steps can be reproduced. GCS will be used for object storage, with clear paths/versioning for the raw and processed data. Python scripts/notebooks will document the data acquisition, exploration, cleaning, storage and splitting procedures. For example, the creation of chronological train/evaluation/test datasets for time aware predictions. Ultimately, the project will investigate whether machine-learning classification can predict air quality categories, (GOOD/MODERATE/POOR) for an urban area, using recent environmental measurements. “What is the air quality now and what prediction in an hour’s time?”

### Sample classification task, with time-aware prediction:

Current time: 12:00 ↓

Information available at 12:00 ↓

CO, NO₂, NOx, benzene, temperature,
humidity, previous measurements, 
time features ↓

Model ↓

Predicted category at 13:00 ↓

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
├── data/
│   ├── raw/
│   ├── processed/
│   └── features/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_feature_engineering.ipynb
│
├── src/
│   ├── data_load_gcs.py
│   ├── data_quality.py
│   └── data_storage_gcs.py
│
├── reports/
│   ├── milestone1.pdf
│   └── milestone2.pdf
│
├── tests/
│
├── environment.yml
├── requirements.txt
├── README.md
└── .gitignore

### Requirements and Setup

The project can be reproduced using a Python virtual environment, first clone the repository:

   git clone <https://github.com/ChloeKC/healthyair>

**Software**

Windows, macOS or Linux

Python 3.14

Git

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


### Option 1 — Python Virtual Environment

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


### Option 2 — Conda

1. Create healthy_air environment

   conda env create -f environment.yml

2. Activate the environment

   conda activate healthy_air

3. Open the cloned project folder

   cd ... 

4. Register the Jupyter kernel

   python -m ipykernel install --user --name healthy_air --display-name "Python (HealthyAir)"

5. Start JupyterLab

   jupyter lab

6. Select the kernel

   In JupyterLab, select: Python (HealthyAir)
   
7. Verify environment
   
   import sys
   
   print(sys.executable)

**Conda environment:**

healthy_air
Package Versions:
Python 3.14.7
NumPy 2.5.3
Pandas 3.0.6
Matplotlib 3.11.1
Scikit-learn 1.9.1
SciPy 1.18.1
JupyterLab 4.6.4
IPykernel 7.3.0

### Google Cloud

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
   

## Milestone 2

My focus for milestone 2 is further development of data pipeline architecture, target-label definition, data exploration and preprocessing, and feature engineering. This prepares the dataset for the machine-learning stage maintaining quality, traceability, and reproducibility.

### Dataset

The UCI Air Quality Dataset contains hourly air-quality and environmental measurements, including CO, NO₂, NOx, benzene, temperature, humidity from an Italian town. Ethical considerations include potential bias arising from data collected at a single location. The chronological ordering will be retained because the data represents time series records which will be important to maintain for future prediction tasks.

### Data Pipeline Architecture: 

Healthy Air currently operates as a batch-processing pipeline, where historical air quality measurements are processed to generate reproducible training datasets for model training. However, the architecture could be updated to support streaming real time data ingestion. This is also true for sharded data storage, to support future implementation scalability. The current pipeline design mimics Apache Beam data-processing with python notebooks. Raw observations are validated against defined quality rules, cleaned, transformed, and converted into model-ready datasets. The resulting datasets should be stored separately from the raw source data in Google Cloud Storage. The current implementation uses file-based storage because the dataset is relatively small. Processed datasets generated during cleaning, feature engineering, and dataset splitting are stored as Parquet files. The proposed architecture remains compatible with Google Cloud Storage and Big Query for future scaling and deployment.

### Data Pipeline Architecture: 

Healthy Air currently operates as a batch-processing pipeline, where historical air quality measurements are processed to generate reproducible training datasets for model training. However, the architecture could be updated to support streaming real time data ingestion. This is also true for sharded data storage, to support future implementation scalability. The current pipeline design mimics Apache Beam data-processing with python notebooks. Raw observations are validated against defined quality rules, cleaned, transformed, and converted into model-ready datasets. The resulting datasets should be stored separately from the raw source data in Google Cloud Storage. The current implementation uses file-based storage because the dataset is relatively small. Processed datasets generated during cleaning, feature engineering, and dataset splitting are stored as Parquet files. The proposed architecture remains compatible with Google Cloud Storage and Big Query for future scaling and deployment.

### Target Label Definition NO₂(1 hour ahead):

The UCI Air Quality Dataset contains hourly air-quality and environmental measurements, including CO, NO₂, NOx, benzene, temperature, relative humidity and absolute humidity. The chronological ordering will be retained because the data represents time series records which will be important for the future prediction task. I’ve chosen Nitrogen Dioxide NO2 as the target label as it’s a direct air-pollution measurement, with recognised health impacts, and it can be converted into categories:
GOOD      NO2 <= 100
MODERATE  100 < NO2 <= 200
POOR      NO2 > 200
The target label is generated by predicting the NO₂ observation one time step forward. Features at time t are used to predict the air-quality category at time t+1 hour. This approach ensures that only information available at prediction time is used and helps prevent data leakage.

### Data Exploration, Cleaning and Preprocessing:

EDA, cleaning and feature creation notebooks are developed in notebooks/ and utilized in .py scripts supplied in src/. For now, the focus of Milestone 2 is on reproducible data quality checks, cleaning, feature engineering, splitting and storage of the resulting datasets. This should hopefully provide the foundation for the subsequent machine-learning stage.

Raw Dataset

↓

Validation

↓

Good Rows 

↓

Processing

↓

Bad Rows  

↓

Quarantined Dataset

### Three Notebooks

1.	data_exploration.ipynb

•	Data acquisition
•	Basic profiling
•	Missing data analysis
•	Duplicate detection 
•	Distribution analysis
•	Correlation analysis 
•	Time-series inspection
•	Documented findings


2.	data_cleaning.ipynb 

This preprocessing notebook will clean the data with procedures for missing values, invalid measurements and potential issues(leakage risks). 

Conclusions:

•	Replace -200 with NaN.
•	Create Datetime column.
•	Remove mostly incomplete records.
•	Generate lag features for modelling.

3.	feature_engineering.ipynb
 
Feature generation obtains information the model will learn from the dataset: 
Hourly air quality statistics.

Examples:
avg_co
avg_nox
avg_no2
temperature_avg
humidity_avg

•	rolling averages
•	time-of-day features
•	environmental indicators

### Three Python Scripts

1.	data_load_gcs.py

Load raw dataset from Google Cloud Storage .

2.	data_quality.py

Data contract: metrics for bad rows, empty files, etc. Incoming records are validated against defined quality rules, invalid observations are quarantined, data-quality metrics are generated, and the remaining records are transformed into a model-ready dataset. ETL processing: Read → Validate → Transform → Aggregate

   1.	missing_values
   2.	invalid_temperature
   3.	invalid_humidity
   4.	duplicate_records

3.	data_storage_gcs.py

The dataset is divided chronologically into training (70%), validation (15%), and test (15%) subsets. A temporal split wis used as aim is to predict future air-quality categories using previous measurements. This approach reflects real-world deployment and reduces risk of temporal data leakage. The UCI Air Quality dataset is small enough to be stored as CSV and Parquet files in Google Cloud Storage.


### The following will be investigated:

Detailed ML analysis: More detailed analysis, including feature engineering, model selection, hyperparameter tuning and model evaluation, will be carried out in later milestones.

ML analysis: model selection, hyperparameter tuning and model evaluation.

Model comparison: Models such as Logistic Regression, Random Forest and SVM will be compared.

1.	Primary model: Random Forest 
2.	Secondary model: SVM

Model evaluation: Confidence and other evaluation measures will be produced during the ML stage.

Evaluate using:

•	Accuracy
•	Precision
•	Recall
•	F1 Score
•	Confusion Matrix