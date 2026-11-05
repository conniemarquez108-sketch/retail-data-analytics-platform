import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(file).resolve().parents[1]
DATABASE_FILE = PROJECT_ROOT / "retail_analytics.db"


def generate_sales_analytics():
    """Generate business insights from retail sales data."""

    if not DATABASE_FILE.exists():
        print("Database not found. Run etl_pipeline.py first.")
        return

    with sqlite3.connect(DATABASE_FILE) as connection:
        df = pd.read_sql_query(
            "SELECT * FROM sales",
            connection
        )

    if df.empty:
        print("No sales records found.")
        return

    # Overall business performance
    total_revenue = df["total_sales"].sum()
    total_transactions = len(df)
    average_transaction = total_revenue / total_transactions

    print("\n===== RETAIL SALES ANALYTICS =====")
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Total Transactions: {total_transactions}")
    print(f"Average Transaction: ${average_transaction:,.2f}")

    # Best-selling products
    print("\n===== TOP PRODUCTS =====")
    products = (
        df.groupby("product")["quantity"]
        .sum()
        .sort_values(ascending=False)
    )
    print(products.head(5))

    # Revenue by category
    print("\n===== REVENUE BY CATEGORY =====")
    categories = (
        df.groupby("category")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )
    print(categories)

    # Revenue by store
    print("\n===== STORE PERFORMANCE =====")
    stores = (
        df.groupby("store")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )
    print(stores)

    # Export analytics reports
    report_file = PROJECT_ROOT / "data" / "sales_report.csv"
    categories.to_csv(report_file, header=["revenue"])

    print(f"\nReport saved to: {report_file}")


if name == "main":
    generate_sales_analytics()
