from pathlib import Path
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

# Get the main Foresight project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Data folder
DATA_FOLDER = BASE_DIR / "data"


# ============================================================
# 2. FIND DATA FILES
# ============================================================

def find_data_files():
    """
    Find CSV, TXT, Excel and XLS files
    inside the data folder.
    """

    files = []

    for extension in ["*.csv", "*.txt", "*.xlsx", "*.xls"]:
        files.extend(DATA_FOLDER.rglob(extension))

    return files


# ============================================================
# 3. READ DATA FILE
# ============================================================

def read_file(file_path):
    """
    Read CSV, TXT or Excel files.
    """

    suffix = file_path.suffix.lower()

    # ---------------- CSV ----------------
    if suffix == ".csv":

        df = pd.read_csv(
            file_path,
            low_memory=False,
            on_bad_lines="warn"
        )

        return df

    # ---------------- TXT ----------------
    elif suffix == ".txt":

        df = pd.read_csv(
            file_path,
            sep=None,
            engine="python",
            low_memory=False,
            on_bad_lines="warn"
        )

        return df

    # ---------------- Excel ----------------
    elif suffix in [".xlsx", ".xls"]:

        df = pd.read_excel(file_path)

        return df

    else:

        return None


# ============================================================
# 4. INSPECT DATASET
# ============================================================

def inspect_files():

    print("\n" + "=" * 70)
    print("FORESIGHT DATASET INSPECTION")
    print("=" * 70)

    # Check whether data folder exists
    if not DATA_FOLDER.exists():

        print("\nERROR: Data folder does not exist.")
        print("Expected location:")
        print(DATA_FOLDER)

        return

    # Find files
    files = find_data_files()

    print("\nData folder:")
    print(DATA_FOLDER)

    print("\nFiles found:")
    print("-" * 70)

    if not files:

        print("No data files found.")
        print("\nMake sure your dataset is inside:")
        print(DATA_FOLDER)

        return

    # ========================================================
    # PROCESS EACH FILE
    # ========================================================

    for file in files:

        print("\nFile:")
        print(file)

        print("-" * 70)

        try:

            # Read dataset
            df = read_file(file)

            # Check if dataframe was created
            if df is None:

                print("Unsupported file format.")

                continue

            # =================================================
            # BASIC INFORMATION
            # =================================================

            print("\nDATASET INFORMATION")
            print("-" * 70)

            print("Number of rows    :", df.shape[0])
            print("Number of columns :", df.shape[1])

            # =================================================
            # COLUMN NAMES
            # =================================================

            print("\nCOLUMN NAMES")
            print("-" * 70)

            for i, column in enumerate(df.columns, start=1):

                print(f"{i}. {column}")

            # =================================================
            # DATA TYPES
            # =================================================

            print("\nDATA TYPES")
            print("-" * 70)

            print(df.dtypes)

            # =================================================
            # FIRST 5 ROWS
            # =================================================

            print("\nFIRST 5 ROWS")
            print("-" * 70)

            print(df.head())

            # =================================================
            # MISSING VALUES
            # =================================================

            print("\nMISSING VALUES")
            print("-" * 70)

            missing_values = df.isnull().sum()

            missing_table = pd.DataFrame({
                "Column": missing_values.index,
                "Missing Values": missing_values.values
            })

            print(missing_table.to_string(index=False))

            # =================================================
            # DUPLICATES
            # =================================================

            print("\nDUPLICATE ROWS")
            print("-" * 70)

            duplicate_count = df.duplicated().sum()

            print("Duplicate rows:", duplicate_count)

            # =================================================
            # NUMERICAL SUMMARY
            # =================================================

            print("\nNUMERICAL SUMMARY")
            print("-" * 70)

            print(df.describe(include="all").transpose())

            # =================================================
            # UNIQUE VALUES
            # =================================================

            print("\nUNIQUE VALUES")
            print("-" * 70)

            for column in df.columns:

                try:

                    unique_count = df[column].nunique()

                    print(
                        f"{column}: "
                        f"{unique_count} unique values"
                    )

                except Exception:

                    pass

            print("\n" + "=" * 70)
            print("INSPECTION COMPLETED")
            print("=" * 70)

        except Exception as error:

            print("\nCould not read file.")
            print("Error:", error)


# ============================================================
# 5. RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    inspect_files()