import pandas as pd
import numpy as np

# Load the raw data
df = pd.read_csv('9. Sales-Data-Analysis.csv')

# Data cleaning steps
# 1. Strip whitespace from all string columns
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].str.strip()

# 2. Convert Date to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

# 3. Calculate Revenue (Price * Quantity)
df['Revenue'] = df['Price'] * df['Quantity']

# 4. Handle any missing values
print(f"Missing values before handling:\n{df.isnull().sum()}\n")
df = df.dropna()

# 5. Sort by date
df = df.sort_values('Date')

# 6. Display basic statistics
print("Data Summary:")
print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"Total records: {len(df)}")
print(f"Total revenue: ${df['Revenue'].sum():,.2f}")
print(f"\nTop products by revenue:")
print(df.groupby('Product')['Revenue'].sum().sort_values(ascending=False))

# Save cleaned data
df.to_csv('cleaned_sales_data.csv', index=False)
print("\n✓ Cleaned data saved to 'cleaned_sales_data.csv'")
