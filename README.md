# 🔮 Foresight — Retail Sales Forecasting Dashboard

Foresight is an interactive **retail sales forecasting and analytics dashboard** built with Python and Streamlit.

The project transforms historical retail sales data into meaningful business insights and future sales forecasts. It combines **data cleaning, exploratory data analysis, time-series forecasting, model evaluation, and interactive visualization** in one dashboard.

The goal of Foresight is to help businesses understand historical sales patterns and use them to plan future inventory, sales targets, and business operations.

---

## 📊 Project Overview

Retail businesses generate large amounts of sales data every day. However, historical data becomes much more useful when it can answer questions such as:

* How are sales changing over time?
* Which months have the highest and lowest sales?
* Are there seasonal patterns?
* What are the recent sales trends?
* What could sales look like over the next 12 months?
* How accurate is the forecasting model?
* How does the forecasting model compare with a simple baseline?

**Foresight** addresses these questions through an easy-to-understand interactive dashboard.

### Project Workflow

```text
Raw Retail Data
       ↓
Data Cleaning
       ↓
Data Validation
       ↓
Exploratory Data Analysis
       ↓
Monthly Sales Aggregation
       ↓
Time-Series Analysis
       ↓
Forecasting Models
       ↓
Model Evaluation
       ↓
Future Sales Forecast
       ↓
Interactive Streamlit Dashboard
```

---

## 🎯 Objectives

The main objectives of Foresight are:

1. Analyze historical retail sales data.
2. Identify sales trends and seasonal patterns.
3. Create meaningful business KPIs.
4. Aggregate sales data into a monthly time series.
5. Forecast future sales using time-series techniques.
6. Compare forecasting performance against a baseline model.
7. Present results through an interactive dashboard.
8. Make the analysis understandable for both technical and non-technical users.

---

## ✨ Key Features

### 📈 Sales Trend Analysis

Visualize historical sales performance over time and identify:

* Growth and decline periods
* Monthly fluctuations
* Long-term trends
* Seasonal behavior

### 📊 Business KPIs

The dashboard provides important metrics such as:

* Total Sales
* Average Monthly Sales
* Highest Sales Month
* Lowest Sales Month
* Forecasted Sales
* Sales Growth

### 🔮 Sales Forecasting

Foresight uses time-series forecasting to estimate future sales.

The main forecasting approach is:

**Holt-Winters Exponential Smoothing**

The model considers:

* Level
* Trend
* Seasonality

A **Seasonal Naive** model is also used as a baseline for comparison.

### 🧪 Model Evaluation

Forecasting performance is evaluated using:

* MAE — Mean Absolute Error
* RMSE — Root Mean Squared Error
* MAPE — Mean Absolute Percentage Error

This helps understand how closely the forecasts match historical observations during backtesting.

### 📅 Future Forecast

The dashboard can display future monthly sales predictions, making it easier to understand expected demand patterns.

### 🎛️ Interactive Dashboard

Users can interact with the dashboard to explore:

* Historical sales
* Forecast periods
* KPIs
* Trends
* Forecast results
* Model performance

---

## 🧠 Forecasting Models

### 1. Holt-Winters Exponential Smoothing

Holt-Winters is a time-series forecasting method that can model both trend and seasonal patterns.

For monthly retail data, the project uses a seasonal period of:

```text
12 months
```

This allows the model to capture yearly seasonal behavior.

### 2. Seasonal Naive

The Seasonal Naive model provides a simple baseline.

It assumes that the value for a future month will be similar to the value from the corresponding month in the previous year.

For example:

```text
January 2026 → January 2027
February 2026 → February 2027
March 2026 → March 2027
```

Comparing the models helps provide context for the forecasting results.

---

## 📏 Evaluation Metrics

### MAE

Mean Absolute Error measures the average absolute difference between actual and predicted values.

```text
MAE = Average(|Actual - Predicted|)
```

Lower values indicate smaller average errors.

### RMSE

Root Mean Squared Error gives more weight to larger errors.

```text
RMSE = √Average((Actual - Predicted)²)
```

### MAPE

