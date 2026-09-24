import streamlit as st
import pandas as pd
import plotly.express as px

from sahithimeenugu_foresightdashboard.data_loader import load_retail_data


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Foresight | Retail Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero {
        padding: 25px;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #111827,
            #1f2937
        );
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 17px;
        color: #d1d5db;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def get_data():

    df = load_retail_data()

    # Convert period name into actual date
    df["date"] = pd.to_datetime(
        df["per_name"],
        format="%b-%Y",
        errors="coerce"
    )

    # Convert sales to million dollars
    df["sales_million"] = pd.to_numeric(
        df["val"],
        errors="coerce"
    )

    # Remove invalid dates
    df = df.dropna(
        subset=["date"]
    )

    # Sort data
    df = df.sort_values(
        ["cat_code", "date"]
    )

    return df


df = get_data()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <h1>📈 FORESIGHT</h1>

        <p>
        Retail Intelligence & Forecasting Dashboard
        </p>

        <p>
        Understand historical retail sales, identify trends,
        compare categories and prepare for future demand.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎛️ Dashboard Controls")

st.sidebar.markdown(
    "Use the controls below to explore the retail market."
)

# Category selection
categories = sorted(
    df["cat_desc"].dropna().unique()
)

selected_category = st.sidebar.selectbox(
    "Select Retail Category",
    categories
)


# Date range
min_date = df["date"].min().date()
max_date = df["date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# ============================================================
# FILTER DATA
# ============================================================

category_df = df[
    df["cat_desc"] == selected_category
].copy()


if len(selected_dates) == 2:

    start_date = pd.Timestamp(
        selected_dates[0]
    )

    end_date = pd.Timestamp(
        selected_dates[1]
    )

    category_df = category_df[
        (category_df["date"] >= start_date)
        &
        (category_df["date"] <= end_date)
    ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

if not category_df.empty:

    latest_sales = category_df.iloc[-1]["sales_million"]

    average_sales = category_df[
        "sales_million"
    ].mean()

    highest_sales = category_df[
        "sales_million"
    ].max()

    lowest_sales = category_df[
        "sales_million"
    ].min()

else:

    latest_sales = 0
    average_sales = 0
    highest_sales = 0
    lowest_sales = 0


# ============================================================
# KPI CARDS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Market Snapshot</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Latest Sales",
        f"${latest_sales:,.0f}M"
    )


with col2:

    st.metric(
        "Average Sales",
        f"${average_sales:,.0f}M"
    )


with col3:

    st.metric(
        "Highest Sales",
        f"${highest_sales:,.0f}M"
    )


with col4:

    st.metric(
        "Lowest Sales",
        f"${lowest_sales:,.0f}M"
    )


# ============================================================
# SALES TREND
# ============================================================

st.markdown(
    '<div class="section-title">📈 Historical Sales Trend</div>',
    unsafe_allow_html=True
)


fig = px.line(
    category_df,
    x="date",
    y="sales_million",
    title=f"Monthly Sales — {selected_category}",
    markers=False
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales ($ Million)",
    hovermode="x unified",
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# YEARLY SALES
# ============================================================

st.markdown(
    '<div class="section-title">📅 Yearly Performance</div>',
    unsafe_allow_html=True
)

if not category_df.empty:

    category_df["year"] = category_df[
        "date"
    ].dt.year

    yearly_sales = (
        category_df
        .groupby("year")["sales_million"]
        .sum()
        .reset_index()
    )

    fig_year = px.bar(
        yearly_sales,
        x="year",
        y="sales_million",
        title="Annual Sales"
    )

    fig_year.update_layout(
        xaxis_title="Year",
        yaxis_title="Total Sales ($ Million)",
        height=400
    )

    st.plotly_chart(
        fig_year,
        use_container_width=True
    )


# ============================================================
# MONTHLY SEASONALITY
# ============================================================

st.markdown(
    '<div class="section-title">🗓️ Monthly Seasonality</div>',
    unsafe_allow_html=True
)

if not category_df.empty:

    category_df["month"] = category_df[
        "date"
    ].dt.month

    category_df["month_name"] = category_df[
        "date"
    ].dt.strftime("%b")

    monthly_pattern = (
        category_df
        .groupby(
            ["month", "month_name"]
        )["sales_million"]
        .mean()
        .reset_index()
        .sort_values("month")
    )

    fig_season = px.line(
        monthly_pattern,
        x="month_name",
        y="sales_million",
        markers=True,
        title="Average Sales by Month"
    )

    fig_season.update_layout(
        xaxis_title="Month",
        yaxis_title="Average Sales ($ Million)",
        height=400
    )

    st.plotly_chart(
        fig_season,
        use_container_width=True
    )


# ============================================================
# CATEGORY COMPARISON
# ============================================================

st.markdown(
    '<div class="section-title">🏪 Retail Category Comparison</div>',
    unsafe_allow_html=True
)

category_summary = (
    df.groupby("cat_desc")["sales_million"]
    .mean()
    .reset_index()
    .sort_values(
        "sales_million",
        ascending=False
    )
)

fig_category = px.bar(
    category_summary,
    x="sales_million",
    y="cat_desc",
    orientation="h",
    title="Average Monthly Sales by Category"
)

fig_category.update_layout(
    xaxis_title="Average Sales ($ Million)",
    yaxis_title="Retail Category",
    height=650
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)


# ============================================================
# RECENT DATA
# ============================================================

st.markdown(
    '<div class="section-title">🔎 Recent Observations</div>',
    unsafe_allow_html=True
)

recent_data = (
    category_df[
        [
            "date",
            "cat_desc",
            "sales_million"
        ]
    ]
    .sort_values(
        "date",
        ascending=False
    )
    .head(12)
)

recent_data = recent_data.rename(
    columns={
        "date": "Date",
        "cat_desc": "Category",
        "sales_million": "Sales ($M)"
    }
)

st.dataframe(
    recent_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br>
    <hr>

    <center>

    <b>FORESIGHT</b> — Retail Intelligence Dashboard

    <br>

    Built with Python • Pandas • Plotly • Streamlit

    </center>
    """,
    unsafe_allow_html=True
)