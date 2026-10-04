# Healthy Air Analysis & Alerts

### Project Overview

**Healthy Air is a machine learning project that endeavours to analyse air quality data and categorise quality levels, using UCI Air Quality Dataset, https://www.kaggle.com/datasets/dakshbhalala/uci-air-quality-dataset/data.**

*'The World Health Organisation (WHO) estimates show that more than 400,000 premature deaths are attributable to poor air quality in Europe annually. In Ireland, the number of premature deaths attributable to air pollution is estimated at 1,510 people and is mainly due to cardiovascular disease. The WHO has described air pollution as the "single biggest environmental health risk".

Ireland’s air quality currently is good, relative to other European Union (EU) Member States, but maintaining this standard is a growing challenge. Despite our monitored air quality being within EU limit values, the levels of particulate matter is of growing concern, especially during the winter months when domestic solid fuel burning can directly impact on air quality and on our health. In our larger urban areas we face potential exceedances of nitrogen dioxide limit values unless we reduce our dependence on the private motor car.' EPA*

The project will investigate whether machine-learning classification can predict the air-quality category using recent environmental measurements.

**Sample classification task, with time-aware prediction:**

Current time: 12:00

Information available at 12:00

        ↓
        
CO, NO₂, NOx, benzene, temperature,
humidity, 

previous measurements, time features

        ↓
        
       MODEL
       
        ↓
        
Predicted category at 13:00

        ↓
        
GOOD / MODERATE / POOR/

### Project Structure

healthyair/

── data/

|   ── README.md

── notebooks/

|   ── data_exploration.ipynb
   
|   ── data_cleaning.ipynb
   
|   ── model_training.ipynb

── src/
|  ── ...

── models/
|  ── ...

── environment.yml

── requirements.txt

── README.md

── .gitignore

### Preliminary Design

 UCI Air Quality .csv
 
   Local download

GCS: raw/air_quality.csv

  Clean / preprocess

  Train/Dev/Test

8-fold stratified cross-val.

   GCS: sharded

Model training/eval./testing

### Requirements

The project can be reproduced using a standard Python virtual environment, .venv.

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


1. Clone the repository
git clone <https://github.com/ChloeKC/healthyair>
cd healthyair

2. Create a virtual environment
python -m venv .venv

3. Activate the environment
.venv\Scripts\Activate.ps1
or
source .venv/bin/activate

4. Upgrade pip
python -m pip install --upgrade pip

5. Install project dependencies
pip install -r requirements.txt

6. Start JupyterLab
jupyter lab


### Option 2 — Conda

conda env create -f environment.yml

conda activate healthy_air

jupyter lab


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

Google Cloud services including:

Google Cloud Storage (GCS)

BigQuery

Google Cloud authentication is separate from the Python environment.

For local development, Google Cloud Application Default Credentials can be configured using:

gcloud auth login

gcloud config set project YOUR_PROJECT_ID

gcloud auth application-default login

gcloud services enable storage.googleapis.com

Google Cloud CLI (gcloud) is installed separately from Python and is not installed through requirements.txt.

Users who need to access the cloud-based pipeline authenticate using their Google Cloud account.

gcloud auth application-default login


### Dataset

The project uses the UCI Air Quality Dataset.

Stored Data GCS:

gs://BUCKET/

├── raw/

│   └── uci-air-quality/

│       └── v1/

│           └── AirQualityUCI.csv

└── processed/

    └── v1/
    
        └── airquality.parquet


### Running the Project

After setting up the environment:

Open the project in JupyterLab.
Run the notebooks in the appropriate order.
Explore and clean the air-quality data.
Create the air-quality categories.
Train the baseline machine learning model.
Evaluate the model.
Apply preprocessing improvements.
Train and evaluate the final model.


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

### Overall Shell User Guide 

User


   ├── Clone HealthyAir

   ├── Create Python .venv

   ├── pip install -r requirements.txt

   ├── Authenticate to Google Cloud

   ├── Access HealthyAir GCS bucket

   └── Run pipeline

       Raw → Clean → Features
             ↓
       Train → Validate → Test
             ↓
          Results

## Milestone 1

