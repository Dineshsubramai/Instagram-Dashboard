
import streamlit as st
import pandas as pd


def load_data():

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
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0)

    return df


st.set_page_config(
    page_title="Instagram Category Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📸 Instagram Category Analytics Dashboard")

st.markdown(
    "Analyze categories, followers, engagement "
    "and predict performance using Machine Learning."
)

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

st.write("### Filtered Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)
