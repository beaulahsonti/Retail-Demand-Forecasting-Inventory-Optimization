import numpy as np
import pandas as pd


def recursive_forecast(
    model,
    history_df,
    validation_df,
    feature_columns,
    target_col="sales",
    date_col="date",
    group_cols=("id",),
):
    """
    Generate recursive forecasts without using actual
    validation-period sales as lag features.

    Assumes:
    - history_df contains training-period actual sales.
    - validation_df contains future dates and known features.
    - Feature engineering uses lag_7, lag_28 and rolling_mean_7.
    - The model was trained using the same feature definitions.
    """

    history = history_df.copy()
    future = validation_df.copy()

    history[date_col] = pd.to_datetime(history[date_col])
    future[date_col] = pd.to_datetime(future[date_col])

    history = history.sort_values(
        list(group_cols) + [date_col]
    )

    future = future.sort_values(
        [date_col] + list(group_cols)
    )

    history_lookup = {
        tuple(row[col] for col in group_cols): (
            group.set_index(date_col)[target_col].to_dict()
        )
        for _, group in history.groupby(
            list(group_cols), sort=False
        )
        for row in [group.iloc[0]]
    }

    predictions = []

    for date, day_data in future.groupby(date_col, sort=True):
        day_data = day_data.copy()

        for idx, row in day_data.iterrows():
            key = tuple(row[col] for col in group_cols)
            sales_history = history_lookup.setdefault(key, {})

            day_data.loc[idx, "lag_7"] = sales_history.get(
                date - pd.Timedelta(days=7), np.nan
            )

            day_data.loc[idx, "lag_28"] = sales_history.get(
                date - pd.Timedelta(days=28), np.nan
            )

            previous_sales = [
                sales_history.get(
                    date - pd.Timedelta(days=i), np.nan
                )
                for i in range(1, 8)
            ]

            day_data.loc[idx, "rolling_mean_7"] = (
                np.nanmean(previous_sales)
                if not np.all(np.isnan(previous_sales))
                else np.nan
            )

        day_predictions = model.predict(
            day_data[feature_columns]
        )

        day_predictions = np.maximum(day_predictions, 0)

        for (_, row), prediction in zip(
            day_data.iterrows(), day_predictions
        ):
            key = tuple(row[col] for col in group_cols)

            history_lookup[key][date] = float(prediction)

            predictions.append({
                **{col: row[col] for col in group_cols},
                date_col: date,
                "predicted_sales": float(prediction),
            })

    return pd.DataFrame(predictions)
