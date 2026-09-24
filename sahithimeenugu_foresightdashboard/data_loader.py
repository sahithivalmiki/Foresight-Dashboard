from pathlib import Path
from io import StringIO
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FOLDER = BASE_DIR / "data"
DATA_FILE = DATA_FOLDER / "foresight_retail.csv"


# ============================================================
# FIND SECTION
# ============================================================

def find_section(lines, section_name):
    """
    Find the line number of a section such as:
    CATEGORIES
    DATA TYPES
    TIME PERIODS
    NOTES
    DATA
    """

    for i, line in enumerate(lines):
        if line.strip() == section_name:
            return i

    return None


# ============================================================
# READ SECTION
# ============================================================

def read_section(lines, section_name, next_section_names):
    """
    Read a CSV section between two section headings.
    """

    start = find_section(lines, section_name)

    if start is None:
        raise ValueError(
            f"Section '{section_name}' was not found in the dataset."
        )

    # Header is immediately after section name
    header_line = start + 1

    # Find where the next section begins
    possible_ends = []

    for section in next_section_names:
        position = find_section(lines, section)

        if position is not None and position > header_line:
            possible_ends.append(position)

    if not possible_ends:
        end = len(lines)
    else:
        end = min(possible_ends)

    # Extract only the required lines
    section_lines = lines[header_line:end]

    # Remove completely empty lines
    section_lines = [
        line for line in section_lines
        if line.strip() != ""
    ]

    if not section_lines:
        raise ValueError(
            f"No data found inside section '{section_name}'."
        )

    # Convert selected lines into a CSV
    csv_text = "\n".join(section_lines)

    return pd.read_csv(
        StringIO(csv_text),
        low_memory=False
    )


# ============================================================
# LOAD RETAIL DATA
# ============================================================

