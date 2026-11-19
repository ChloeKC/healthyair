def create_datetime_column(df):

    df = df.copy()

    df["Datetime"] = pd.to_datetime(
        df["Date"] + " " + df["Time"],
        format="%m/%d/%Y %H:%M:%S",
        errors="coerce"
    )

    df = df.sort_values("Datetime").reset_index(drop=True)

    return df