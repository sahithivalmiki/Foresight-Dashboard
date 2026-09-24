import pandas as pd
import numpy as np


def create_features(df):

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date")

    # Calendar features

    df["year"] = df["date"].dt.year

    df["month"] = df["date"].dt.month

    df["quarter"] = df["date"].dt.quarter

    df["month_name"] = df["date"].dt.strftime("%b")

    # Total retail growth

    if "total_retail" in df.columns:

        df["total_mom_growth"] = (
            df["total_retail"]
            .pct_change() * 100
        )

        df["total_yoy_growth"] = (
            df["total_retail"]
            .pct_change(12) * 100
        )

        df["rolling_3m"] = (
            df["total_retail"]
            .rolling(3)
            .mean()
        )

        df["rolling_12m"] = (
            df["total_retail"]
            .rolling(12)
            .mean()
        )

    return df
RETAIL_COLUMNS = {

    "total_retail":
        "Retail, total",

    "motor_vehicle":
        "Motor Vehicle and Parts Dealers",

    "furniture":
        "Furniture and Home Furnishings Stores",

    "electronics":
        "Electronics and Appliance Stores",

    "building_material":
        "Building Material and Garden Equipment",

    "food_beverage":
        "Food and Beverage Stores",

    "grocery":
        "Grocery Stores",

    "health_personal":
        "Health and Personal Care Stores",

    "gasoline":
        "Gasoline Stations",

    "clothing":
        "Clothing and Clothing Accessories Stores",

    "sporting_goods":
        "Sporting Goods, Hobby, Book, and Music Stores",

    "general_merchandise":
        "General Merchandise Stores",

    "miscellaneous":
        "Miscellaneous Store Retailers",

    "nonstore":
        "Nonstore Retailers",

    "food_services":
        "Food Services and Drinking Places"
}