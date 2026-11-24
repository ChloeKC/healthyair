def create_datetime_features(
    df
):

    df = df.copy()

    df["hour"] = (
        df["Datetime"]
        .dt.hour
    )

    df["day_of_week"] = (
        df["Datetime"]
        .dt.dayofweek
    )

    df["month"] = (
        df["Datetime"]
        .dt.month
    )

    return df


def create_lag_features(
    df
):

    df = df.copy()

    df["NO2_lag1"] = (
        df["NO2(GT)"]
        .shift(1)
    )

    df["NO2_lag3"] = (
        df["NO2(GT)"]
        .shift(3)
    )

    df["NO2_lag6"] = (
        df["NO2(GT)"]
        .shift(6)
    )

    return df


def create_rolling_features(
    df
):

    df = df.copy()

    df["NO2_roll3"] = (
        df["NO2(GT)"]
        .rolling(3)
        .mean()
    )

    df["NO2_roll6"] = (
        df["NO2(GT)"]
        .rolling(6)
        .mean()
    )

    return df