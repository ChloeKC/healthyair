# HealthyAir - Google Cloud Storage configuration

# This notebook demonstrates an end-to-end data engineering workflow using the UCI Air Quality dataset and Google Cloud Platform (GCP).

#   1. Installs the required Python libraries.
#   2. Configures GCP authentication and project settings.
#   3. Creates a Google Cloud Storage (GCS) bucket if none exists.
#   4. Downloads the raw UCI Air Quality CSV and stores it in GCS.
#   5. Creates chronological stratified train/dev/test datasets and 8-fold cross-validation splits.
#   6. Stores the resulting shards back in GCS.
#   7. Loads the raw data into BigQuery, with an optional PostgreSQL/Cloud SQL path.
#   8. Verifies the bucket contents and reads a shard directly from GCS with Pandas.

from pathlib import Path
import pandas as pd
from google.cloud import storage
import numpy as np
from sklearn.model_selection import TimeSeriesSplit

print("Google Cloud Storage imported successfully")

# Healthy Air Project GCS Configuration
# ---------------------------------------------------------------------

PROJECT_ID = "healthy-air-analysis"
BUCKET_NAME = "uci_air_quality"
LOCATION = "EU"

print(f"Project: {PROJECT_ID}")
print(f"Bucket: gs://{BUCKET_NAME}")

# GCS paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_ROOT / "data_raw" / "AirQualityUCI.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

RAW_GCS_PATH = "/uci-air-quality/v1/AirQualityUCI.csv"
PROCESSED_GCS_PATH = "processed/v1/"

print("Raw data path:", RAW_GCS_PATH)
print("Processed data prefix:", PROCESSED_GCS_PATH)

LOCAL_FILE = "../data/raw/AirQualityUCI.csv"
GCS_FILE = "raw/uci-air-quality/v1/AirQualityUCI.csv"

df = pd.read_csv(LOCAL_RAW_PATH)

print("Dataset shape:", df.shape)
display(df.head())

# Google Cloud Storage functions
# ---------------------------------------------------------------------

def _get_storage_client(project_id: str = PROJECT_ID):
    """Create an authenticated Google Cloud Storage client."""
    try:
        from google.cloud import storage
    except ImportError as exc:
        raise ImportError(
            "Install Google Cloud Storage support with: "
            "pip install google-cloud-storage"
        ) from exc

    return storage.Client(project=project_id)

# GCS - Bucket
# ---------------------------------------------------------------------

def create_gcs_bucket(
    bucket_name: str = BUCKET_NAME,
    project_id: str = PROJECT_ID,
    location: str = LOCATION,
):
    """Create the bucket if it does not already exist; return the bucket."""
    client = _get_storage_client(project_id)
    bucket = client.lookup_bucket(bucket_name)

    if bucket is not None:
        print(f"Bucket already exists: gs://{bucket_name}")
        return bucket

    bucket = client.bucket(bucket_name)
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket = client.create_bucket(bucket, location=location)

    print(f"Created bucket: gs://{bucket_name}")
    return bucket

def upload_file_to_gcs(
    local_path: Path,
    destination_blob_name: str,
    bucket_name: str = BUCKET_NAME,
    project_id: str = PROJECT_ID,
) -> None:
    """Upload one local file to the specified GCS object path."""
    local_path = Path(local_path)

    if not local_path.is_file():
        raise FileNotFoundError(f"File not found: {local_path}")

    client = _get_storage_client(project_id)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(str(local_path))

    print(
        f"Uploaded {local_path} -> "
        f"gs://{bucket_name}/{destination_blob_name}"
    )


def upload_raw_data(
    local_path: Path = RAW_FILE,
    bucket_name: str = BUCKET_NAME,
    project_id: str = PROJECT_ID,
) -> None:
    """Upload the unchanged raw CSV to its configured GCS location."""
    upload_file_to_gcs(
        local_path=local_path,
        destination_blob_name=RAW_GCS_PATH,
        bucket_name=bucket_name,
        project_id=project_id,
    )

# Chronological Train / Evaluation / Test Splits + Cross-validation
# ---------------------------------------------------------------------
# Create chronological 70/15/15 train, evaluation and test splits.
# Generate 8 expanding-window CV folds from training data only(data leakage).
# The splits are stored in the `data/processed` folder and uploaded to GCS.

