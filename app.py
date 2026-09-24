import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from src.forecasting import (
    holt_winters_forecast,
    seasonal_naive_forecast,
    backtest_holt_winters
)

from src.anomaly import (
    detect_anomalies
)

from src.insights import (
    get_forecast_direction,
    sector_growth
)
st.set_page_config(

    page_title="FORESIGHT",

    page_icon="🔭",

    layout="wide",

    initial_sidebar_state="expanded"
)
st.markdown(
    """
    <style>

    .main-title {

        font-size: 42px;

        font-weight: 800;

        margin-bottom: 0px;

    }

    .subtitle {

        font-size: 18px;

        color: #6b7280;

        margin-bottom: 30px;

    }

    .section {

        font-size: 24px;

        font-weight: 700;

        margin-top: 30px;

        margin-bottom: 15px;

    }

    </style>
    """,

    unsafe_allow_html=True
)
st.markdown(
    '<div class="main-title">🔭 FORESIGHT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Multi-Sector Retail Forecasting & Intelligence Platform'
    '</div>',
    unsafe_allow_html=True
)
st.sidebar.title("FORESIGHT")

st.sidebar.markdown(
    "### Control Center"
)

forecast_period = st.sidebar.slider(

    "Forecast horizon",

    min_value=3,

    max_value=24,

    value=12
)

model_name = st.sidebar.selectbox(

    "Forecast model",

    [
        "Holt-Winters",
        "Seasonal Naive"
    ]
)

scenario = st.sidebar.slider(

    "Scenario adjustment",

    -15,

    15,

    0
)
sector_names = {

    "total_retail":
        "Total Retail",

    "motor_vehicle":
        "Motor Vehicle",

    "furniture":
        "Furniture",

    "electronics":
        "Electronics",

    "building_material":
        "Building Materials",

    "food_beverage":
        "Food & Beverage",

    "grocery":
        "Grocery",

    "health_personal":
        "Health & Personal Care",

    "gasoline":
        "Gasoline",

    "clothing":
        "Clothing",

    "sporting_goods":
        "Sporting Goods",

    "general_merchandise":
        "General Merchandise",

    "miscellaneous":
        "Miscellaneous",

    "nonstore":
        "Nonstore Retail",

    "food_services":
        "Food Services"
}
selected_sector = st.sidebar.selectbox(

    "Select retail sector",

    list(sector_names.keys()),

    format_func=lambda x:
        sector_names[x]
)
df = pd.read_csv(
    "data/foresight_retail.csv"
)

df["date"] = pd.to_datetime(
    df["date"]
)

df = df.sort_values(
    "date"
)
series = (

    df
    .set_index("date")
    [selected_sector]
    .dropna()
)
if model_name == "Holt-Winters":

    forecast = holt_winters_forecast(

        series,

        forecast_period
    )

else:

    forecast = seasonal_naive_forecast(

        series,

        forecast_period
    )
    forecast = (

    forecast

    * (1 + scenario / 100)

)
    latest = series.iloc[-1]

previous = series.iloc[-2]

mom_growth = (

    (latest - previous)

    / previous

) * 100

forecast_average = forecast.mean()

forecast_change = (

    (forecast.iloc[-1]
     - forecast.iloc[0])

    / forecast.iloc[0]

) * 100
col1, col2, col3, col4 = st.columns(4)

col1.metric(

    "Latest Sales",

    f"${latest:,.0f}M"

)

col2.metric(

    "MoM Growth",

    f"{mom_growth:+.2f}%"

)

col3.metric(

    "Next Forecast",

    f"${forecast.iloc[0]:,.0f}M"

)

col4.metric(

    "Forecast Direction",

    f"{forecast_change:+.2f}%"

)
st.markdown(
    '<div class="section">📈 Forecast Outlook</div>',
    unsafe_allow_html=True
)

fig = go.Figure()

fig.add_trace(

    go.Scatter(

        x=series.index,

        y=series.values,

        mode="lines",

        name="Historical"

    )

)

fig.add_trace(

    go.Scatter(

        x=forecast.index,

        y=forecast.values,

        mode="lines+markers",

        name="Forecast",

        line=dict(

            dash="dash",

            width=3

        )

    )

)

