
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# Average Engagement Rate by Category

base_dir = Path(__file__).resolve().parent.parent
csv_candidates = [
    base_dir / "archive (1)" / "top_200_instagrammers.csv",
    base_dir / "top_200_instagrammers.csv",
    base_dir / "archive (1)" / "top_200_instagrammers.csv",
]

csv_path = next((path for path in csv_candidates if path.exists()), csv_candidates[0])

if not csv_path.exists():
    st.error(f"CSV file not found. Expected one of: {', '.join(str(p) for p in csv_candidates)}")
    st.stop()

try:
    df = pd.read_csv(csv_path)
except Exception as exc:
    st.error(f"Could not read CSV: {exc}")
    st.stop()

filtered_df = df.copy()

required_columns = {"Main video category", "Engagement Rate"}
if filtered_df.empty or not required_columns.issubset(filtered_df.columns):
    st.warning("No data available to calculate engagement by category.")
    st.stop()

engagement_cat = (
    filtered_df.groupby("Main video category", dropna=False)["Engagement Rate"]
    .mean()
    .reset_index()
)

engagement_cat["Engagement %"] = engagement_cat["Engagement Rate"] * 100
engagement_cat = engagement_cat.sort_values(by="Engagement %", ascending=False)

if engagement_cat.empty:
    st.warning("No category-level engagement values are available.")
    st.stop()

st.subheader("🔥 Average Engagement Rate by Category")

fig_engage = px.bar(
    engagement_cat,
    x="Main video category",
    y="Engagement %",
    color="Engagement %",
    text_auto=".2f",
    color_continuous_scale="Reds",
)

st.plotly_chart(fig_engage, use_container_width=True)

# Highest engagement category
best_content = engagement_cat.iloc[0]

st.subheader("🏆 Best Performing Content")

st.success(
    f"""
Category: {best_content['Main video category']}

Average Engagement:
{best_content['Engagement %']:.2f}%
"""
)

