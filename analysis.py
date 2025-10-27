# analysis.py
# Sample script for Retail Business Performance & Profitability Analysis
# Requires: pandas, matplotlib, seaborn
# Usage: place `transactions.csv` inside `data/` and run: python analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_PATH = os.path.join("data", "transactions.csv")

def load_data(path=DATA_PATH):
    # Example expected columns: order_id, order_date, product_id, product_name,
    # category, quantity, unit_price, cost_price, inventory_days, region
    df = pd.read_csv(path, parse_dates=["order_date"])
    return df

def preprocess(df):
    df["sales"] = df["quantity"] * df["unit_price"]
    df["profit"] = df["quantity"] * (df["unit_price"] - df["cost_price"])
    return df

def top_categories(df, n=10):
    cat = df.groupby("category")[["sales","profit"]].sum().sort_values("profit", ascending=False)
    print("Top categories by profit:")
    print(cat.head(n))
    return cat

def monthly_trends(df):
    df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    monthly = df.groupby(["month","category"])["sales"].sum().unstack(fill_value=0)
    monthly.plot(figsize=(10,5))
    plt.title("Monthly Sales by Category")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig("monthly_sales_by_category.png")
    print("Saved plot: monthly_sales_by_category.png")

def main():
    if not os.path.exists(DATA_PATH):
        print(f"Data file not found at {DATA_PATH}. Please add your transactions.csv file in data/")
        return
    df = load_data()
    df = preprocess(df)
    top_categories(df)
    monthly_trends(df)

if __name__ == "__main__":
    main()