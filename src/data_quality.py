def check_missing_values(df):
    return df.isnull().sum()


def check_duplicates(df):
    return df.duplicated().sum()


def validate_timestamps(df):
    return df["Datetime"].is_monotonic_increasing