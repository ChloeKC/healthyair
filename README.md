Healthy Air Analysis & Alerts

Air Quality Category Prediction Using Machine Learning and the UCI Air Quality Dataset

Project Overview

Healthy Air is a machine learning project that analyses air-quality data and predicts air-quality categories using the UCI Air Quality Dataset.


Project Structure

healthyair/
│
├── data/
│   └── README.md
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_model_training.ipynb
│
├── src/
│   └── ...
│
├── models/
│   └── ...
│
├── environment.yml
├── requirements.txt
├── README.md
└── .gitignore

Requirements

The project can be reproduced using a standard Python virtual environment. Anaconda is not required.

# Software

Windows, macOS or Linux

Python 3.14

Git

JupyterLab

Internet connection

Python libraries

# The project uses:

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

# Option 1 — Standard Python Virtual Environment

This is the recommended setup for users who do not have Anaconda or Miniconda.

1. Clone the repository

git clone <repository-url>
cd healthyair

2. Create a virtual environment

On Windows PowerShell:

python -m venv .venv

3. Activate the environment

.venv\Scripts\Activate.ps1

On macOS/Linux:

source .venv/bin/activate

4. Upgrade pip

python -m pip install --upgrade pip

5. Install the project dependencies

pip install -r requirements.txt

6. Register the Jupyter kernel

python -m ipykernel install --user --name healthyair --display-name "Python (HealthyAir)"

7. Start JupyterLab

jupyter lab

When opening the notebooks, select the:

Python (HealthyAir)

kernel.

To verify the Python environment:

import sys
print(sys.executable)

The path should point to the project's .venv directory.

# Option 2 — Conda

Conda is optional. The project's development environment can also be recreated using the supplied environment.yml.

conda env create -f environment.yml
conda activate healthy_air

Start JupyterLab:

jupyter lab


Conda environment:

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

The exact package versions are recorded in requirements.txt


# Google Cloud

Google Cloud services including:

Google Cloud Storage (GCS)

BigQuery

Google Cloud authentication is separate from the Python environment.

Users who need to access the cloud-based pipeline must authenticate using their own Google Cloud account and the permissions provided for the project.

For local development, Google Cloud Application Default Credentials can be configured using:

gcloud auth application-default login

The Google Cloud CLI (gcloud) is installed separately from Python and is not installed through requirements.txt.


# Security

Do not store credentials or secrets in this repository.



# Dataset

The project uses the UCI Air Quality Dataset.

The dataset should be stored locally according to the instructions in the data/README.md file.


# Running the Project

After setting up the environment:

Open the project in JupyterLab.

Select the Python (HealthyAir) kernel.

Run the notebooks in the appropriate order.

Explore and clean the air-quality data.

Create the air-quality categories.

Train the baseline machine learning model.

Evaluate the model.

Apply preprocessing improvements.

Train and evaluate the final model.


# GitHub Workflow

After making changes:

git status
git add .
git commit -m "Describe your changes"
git push

Do not commit the Conda environment itself, `.venv`, Python cache files, or other generated files.

A `.gitignore` file should be used to exclude these files.


# Reproducibility

HealthyAir provides two environment setup options:

requirements.txt — recommended for users using standard Python and venv

environment.yml — optional setup for users using Conda


