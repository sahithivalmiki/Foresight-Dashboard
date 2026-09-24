import pandas as pd
import numpy as np


def detect_anomalies(
    series,
    window=12
):

    data = pd.DataFrame({

        "date":
        series.index,

        "sales":
        series.values

    })

    data["rolling_mean"] = (
        data["sales"]
        .rolling(
            window,
            min_periods=6
        )
        .mean()
    )

    data["rolling_std"] = (
        data["sales"]
        .rolling(
            window,
            min_periods=6
        )
        .std()
    )

    data["z_score"] = (

        data["sales"]
        - data["rolling_mean"]

    ) / data["rolling_std"]

    data["anomaly"] = (
        data["z_score"].abs() >= 2
    )

    return data