Mean Absolute Percentage Error expresses forecasting error as a percentage.

```text
MAPE = Average(|Actual - Predicted| / |Actual|) × 100
```

Zero-valued actual observations are excluded from the MAPE calculation to avoid division-by-zero problems.

---

## 🗂️ Dataset

The project uses a retail sales dataset stored locally in:

```text
data/MARTS-mf.csv
```

The dataset is processed before analysis to prepare it for time-series forecasting.

The data pipeline is designed to:

* Load the raw dataset
* Validate the data
* Handle missing values
* Convert date fields
* Prepare numerical fields
* Aggregate sales by month
* Create a forecasting-ready time series

> **Note:** The dataset should be included in the repository only if its licensing and redistribution terms allow it. Otherwise, provide instructions for obtaining the dataset separately.

---

## 🛠️ Technologies Used

### Programming Language

* Python

### Data Analysis

* Pandas
* NumPy

### Visualization

* Plotly

### Machine Learning / Forecasting

* Statsmodels
* Scikit-learn

### Dashboard
[open streamlit Dasboard](https://foresight-dashboard-hcgwv9mjjeutbddiy8egpb.streamlit.app/)
* Streamlit

### File Processing

* OpenPyXL

### Development Tools

* VS Code
* Git
* GitHub

---

## 📁 Project Structure

```text
Foresight project/
│
├── app.py
│
├── data/
│   └── MARTS-mf.csv
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   └── forecasting.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

### File Description

| File               | Purpose                           |
| ------------------ | --------------------------------- |
| `app.py`           | Main Streamlit dashboard          |
| `data_loader.py`   | Loads and inspects datasets       |
| `forecasting.py`   | Forecasting models and evaluation |
| `MARTS-mf.csv`     | Retail sales dataset              |
| `requirements.txt` | Python dependencies               |
| `README.md`        | Project documentation             |
| `.gitignore`       | Files excluded from Git           |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/foresight-dashboard.git
```

Move into the project directory:

```bash
cd foresight-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Git Bash

```bash
source venv/Scripts/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Dashboard Locally

Run:

```bash
streamlit run app.py
```

or:

```bash
python -m streamlit run app.py
```

Streamlit will provide a local address such as:

```text
http://localhost:8501
```

Open the address in your browser.

---

## 🌐 Deployment

The application can be deployed using **Streamlit Community Cloud**.

### Deployment Steps

1. Push the project to GitHub.
2. Make sure `app.py` is in the repository root.
3. Make sure `requirements.txt` is included.
4. Make sure the dataset is available according to its licensing terms.
5. Open Streamlit Community Cloud.
6. Connect your GitHub account.
7. Select the Foresight repository.
8. Select the `main` branch.
9. Set the main file to:

```text
app.py
```

10. Deploy the application.

---

## 🔐 Data Path

The application should use a relative project path rather than a computer-specific Windows path.

Example:

```python
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "MARTS-mf.csv"

df = pd.read_csv(DATA_PATH)
```

This allows the application to work both locally and on a deployment server.

---

## 📌 Example Business Questions

Foresight can be used to explore questions such as:

```text
What is the overall sales trend?

Which months generate the highest sales?

Is there a yearly seasonal pattern?

What are the expected sales for upcoming months?

How does the forecasting model perform?

How different are the forecasts from a simple seasonal baseline?
```

---

## 🚀 Future Improvements

Potential future enhancements include:

* Product-level forecasting
* Store-level forecasting
* Region-level forecasting
* Interactive product filters
* Inventory demand prediction
* Promotion impact analysis
* Anomaly detection
* Forecast confidence intervals
* Multiple forecasting algorithms
* Automated model selection
* Downloadable forecast reports
* Real-time data integration
* Database integration
* Automated model retraining

---

## 💡 Why Foresight?

Traditional dashboards mainly describe what happened in the past.

Foresight combines:

```text
Descriptive Analytics
        +
Time-Series Analysis
        +
Forecasting
        +
Interactive Visualization
```

This creates a workflow that moves from:

**What happened? → Why might it be happening? → What could happen next?**

The project de
