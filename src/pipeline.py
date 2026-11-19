# Run the complete ETL process
from data_load_gcs import load_data
from data_quality import validate_data
from data_cleaning import clean_data
from feature_engineering import create_features
from data_storage_gcs import save_data

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


if __name__ == "__main__":
    run_pipeline()