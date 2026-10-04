# HealthyAir - Google Cloud Storage configuration

#    1. Create/check the Google Cloud Storage bucket.
#    2. Upload the unchanged raw UCI Air Quality CSV.
#    3. Create chronological train/dev/test splits.
#    4. Upload the processed splits to GCS.

from pathlib import Path
import pandas as pd
from google.cloud import storage

print("Google Cloud Storage imported successfully")

PROJECT_ID = "healthy-air-analysis"
BUCKET_NAME = "healthy-air-analysis-data"
LOCATION = "EU"

print(f"Project: {PROJECT_ID}")
print(f"Bucket: gs://{BUCKET_NAME}")


# Healthy Air Project folders 
# ---------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "AirQualityUCI.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# GCS paths
# ---------------------------------------------------------------------
RAW_GCS_PATH = "raw/uci-air-quality/v1/AirQualityUCI.csv"
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

def upload_to_gcs(healthy-air-analysis-data, source_file_name, destination_blob_name):
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