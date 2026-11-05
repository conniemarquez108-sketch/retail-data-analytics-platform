import pandas as pd
from pathlib import Path

# Define project paths
PROJECT_ROOT = Path(file).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "sample_sales.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "cleaned_sales.csv"


def clean_sales_data():
    """Clean and validate retail sales transactions."""

    # Load sales data
    df = pd.read_csv(INPUT_FILE)

    # Remove duplicate transactions
    df = df.drop_duplicates(subset=["transaction_id"])

    # Convert columns to appropriate data types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(
        df["unit_price"], errors="coerce"
    )

    # Remove rows with missing or invalid values
    df = df.dropna(
        subset=[
            "transaction_id",
            "date",
            "store",
            "product",
            "quantity",
            "unit_price"
        ]
    )

    # Keep only valid sales
    df = df[
        (df["quantity"] > 0) &
        (df["unit_price"] >= 0)
    ]

    # Calculate transaction revenue
    df["total_sales"] = df["quantity"] * df["unit_price"]

    # Save cleaned data
    df.to_csv(OUTPUT_FILE, index=False)

    print("Sales data cleaning completed!")
    print(f"Valid transactions: {len(df)}")
    print(f"Total revenue: ${df['total_sales'].sum():,.2f}")
    print(f"Cleaned data saved to: {OUTPUT_FILE}")


if name == "main":
    clean_sales_data()
