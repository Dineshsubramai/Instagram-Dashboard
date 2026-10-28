
import pandas as pd
df = pd.read_csv(r"C:\Users\Kaar User\Desktop\New folder\Instagram Analytics\archive (1)\top_200_instagrammers.csv")
df = df[
    [
        "Main topic",
        "Main video category",
        "Followers",
        "Engagement Rate",
        "Likes Avg.",
        "Comments Avg."
    ]
]


df["Main topic"] = df["Main topic"].fillna("Unknown")
df["Main video category"] = df["Main video category"].fillna("Unknown")


numeric_columns = [
    "Followers",
    "Engagement Rate",
    "Likes Avg.",
    "Comments Avg."
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")
    df[column] = df[column].fillna(0)

print("Data cleaning completed!")
print()

print(df.head())

print()

print("Missing values:")
print(df.isnull().sum())
