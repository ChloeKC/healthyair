import numpy as np
import pandas as pd

from sklearn.model_selection import (
    TimeSeriesSplit
)

from src.gcs_config import (
    PROCESSED_DIR,
    PROCESSED_GCS_PATH
)

from src.gcs_utilities import (
    upload_file_to_gcs
)


def create_chronological_splits(
    df,
    train_fraction=0.70,
    evaluation_fraction=0.15,
    n_splits=8,
    cv_gap=1,
    upload_to_gcs=False,
    bucket_name=None,
    project_id=None
):

    required_columns = {
        "Date",
        "Time",
        "NO2(GT)"
    }

    missing = (
        required_columns
        .difference(df.columns)
    )

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    df_split = df.copy()

    df_split["Datetime"] = pd.to_datetime(
        df_split["Date"]
        + " "
        + df_split["Time"],
        errors="coerce"
    )

    df_split["NO2(GT)"] = (
        pd.to_numeric(
            df_split["NO2(GT)"],
            errors="coerce"
        )
    )

    df_split["NO2(GT)"] = (
        df_split["NO2(GT)"]
        .replace(-200, np.nan)
    )

    df_split = (
        df_split
        .dropna(
            subset=["Datetime"]
        )
        .sort_values(
            "Datetime"
        )
        .reset_index(
            drop=True
        )
    )

    df_split["Target_Next_Hour"] = (
        df_split["NO2(GT)"]
        .shift(-1)
    )

    df_split["Target_Datetime"] = (
        df_split["Datetime"]
        .shift(-1)
    )

    valid_next_hour = (
        df_split["Target_Datetime"]
        ==
        df_split["Datetime"]
        + pd.Timedelta(hours=1)
    )

    df_split.loc[
        ~valid_next_hour,
        "Target_Next_Hour"
    ] = pd.NA

    df_split["Target_Next_Hour"] = (
        pd.cut(
            df_split["Target_Next_Hour"],
            bins=[
                -np.inf,
                100,
                200,
                np.inf
            ],
            labels=[
                "GOOD",
                "MODERATE",
                "POOR"
            ]
        )
    )

    df_split = (
        df_split
        .dropna(
            subset=[
                "Target_Next_Hour"
            ]
        )
        .reset_index(
            drop=True
        )
    )

    n = len(df_split)

    if n == 0:
        raise ValueError(
            "No usable rows."
        )

    train_end = int(
        n * train_fraction
    )

    eval_end = int(
        n *
        (
            train_fraction
            +
            evaluation_fraction
        )
    )

    train_boundary = (
        df_split.loc[
            train_end - 1,
            "Datetime"
        ]
    )

    eval_boundary = (
        df_split.loc[
            eval_end - 1,
            "Datetime"
        ]
    )

    train_df = df_split[
        (
            df_split["Datetime"]
            <= train_boundary
        )
    ].copy()

    eval_df = df_split[
        (
            df_split["Datetime"]
            > train_boundary
        )
        &
        (
            df_split["Datetime"]
            <= eval_boundary
        )
    ].copy()

    test_df = df_split[
        (
            df_split["Datetime"]
            > eval_boundary
        )
    ].copy()

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    train_df.to_parquet(
        PROCESSED_DIR /
        "train.parquet",
        index=False
    )

    eval_df.to_parquet(
        PROCESSED_DIR /
        "evaluation.parquet",
        index=False
    )

    test_df.to_parquet(
        PROCESSED_DIR /
        "test.parquet",
        index=False
    )

    tscv = TimeSeriesSplit(
        n_splits=n_splits,
        gap=cv_gap
    )

    cv_folds = {}

    for fold,
    (train_idx, val_idx) in enumerate(
        tscv.split(train_df),
        start=1
    ):

        cv_folds[fold] = (
            train_df.iloc[
                train_idx
            ].copy(),
            train_df.iloc[
                val_idx
            ].copy()
        )

    return (
        train_df,
        eval_df,
        test_df,
        cv_folds
    )