# healthyair
Air Quality Analysis &amp; Alerts - Air quality category prediction using machine learning and the UCI Air Quality Dataset

Initial project structure
        ↓
Add UCI dataset
        ↓
Data cleaning
        ↓
Create air-quality categories
        ↓
Train baseline model
        ↓
Evaluate model
        ↓
Improve preprocessing
        ↓
Final model

Open Anaconda Prompt to start...

conda activate healthy_air

cd C:\Users\Chloe\Documents\DataHandling\healthyair

jupyter lab

# HealthyAir — Requirements & Setup

## Requirements

The HealthyAir project requires:

- Windows, macOS or Linux
- Python 3.14
- Anaconda or Miniconda
- JupyterLab
- Git
- Internet connection for downloading the dataset and Python packages

### Python libraries

The project uses:

- NumPy
- Pandas
- Matplotlib
- Scikit-learn
- Jupyter / IPykernel

## 6. Recreating the environment

If an `environment.yml` file is included in the repository, the environment can be recreated with:

```bash
conda env create -f environment.yml
conda activate healthy_air
```

This allows other users to install the required Python packages without manually identifying each dependency.

## 7. GitHub workflow

After making changes:

```bash
git add .
git commit -m "Describe your changes"
git push
```

Do **not** commit the Conda environment itself, `.venv`, Python cache files, or other generated files.

A `.gitignore` file should be used to exclude these files.


healthy_air/
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
├── README.md
└── .gitignore

| Package | Version |
|---|---:|
| Python | **3.14.7** |
| NumPy | **2.5.3** |
| Pandas | **3.0.6** |
| Matplotlib | **3.11.1** |
| Scikit-learn | **1.9.1** |
| JupyterLab | **4.6.4** |
| IPykernel | **7.3.0** |
| SciPy | **1.18.1** |