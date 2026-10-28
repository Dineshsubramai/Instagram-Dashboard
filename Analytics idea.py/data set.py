
import pandas as pd

df = pd.read_csv(r"C:\Users\Kaar User\Desktop\New folder\Instagram Analytics\archive (1)\top_200_instagrammers.csv")

print("Data loaded successfully!")
print()

print("First 5 rows:")
print(df.head())

print()

print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print()

print("Column names:")
print(df.columns.tolist())
