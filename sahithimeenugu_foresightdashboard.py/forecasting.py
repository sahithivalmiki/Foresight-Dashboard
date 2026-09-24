import numpy as np
import pandas as pd

from statsmodels.tsa.holtwinters import (
    ExponentialSmoothing
)


def holt_winters_forecast(
    series,
    periods=12
):

    series = series.dropna()

    model = ExponentialSmoothing(

        series,

        trend="add",

        seasonal="add",

        seasonal_periods=12,

        initialization_method="estimated"

    )

    fitted_model = model.fit(
        optimized=True
    )

    forecast = fitted_model.forecast(
        periods
    )

    return forecast
def seasonal_naive_forecast(
    series,
    periods=12
):

    series = series.dropna()

    last_year = series.iloc[-12:]

    values = []

    for i in range(periods):

        values.append(
            last_year.iloc[
                i % 12
            ]
        )

    future_dates = pd.date_range(

        start=
        series.index[-1]
        + pd.DateOffset(months=1),

        periods=periods,

        freq="MS"
    )

    return pd.Series(

        values,

        index=future_dates
    )