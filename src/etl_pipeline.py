import sqlite3
import pandas as pd
from pathlib import Path

from data_cleaning import clean_sales_data

# Define project paths
PROJECT_ROOT = Path(file).resolve().parents[1]
CLEANED_FILE = PROJECT_ROOT / "data" / "cleaned_sales.csv"
DATABASE_FILE = PROJECT_ROOT / "retail_analytics.db"


def run_etl_pipeline():
    """Extract, transform, and load retail sales data."""

    print("Starting retail ETL pipeline...")

    # Step 1: Transform and clean the raw data
    clean_sales_data()

    # Step 2: Extract cleaned data
    df = pd.read_csv(CLEANED_FILE)

    # Step 3: Load data into SQLite
    with sqlite3.connect(DATABASE_FILE) as connection:
        df.to_sql(
            "sales",
            connection,
            if_exists="replace",
            index=False
        )

    print("ETL pipeline completed successfully!")
    print(f"Transactions loaded: {len(df)}")
    print(f"Database location: {DATABASE_FILE}")


if name == "main":
    run_etl_pipeline()