**My focus for milestone 1 is creating the data pipeline architecture for the project. A reproducible design, that obtains the raw dataset, stores it in Google Cloud Storage, creates appropriate chronological train/evaluation/test datasets, and stores the resulting data for analysis.**

### Process/Pipeline:

UCI Air Quality Dataset

          ↓
      Raw data
      
          ↓
 Google Cloud Storage
 
          ↓
   Basic preparation
   
          ↓
 Chronological splits
 
          ↓
 Google Cloud Storage

### Dataset and Code

The UCI Air Quality Dataset  contains hourly air-quality and environmental measurements, including CO, NO₂, NOx, benzene, temperature, relative humidity and absolute humidity. The chronological ordering will be retained because the data represents time series records which will be important to maintain for the future prediction task.

The final preprocessing, target-label definition, feature engineering and machine-learning approach will be investigated in a later milestone. I will consider whether the data is best used for historical air-quality classification or prediction of a future air-quality category from previous observations.

The dataset will be stored as raw data and retained unchanged. The raw dataset will be retained separately from processed datasets so that the processing steps can be reproduced. Google Cloud Storage will be used for object storage, with clear paths/versioning for the raw and processed data. Python scripts/notebooks will document the data acquisition, storage and splitting procedures.

### Preliminary Train/Test Splits

70%                15%          15%

TRAIN              DEV          TEST

### Criterion and Healthy Air Approach:

1. Raw data storage:
The original UCI Air Quality dataset is stored in Google Cloud Storage (GCS) as the raw source.
An untouched local copy is stored for development.
2. Processed data storage & formats:
Raw data: CSV. 
Processed data: Parquet in GCS as more efficient for ML/tabular data.
3. Database / object storage decision:
Used GCS object storage for raw and processed files.
BigQuery will be for structured analytical/query access.
4. Data versioning:
Raw data is kept immutable and dataset versions are identified using filenames/folders and Github for tracking. 
5. Data access:
Python accesses GCS using google-cloud-storage / gcsfs; BigQuery through google-cloud-bigquery; authentication through Google Cloud credentials.
6. Data split / validation:
Use a train/evaluation/test split, or potentially stratified cross-validation. The split will happen before model training and preprocessing fitted only on training data to avoid leakage.
7. Feature description:
Sensor/environmental variables used to predict the air-quality category, e.g. NO₂, CO, NOx, benzene, temperature, RH, absolute humidity, etc.
8. Data types/formats
Numerical sensor measurements → float; timestamps → datetime; category → categorical/string; raw → CSV; processed → Parquet; cloud analytical table → BigQuery.
9. Reproducibility of data collection:
The exact UCI dataset, source URL, dataset version/date, download procedure and code used to obtain it are all documented in README.md.
10. Reproducibility of preprocessing: Milestone 2. Put cleaning/category creation in notebooks.


### The following will be investigated:

Feature selection: The available UCI air-quality and environmental measurements will first be retained and documented.

Air-quality categories: The final definition of categories such as Good, Moderate or Poor has not been completed at this stage.

Target labels: The appropriate target variable will depend on the final modelling approach, investigated during preprocessing and selected in milestone 2.

Machine-learning model: The focus was on preparing and storing reproducible datasets for future modelling.

Model comparison: Models such as Decision Tree and Random Forest will be compared in later milestone.

Model evaluation: Accuracy, precision, recall, F1-score and other evaluation measures will be produced during the ML stage.

Future prediction: This will be investigated after the initial data infrastructure has been established.

Detailed ML analysis: More detailed analysis, including feature engineering, model selection, hyperparameter tuning and model evaluation, will be carried out in later milestones.

### Milestone 2 Plans:

During Milestone 2, a preprocessing notebook will clean the data, investigate the creation of target labels as the final target label methodology has not yet been fixed. Then I can determine whether the focus will be on historical classification or prediction of a future air-quality category using recent observations.

Cleaning/category creation will be supplied in notebooks or Python scripts in src/, with procedures for missing values, invalid measurements, feature construction and category thresholds. The focus of Milestone 1 is therefore on data acquisition, raw data storage, reproducible data splitting and storage of the resulting datasets, providing a foundation for the subsequent preprocessing and machine-learning stages.

Stored data

↓
Preprocessing

↓
Target-label definition

↓
Feature engineering

↓
ML modelling