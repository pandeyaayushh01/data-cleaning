import numpy as np
import pandas as pd

# 1. Load the dataset
df = pd.read_csv(r"C:\Users\Ayush Pandey\Downloads\dirty_cafe_sales.csv")

# 2. Replace bad text values ("ERROR", "UNKNOWN", blanks) with NaN (missing)
bad_values = ["ERROR", "UNKNOWN", "", "nan", "None"]
df = df.replace(bad_values, np.nan)

# Remove extra spaces around text
for col in ["Transaction ID", "Item", "Payment Method", "Location"]:
    df[col] = df[col].str.strip()

# 3. Convert text numbers and dates into proper numbers and dates
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Price Per Unit"] = pd.to_numeric(df["Price Per Unit"], errors="coerce")
df["Total Spent"] = pd.to_numeric(df["Total Spent"], errors="coerce")
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")

# 4. Fill missing prices using each menu item's known price
menu_prices = {
    "Cookie": 1.0,
    "Tea": 1.5,
    "Coffee": 2.0,
    "Cake": 3.0,
    "Juice": 3.0,
    "Sandwich": 4.0,
    "Smoothie": 4.0,
    "Salad": 5.0,
}

missing_price = df["Price Per Unit"].isna()
df.loc[missing_price, "Price Per Unit"] = df.loc[missing_price, "Item"].map(menu_prices)

# 5. Fill missing math values (Total = Quantity * Price Per Unit)
missing_total = df["Total Spent"].isna()
df.loc[missing_total, "Total Spent"] = (
    df.loc[missing_total, "Quantity"] * df.loc[missing_total, "Price Per Unit"]
)

missing_qty = df["Quantity"].isna()
df.loc[missing_qty, "Quantity"] = (
    df.loc[missing_qty, "Total Spent"] / df.loc[missing_qty, "Price Per Unit"]
)

missing_price_again = df["Price Per Unit"].isna()
df.loc[missing_price_again, "Price Per Unit"] = (
    df.loc[missing_price_again, "Total Spent"] / df.loc[missing_price_again, "Quantity"]
)

# 6. Fill missing Item names when the price belongs to only one item
unique_price_items = {
    1.0: "Cookie",
    1.5: "Tea",
    2.0: "Coffee",
    5.0: "Salad",
}
missing_item = df["Item"].isna()
df.loc[missing_item, "Item"] = df.loc[missing_item, "Price Per Unit"].map(
    unique_price_items
)

# 7. Label remaining missing text categories as "Unknown"
for col in ["Item", "Payment Method", "Location"]:
    df[col] = df[col].fillna("Unknown")

# 8. Remove duplicate rows (if any) and save the cleaned file
df = df.drop_duplicates()
df.to_csv("cleaned_cafe_sales.csv", index=False)

print("Done! Missing values left per column:")
print(df.isna().sum())