def calculate_growth(
    current,
    previous
):

    return (
        (current - previous)
        / previous
    ) * 100


def get_forecast_direction(
    forecast
):

    first = forecast.iloc[0]

    last = forecast.iloc[-1]

    change = (
        (last - first)
        / first
    ) * 100

    if change > 2:

        return "Increasing", change

    elif change < -2:

        return "Decreasing", change

    else:

        return "Stable", change


def sector_growth(
    df,
    column
):

    latest = df[column].iloc[-1]

    previous = df[column].iloc[-13]

    return calculate_growth(
        latest,
        previous
    )