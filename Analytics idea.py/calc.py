
import streamlit as st
import pandas as pd


def load_data():

    df = pd.read_csv(
        "data/top_200_instagrammers.csv"
    )

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
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0)

    return df


st.set_page_config(
    page_title="Instagram Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📸 Instagram Category Analytics Dashboard")

df = load_data()


st.sidebar.header("Filters")

categories = df["Main video category"].unique()

selected_category = st.sidebar.multiselect(
    "Select Video Category",
    categories,
    default=list(categories)
)

filtered_df = df[
    df["Main video category"].isin(selected_category)
]


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Influencers",
    len(filtered_df)
)

col2.metric(
    "Avg Followers",
    f"{filtered_df['Followers'].mean():,.0f}"
)

col3.metric(
    "Avg Engagement",
    f"{filtered_df['Engagement Rate'].mean() * 100:.2f}%"
)

col4.metric(
    "Categories",
    filtered_df["Main video category"].nunique()
)

st.divider()

st.subheader("Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)