def create_chronological_splits(
    df: pd.DataFrame,
    train_fraction: float = 0.70,
    evaluation_fraction: float = 0.15,
    n_splits: int = 8,
    cv_gap: int = 1,
    save_local: bool = True,
    upload_to_gcs: bool = False,
    bucket_name: str = BUCKET_NAME,
    project_id: str = PROJECT_ID,
):
    required_columns = {"Datetime", "NO2(GT)"}
    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1.")

    if not 0 < evaluation_fraction < 1:
        raise ValueError("evaluation_fraction must be between 0 and 1.")

    if train_fraction + evaluation_fraction >= 1:
        raise ValueError(
            "train_fraction + evaluation_fraction must be less than 1."
        )

    if n_splits < 2:
        raise ValueError("n_splits must be at least 2.")

    if cv_gap < 0:
        raise ValueError("cv_gap cannot be negative.")

    df_split = df.copy()
    df_split["Datetime"] = pd.to_datetime(data["Datetime"], errors="coerce")
    df_split["NO2(GT)"] = pd.to_numeric(data["NO2(GT)"], errors="coerce")

    # The UCI dataset uses -200 as a missing-value marker.
    df_split["NO2(GT)"] = df_split["NO2(GT)"].replace(-200, np.nan)

    # Drop NANs and nsure chronological order
    df_split = (
        df_split.dropna(subset=["Datetime"])
        .sort_values("Datetime").reset_index(drop=True)

    if df_split["Datetime"].duplicated().any():
        raise ValueError(
            "Duplicate timestamps found. Resolve them during data cleaning "
            "before creating chronological splits."
        )
    
    # Create next-hour target and its corresponding timestamp
    df_split["Target_Next_Hour"] = df_split["NO2(GT)"].shift(-1)
    df_split["Target_Datetime"] = df_split["Datetime"].shift(-1)

    # Only retain consecutive hourly observations
    valid_next_hour = (
        df_split["Target_Datetime"] ==
        df_split["Datetime"] + pd.Timedelta(hours=1)
    )

    df_split.loc[~valid_next_hour, "Target_Next_Hour"] = pd.NA

    # Apply project-defined NO2 categories
    df_split["Target_Next_Hour"] = pd.cut(
        df_split["Target_Next_Hour"],
        bins=[-np.inf, 100, 200, np.inf],
        labels=["GOOD", "MODERATE", "POOR"]
    )

    # Remove rows without a valid next-hour target
    df_split = df_split.dropna(subset=["Target_Next_Hour"]).reset_index(drop=True)

    # Determine chronological boundaries
    n = len(df_split)
    train_end = int(n * 0.70)
    eval_end = int(n * 0.85)

    train_boundary = df_split.loc[train_end - 1, "Datetime"]
    eval_boundary = df_split.loc[eval_end - 1, "Datetime"]

    # Training: target must remain within training period
    train_df = df_split[
        (df_split["Datetime"] <= train_boundary) &
        (df_split["Target_Datetime"] <= train_boundary)
    ].copy()

    # Evaluation: features and target must remain in evaluation period
    eval_df = df_split[
        (df_split["Datetime"] > train_boundary) &
        (df_split["Datetime"] <= eval_boundary) &
        (df_split["Target_Datetime"] <= eval_boundary)
    ].copy()

    # Testing: features and target must remain in testing period
    test_df = df_split[
        (df_split["Datetime"] > eval_boundary)
    ].copy()

    # Generate 8 expanding-window CV folds from training data only
    tscv = TimeSeriesSplit(n_splits=8, gap=1)

    cv_folds = {}

    for fold_idx, (train_idx, val_idx) in enumerate(
        tscv.split(train_df), start=1
    ):
        cv_folds[fold_idx] = (
            train_df.iloc[train_idx].copy(),
            train_df.iloc[val_idx].copy()
        )

    # Save processed splits locally
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(PROCESSED_DIR / "train.csv", index=False)
    eval_df.to_csv(PROCESSED_DIR / "evaluation.csv", index=False)
    test_df.to_csv(PROCESSED_DIR / "test.csv", index=False)

    # Save individual CV fold datasets
    cv_dir = PROCESSED_DIR / "cross_validation"
    cv_dir.mkdir(parents=True, exist_ok=True)

    for fold, (fold_train, fold_val) in cv_folds.items():
        fold_train.to_csv(
            cv_dir / f"fold_{fold:02d}_train.csv", index=False
        )
        fold_val.to_csv(
            cv_dir / f"fold_{fold:02d}_validation.csv", index=False
        )

    # Summarise split sizes and category distributions
    split_summary = pd.DataFrame({
        "observations": [
            len(train_df), len(eval_df), len(test_df)
        ],
        "start_date": [
            train_df["Datetime"].min(),
            eval_df["Datetime"].min(),
            test_df["Datetime"].min()
        ],
        "end_date": [
            train_df["Datetime"].max(),
            eval_df["Datetime"].max(),
            test_df["Datetime"].max()
        ]
    }, index=["Training", "Evaluation", "Testing"])

    print("Chronological splits completed:")
    display(split_summary)

    print("\nTarget category distributions:")
    for name, split in [
        ("Training", train_df),
        ("Evaluation", eval_df),
        ("Testing", test_df)
    ]:
        print(f"\n{name}:")
        print(
            split["Target_Next_Hour"]
            .value_counts(normalize=True)
            .mul(100)
            .round(2)
        )

    print(f"\nGenerated {len(cv_folds)} cross-validation folds.")

    return train_df, eval_df, test_df, cv_folds
