import plotly.express as px
import pandas as pd
import streamlit as st

# Ensure the filtered data exists before computing category summaries.
if "filtered_df" not in globals():
    filtered_df = pd.DataFrame(columns=["Main video category", "Followers"])

# Average Followers by Category
followers_cat = (
    filtered_df.groupby("Main video category")["Followers"]
    .mean()
    .reset_index()
    .sort_values(by="Followers", ascending=False)
)

st.subheader("👥 Average Followers by Category")

if not followers_cat.empty:

    fig_followers = px.bar(
        followers_cat,
        x="Main video category",
        y="Followers",
        color="Followers",
        text_auto=".2s",
        color_continuous_scale="Viridis",
        title="Average Followers by Category"
    )

    fig_followers.update_layout(
        xaxis_title="Category",
        yaxis_title="Average Followers",
        yaxis_tickformat=".0s"
    )

    st.plotly_chart(
        fig_followers,
        use_container_width=True
    )

    # Top category insight
    top_followers = followers_cat.iloc[0]

    st.success(
        f"🏆 Top Category: **{top_followers['Main video category']}** | "
        f"Average Followers: **{top_followers['Followers']:,.0f}**"
    )

else:
    st.warning("No data available for selected category.")