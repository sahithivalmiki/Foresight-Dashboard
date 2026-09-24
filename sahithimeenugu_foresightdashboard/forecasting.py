import numpy as np
import pandas as pd

from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error


def holt_winters_forecast(series, periods=12):
    """
    Generate a Holt-Winters forecast.

    Parameters
    ----------
    series : pandas Series
        Historical time-series data.
    periods : int
        Number of future periods to forecast.

    Returns
    -------
    pandas Series
        Forecasted values.
    """

    series = series.dropna().astype(float)

    if len(series) < 24:
        raise ValueError(
            "At least 24 historical observations are required "
            "for Holt-Winters forecasting."
        )

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


def seasonal_naive_forecast(series, periods=12):
    """
    Forecast using the Seasonal Naive method.

    Each future value is based on the value
    from the same month in the previous year.
    """

    series = series.dropna().astype(float)

    if len(series) < 12:
        raise ValueError(
            "At least 12 historical observations are required "
            "for Seasonal Naive forecasting."
        )

    last_season = series.iloc[-12:].values

    forecast_values = np.tile(
        last_season,
        int(np.ceil(periods / 12))
    )[:periods]

    # Create monthly future dates
    if isinstance(series.index, pd.DatetimeIndex):
        future_index = pd.date_range(
            start=series.index[-1] + pd.offsets.MonthBegin(1),
            periods=periods,
            freq="MS"
        )
    else:
        future_index = range(periods)

    return pd.Series(
        forecast_values,
        index=future_index,
        name="forecast"
    )


def backtest_holt_winters(series, test_months=24):
    """
    Evaluate Holt-Winters using historical backtesting.

    The final `test_months` observations are held out
    as test data.
    """

    series = series.dropna().astype(float)

    if len(series) <= test_months:
        raise ValueError(
            "Not enough observations for backtesting."
        )

    train = series.iloc[:-test_months]
    test = series.iloc[-test_months:]

    predicted = holt_winters_forecast(
        train,
        periods=test_months
    )

    actual = test.values
    predicted_values = predicted.values

    mae = mean_absolute_error(
        actual,
        predicted_values
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predicted_values
        )
    )

    # Avoid division by zero for MAPE
    non_zero = actual != 0

    if non_zero.any():
        mape = np.mean(
            np.abs(
                (
                    actual[non_zero]
                    - predicted_values[non_zero]
                )
                / actual[non_zero]
            )
        ) * 100
    else:
        mape = np.nan

    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape
    }