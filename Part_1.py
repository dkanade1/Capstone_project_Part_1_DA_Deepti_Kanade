import pandas as pd
import numpy as np
from scipy.stats import zscore
df = pd.read_csv("Task_8_1.csv")

#find out missing count
print("_______Missing values in the CSV __________")
missing_count = df.isnull().sum()
print(missing_count)

#Converting the date fields from string to Date type
df["OrderDate"] = pd.to_datetime(df["OrderDate"],format="mixed", errors="coerce")
df["ShippedDate"] = pd.to_datetime(df["ShippedDate"],format="mixed", errors="coerce")

##Calculate median of shipping delays
median_delay = (df["ShippedDate"] - df["OrderDate"]).dt.days.median()
mask = df["ShippedDate"].isna() & df["OrderDate"].notna()
print("\n_________Displaying Rows with valid order date but null shipping date________\n")
print(df.loc[mask].to_string())


##Update the shipping date with the delay from order date
df.loc[mask, "ShippedDate"] = (
   df.loc[mask, "OrderDate"] +
   pd.to_timedelta(int(median_delay), unit="D")
)
print("_____________Updated shipped date after imputation____________\n")
print(df.loc[mask].to_string())


# ## Fill 'unknown' values in region and country column with null values
print("_________________________________\n")
print("No of Rows with null values in Region and country Column: ",df["Region"].isna().sum(),df["Country"].isna().sum())
df["Region"] = df["Region"].fillna("Unknown")
df["Country"] = df["Country"].fillna("Unknown")
print("No of Rows with null values in Region and country Column after updating with unknown: ",df["Region"].isna().sum(),df["Country"].isna().sum())

#Calculating missing values after imputaion
missing_count2 = df.isnull().sum()
print(f"\n_______________Missing value count after imputation____________\n",missing_count2)

#  Check and remove duplicates
print("_______________Checking for duplicate rows_____________\n")
print("Rows before:", len(df))
print("Duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()
print("Rows after:", len(df))

def detect_zscore_outliers( df, column, threshold=3):
    z = zscore(df[column], nan_policy="omit")
# print(z)
    return df[np.abs(z) > threshold]

numeric_columns = [
    "Freight",
    "UnitPrice",
    "Quantity",
    "Discount",
    "UnitsInStock",
    "UnitsOnOrder"
]

def detect_iqr_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[column] < lower) | (df[column] > upper)]
print("\n_______________Outliers Counts__________")
for col in numeric_columns:
    print(f"\n--- {col} ---")
    print("Z-score outliers:", len(detect_zscore_outliers(df, col)))
    print("IQR outliers:", len(detect_iqr_outliers(df, col)))

##df.to_csv("Task_1_cleaned.csv", index=False)