fig.update_layout(

    height=500,

    hovermode="x unified",

    xaxis_title="Date",

    yaxis_title="Sales ($ Millions)",

    legend=dict(

        orientation="h",

        y=1.02,

        x=0

    )

)

st.plotly_chart(

    fig,

    use_container_width=True

)
st.markdown(
    '<div class="section">🏪 Sector Intelligence</div>',
    unsafe_allow_html=True
)

sector_values = []

for column, name in sector_names.items():

    if column in df.columns:

        latest_value = df[column].iloc[-1]

        sector_values.append({

            "Sector": name,

            "Sales": latest_value

        })

sector_df = pd.DataFrame(
    sector_values
)

sector_df = sector_df.sort_values(
    "Sales",
    ascending=False
)
sector_fig = px.bar(

    sector_df,

    x="Sales",

    y="Sector",

    orientation="h",

    title="Latest Retail Sales by Sector"
)

sector_fig.update_layout(
    height=600
)

st.plotly_chart(
    sector_fig,
    use_container_width=True
)
growth_rows = []

for column, name in sector_names.items():

    if column not in df.columns:

        continue

    if len(df) < 13:

        continue

    latest = df[column].iloc[-1]

    year_ago = df[column].iloc[-13]

    growth = (
        (latest - year_ago)
        / year_ago
    ) * 100

    growth_rows.append({

        "Sector": name,

        "Latest Sales":
            latest,

        "YoY Growth (%)":
            growth

    })

growth_df = pd.DataFrame(
    growth_rows
)
st.dataframe(

    growth_df.style.format({

        "Latest Sales":
            "${:,.0f}M",

        "YoY Growth (%)":
            "{:+.2f}%"

    }),

    use_container_width=True,

    hide_index=True

)
st.markdown(
    '<div class="section">🗓️ Seasonality</div>',
    unsafe_allow_html=True
)

seasonal = (

    df
    .assign(
        month=df["date"].dt.month
    )
    .groupby("month")[selected_sector]
    .mean()
)

month_names = [

    "Jan", "Feb", "Mar",
    "Apr", "May", "Jun",
    "Jul", "Aug", "Sep",
    "Oct", "Nov", "Dec"

]

season_fig = go.Figure()

season_fig.add_trace(

    go.Bar(

        x=month_names,

        y=seasonal.values,

        name="Average Sales"

    )
)

season_fig.update_layout(

    height=400,

    xaxis_title="Month",

    yaxis_title="Average Sales ($ Millions)"

)

st.plotly_chart(

    season_fig,

    use_container_width=True

)
st.markdown(
    '<div class="section">🚨 Anomaly Monitor</div>',
    unsafe_allow_html=True
)

anomaly_df = detect_anomalies(
    series
)

anomalies = anomaly_df[
    anomaly_df["anomaly"] == True
]

st.dataframe(

    anomalies[
        [
            "date",
            "sales",
            "z_score"
        ]
    ]
    .sort_values(
        "date",
        ascending=False
    )
    .head(15),

    use_container_width=True,

    hide_index=True

)
direction, change = (
    get_forecast_direction(
        forecast
    )
)

st.markdown(
    '<div class="section">💡 FORESIGHT Signal</div>',
    unsafe_allow_html=True
)

if direction == "Increasing":

    st.success(

        f"""
        **{sector_names[selected_sector]}**
        has an estimated upward forecast trajectory
        of **{change:+.2f}%** over the selected forecast horizon.
        """

    )

elif direction == "Decreasing":

    st.warning(

        f"""
        **{sector_names[selected_sector]}**
        has an estimated downward forecast trajectory
        of **{change:+.2f}%** over the selected forecast horizon.
        """

    )

else:

    st.info(

        f"""
        **{sector_names[selected_sector]}**
        has a relatively stable forecast trajectory.
        """

    )
    st.markdown(
    '<div class="section">🧪 Model Lab</div>',
    unsafe_allow_html=True
)

if len(series) >= 48:

    metrics = backtest_holt_winters(
        series,
        test_months=24
    )

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "MAE",
        f"{metrics['MAE']:,.2f}"
    )

    m2.metric(
        "RMSE",
        f"{metrics['RMSE']:,.2f}"
    )

    m3.metric(
        "MAPE",
        f"{metrics['MAPE']:.2f}%"
    )

else:

    st.info(
        "Not enough historical observations "
        "for reliable backtesting."
    )