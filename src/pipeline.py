# Load raw data
# ↓
# Upload raw data to GCS
# ↓
# Chronological splitting
# ↓
# Feature engineering
# ↓
# Save feature datasets

# Run the complete ETL process
from data_load_gcs import load_data
from data_quality import validate_data
from data_cleaning import clean_data
from feature_engineering import create_features
from data_storage_gcs import save_data

from src.config import (
    PROJECT_ID,
    BUCKET_NAME,
    LOCATION
)

from src.config import RAW_DIR

from src.gcs_utils import (
    create_gcs_bucket,
    upload_raw_data
)

from src.data_splitter import (
    create_chronological_splits
)

from src.feature_engineering import (
    create_datetime_features,
    create_lag_features,
    create_rolling_features
)


def run_data_pipeline(air_quality):

    create_gcs_bucket()

    upload_raw_data(
        RAW_DIR / "AirQualityUCI.csv"
    )

    (
        train_df,
        eval_df,
        test_df,
        cv_folds
    ) = create_chronological_splits(
        air_quality,
        upload_to_gcs=True
    )

    train_df = create_datetime_features(
        train_df
    )

    train_df = create_lag_features(
        train_df
    )

    train_df = create_rolling_features(
        train_df
    )

    return (
        train_df,
        eval_df,
        test_df,
        cv_folds
    )

raw_df = load_data_from_gcs()

cleaned_df = clean_data(raw_df)

validate_data(cleaned_df)


train_df, eval_df, test_df, cv_folds = (
    create_chronological_splits(cleaned_df)
)

save_splits_to_gcs(train_df, eval_df, test_df, cv_folds)

train_df, evaluation_df, test_df, cv_folds = (
    create_chronological_splits(
        cleaned_df,
        save_local=True,
        upload_to_gcs=True
    )
)

def run_pipeline():

    # 1. Load raw data
    df = load_data()

    # 2. Validate data
    validate_data(df)

    # 3. Clean data
    df = clean_data(df)

    # 4. Create features
    df = create_features(df)

    # 5. Save processed data
    save_data(df)

def get_storage_client():
    ...

def upload_file_to_gcs():
    ...

def create_gcs_bucket():
    ...

def create_chronological_splits():
    ...

if __name__ == "__main__":
    run_pipeline()