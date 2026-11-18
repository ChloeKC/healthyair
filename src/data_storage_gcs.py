# HealthyAir - Google Cloud Storage configuration

# This notebook demonstrates an end-to-end data engineering workflow using the UCI Air Quality dataset and Google Cloud Platform (GCP).
#    1. Create/check the Google Cloud Storage bucket.
#    2. Upload the unchanged raw UCI Air Quality CSV.
#    3. Create chronological train/dev/test splits.
#    4. Upload the processed splits to GCS.
#   1. Installs the required Python libraries.
#   2. Configures GCP authentication and project settings.
#   3. Creates a Google Cloud Storage (GCS) bucket.
#   4. Downloads the raw Titanic CSV and stores it in GCS.
#   5. Creates stratified train/dev/test datasets and 8-fold cross-validation splits.
#   6. Stores the resulting shards back in GCS.
#   7. Loads the raw data into BigQuery, with an optional PostgreSQL/Cloud SQL path.
#   8. Verifies the bucket contents and reads a shard directly from GCS with Pandas.

from pathlib import Path
import pandas as pd
from google.cloud import storage

print("Google Cloud Storage imported successfully")

PROJECT_ID = "healthy-air-analysis"
BUCKET_NAME = "uci_air_quality"
LOCATION = "EU"

print(f"Project: {PROJECT_ID}")
print(f"Bucket: gs://{BUCKET_NAME}")


# Healthy Air Project folders 
# ---------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data_raw" / "AirQualityUCI.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# GCS paths
# ---------------------------------------------------------------------
RAW_GCS_PATH = "/uci-air-quality/v1/AirQualityUCI.csv"
PROCESSED_GCS_PATH = "processed/v1/"

print("Raw data path:", RAW_GCS_PATH)
print("Processed data prefix:", PROCESSED_GCS_PATH)

LOCAL_FILE = "../data/raw/AirQualityUCI.csv"
GCS_FILE = "raw/uci-air-quality/v1/AirQualityUCI.csv"

# GCS - Bucket
# ---------------------------------------------------------------------

def create_gcs_bucket(BUCKET_NAME, PROJECT_ID, LOCATION):
    """Create a GCS bucket if it does not already exist."""
    client = storage.Client(project=PROJECT_ID)

    if client.lookup_bucket(BUCKET_NAME):
        print(f"Bucket 'gs://{BUCKET_NAME}' already exists.")
        return

    bucket = client.bucket(BUCKET_NAME)
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket = client.create_bucket(bucket, location=location)
    print(f"Successfully created bucket: gs://{BUCKET_NAME}")
    

create_gcs_bucket(BUCKET_NAME, PROJECT_ID, LOCATION)

def upload_to_gcs(BUCKET_NAME, source_file_name, destination_blob_name):
    """Upload a local file to a GCS object path."""
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)
    print(
        f"Uploaded {local_path} -> "
        f"gs://{BUCKET_NAME}/{gcs_path}"
    )


upload_to_gcs(BUCKET_NAME, LOCAL_RAW_PATH, gcs_path)



blob = bucket.blob(GCS_FILE)
blob.upload_from_filename(LOCAL_FILE)

print(f"Uploaded: gs://{BUCKET_NAME}/{GCS_FILE}")

# Raw data
# ---------------------------------------------------------------------

def upload_raw_data(bucket):
    """Upload the unchanged raw UCI dataset."""
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw dataset not found:\n{RAW_FILE}\n\n"
            "Place AirQualityUCI.csv in data/raw/ before running the script."
        )

    upload_file(bucket, RAW_FILE, RAW_GCS_PATH)

# Partition Data: Train / Dev / Test + 8-Fold CV
# First create an 70% train / 15% dev / 15% test split.
# The 8-fold cross-validation split is then generated from the training set only, reducing the risk of dataleakage.
# The splits are stored in the `data/processed` folder and uploaded to GCS.

df = pd.read_csv(LOCAL_RAW_PATH)

print("Dataset shape:", df.shape)
display(df.head())

# Stratified Train (80%), Dev (10%), Test (10%) split
train_df, temp_df = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["Survived"],
)

dev_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    random_state=42,
    stratify=temp_df["Survived"],
)

# Generate 8-fold Stratified Cross-Validation folds from TRAIN only
skf = StratifiedKFold(n_splits=8, shuffle=True, random_state=42)
cv_folds = {}

for fold_idx, (train_idx, val_idx) in enumerate(
    skf.split(train_df, train_df["Survived"])
):
    cv_folds[fold_idx] = (
        train_df.iloc[train_idx].copy(),
        train_df.iloc[val_idx].copy(),
    )

print(
    f"Splits complete: Train ({len(train_df)}), "
    f"Dev ({len(dev_df)}), Test ({len(test_df)}), CV Folds ({len(cv_folds)})"
)

print("\nSurvival rates:")
print(pd.DataFrame({
    "train": [train_df["Survived"].mean()],
    "dev": [dev_df["Survived"].mean()],
    "test": [test_df["Survived"].mean()],
}).T.rename(columns={0: "survival_rate"}))