def load_retail_data():

    print("\n" + "=" * 70)
    print("FORESIGHT RETAIL DATA LOADER")
    print("=" * 70)

    # --------------------------------------------------------
    # Check file
    # --------------------------------------------------------

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"\nDataset not found:\n{DATA_FILE}\n\n"
            "Make sure foresight_retail.csv is inside the data folder."
        )

    print("\nDataset:")
    print(DATA_FILE)

    # --------------------------------------------------------
    # Read complete file as text
    # --------------------------------------------------------

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8-sig",
        errors="replace"
    ) as file:

        lines = file.readlines()

    print("\nTotal lines:", len(lines))

    # --------------------------------------------------------
    # Detect sections
    # --------------------------------------------------------

    sections = [
        "CATEGORIES",
        "DATA TYPES",
        "ERROR TYPES",
        "GEO LEVELS",
        "TIME PERIODS",
        "NOTES",
        "DATA UPDATED ON",
        "DATA"
    ]

    print("\nDetected sections:")
    print("-" * 70)

    for section in sections:
        position = find_section(lines, section)

        if position is not None:
            print(f"{section:<20} line {position + 1}")
        else:
            print(f"{section:<20} NOT FOUND")

    # ========================================================
    # READ CATEGORIES
    # ========================================================

    categories = read_section(
        lines,
        "CATEGORIES",
        [
            "DATA TYPES",
            "ERROR TYPES",
            "GEO LEVELS",
            "TIME PERIODS",
            "NOTES",
            "DATA UPDATED ON",
            "DATA"
        ]
    )

    print("\nCategories loaded:", categories.shape)

    # ========================================================
    # READ DATA TYPES
    # ========================================================

    data_types = read_section(
        lines,
        "DATA TYPES",
        [
            "ERROR TYPES",
            "GEO LEVELS",
            "TIME PERIODS",
            "NOTES",
            "DATA UPDATED ON",
            "DATA"
        ]
    )

    print("Data types loaded:", data_types.shape)

    # ========================================================
    # READ TIME PERIODS
    # ========================================================

    time_periods = read_section(
        lines,
        "TIME PERIODS",
        [
            "NOTES",
            "DATA UPDATED ON",
            "DATA"
        ]
    )

    print("Time periods loaded:", time_periods.shape)

    # ========================================================
    # READ MAIN DATA TABLE
    # ========================================================

    data_start = find_section(lines, "DATA")

    if data_start is None:
        raise ValueError("DATA section was not found.")

    # DATA header is immediately after DATA
    data_header = data_start + 1

    data_lines = lines[data_header:]

    # Remove empty lines
    data_lines = [
        line for line in data_lines
        if line.strip() != ""
    ]

    data_text = "".join(data_lines)

    df = pd.read_csv(
        StringIO(data_text),
        low_memory=False
    )

    print("Main data loaded:", df.shape)

    # ========================================================
    # CLEAN COLUMN NAMES
    # ========================================================

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    categories.columns = [
        str(column).strip()
        for column in categories.columns
    ]

    data_types.columns = [
        str(column).strip()
        for column in data_types.columns
    ]

    time_periods.columns = [
        str(column).strip()
        for column in time_periods.columns
    ]

    # ========================================================
    # CLEAN DATA TYPES
    # ========================================================

    if "cat_idx" in df.columns:
        df["cat_idx"] = pd.to_numeric(
            df["cat_idx"],
            errors="coerce"
        )

    if "dt_idx" in df.columns:
        df["dt_idx"] = pd.to_numeric(
            df["dt_idx"],
            errors="coerce"
        )

    if "per_idx" in df.columns:
        df["per_idx"] = pd.to_numeric(
            df["per_idx"],
            errors="coerce"
        )

    if "val" in df.columns:
        df["val"] = pd.to_numeric(
            df["val"],
            errors="coerce"
        )

    # ========================================================
    # FILTER MONTHLY SALES
    # ========================================================

    print("\nAvailable data types:")

    if "dt_code" in data_types.columns:
        print(
            data_types[
                ["dt_idx", "dt_code", "dt_desc", "dt_unit"]
            ].to_string(index=False)
        )

    # Find monthly sales code
    monthly_sales = data_types[
        data_types["dt_code"].astype(str).str.upper() == "SM"
    ]

    if not monthly_sales.empty:

        monthly_sales_idx = monthly_sales.iloc[0]["dt_idx"]

        print(
            "\nMonthly sales data type found:",
            monthly_sales_idx
        )

        df = df[
            df["dt_idx"] == monthly_sales_idx
        ].copy()

    else:

        print(
            "\nWARNING: Monthly sales code 'SM' "
            "was not found."
        )

    # ========================================================
    # MERGE CATEGORY INFORMATION
    # ========================================================

    if (
        "cat_idx" in df.columns
        and "cat_idx" in categories.columns
    ):

        category_columns = [
            column
            for column in [
                "cat_idx",
                "cat_code",
                "cat_desc",
                "cat_indent"
            ]
            if column in categories.columns
        ]

        df = df.merge(
            categories[category_columns],
            on="cat_idx",
            how="left"
        )

    # ========================================================
    # MERGE TIME PERIOD INFORMATION
    # ========================================================

    if (
        "per_idx" in df.columns
        and "per_idx" in time_periods.columns
    ):

        df = df.merge(
            time_periods,
            on="per_idx",
            how="left"
        )

    # ========================================================
    # CLEAN VALUES
    # ========================================================

    if "val" in df.columns:

        df["val"] = pd.to_numeric(
            df["val"],
            errors="coerce"
        )

    # Remove completely invalid rows
    df = df.dropna(
        subset=["val"]
    )

    # ========================================================
    # FINAL INFORMATION
    # ========================================================

    print("\n" + "=" * 70)
    print("FINAL DATASET")
    print("=" * 70)

    print("\nShape:", df.shape)

    print("\nColumns:")
    for i, column in enumerate(df.columns, 1):
        print(f"{i}. {column}")

    print("\nFirst 5 rows:")
    print(
        df.head().to_string(index=False)
    )

    print("\n" + "=" * 70)
    print("DATA LOADING COMPLETED")
    print("=" * 70)

    return df


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    df = load_retail_data()

    print("\nDataset successfully loaded.")
    print("Rows:", len(df))