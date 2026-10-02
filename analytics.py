import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


st.set_page_config(
    page_title="Instagram Category Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📸 Instagram Category Analytics Dashboard")
st.markdown("Analyze categories, followers, engagement and predict performance using Machine Learning.")


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

st.sidebar.header("Filters")

selected_category = st.sidebar.multiselect(
    "Select Video Category",
    df["Main video category"].unique(),
    default=df["Main video category"].unique()
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
    f"{filtered_df['Engagement Rate'].mean()*100:.2f}%"
)

col4.metric(
    "Categories",
    filtered_df["Main video category"].nunique()
)

st.divider()


st.subheader("🥧 Category Distribution")

category_count = (
    filtered_df["Main video category"]
    .value_counts()
    .reset_index()
)

category_count.columns = ["Category", "Count"]

fig_pie = px.pie(
    category_count,
    names="Category",
    values="Count",
    hole=0.45,
    color_discrete_sequence=px.colors.qualitative.Bold
)

st.plotly_chart(fig_pie, use_container_width=True)


st.subheader("👥 Average Followers by Category")

followers_cat = (
    filtered_df.groupby("Main video category")["Followers"]
    .mean()
    .reset_index()
)

followers_cat = followers_cat.sort_values(
    by="Followers",
    ascending=False
)

fig_followers = px.bar(
    followers_cat,
    x="Main video category",
    y="Followers",
    color="Followers",
    text_auto=".2s",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig_followers, use_container_width=True)


st.subheader("🔥 Average Engagement Rate by Category")

engagement_cat = (
    filtered_df.groupby("Main video category")["Engagement Rate"]
    .mean()
    .reset_index()
)

engagement_cat["Engagement %"] = (
    engagement_cat["Engagement Rate"] * 100
)

engagement_cat = engagement_cat.sort_values(
    by="Engagement %",
    ascending=False
)

fig_engage = px.bar(
    engagement_cat,
    x="Main video category",
    y="Engagement %",
    color="Engagement %",
    text_auto=".2f",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_engage, use_container_width=True)


st.subheader("🏆 Best Performing Niche")

best_niche = engagement_cat.iloc[0]

st.success(
    f"""
Best Category: {best_niche['Main video category']}

Average Engagement:
{best_niche['Engagement %']:.2f}%
"""
)


st.subheader("⭐ Category Attracting Most Followers")

top_followers = followers_cat.iloc[0]

st.info(
    f"""
Top Category: {top_followers['Main video category']}

Average Followers:
{top_followers['Followers']:,.0f}
"""
)


st.subheader("🤖 Machine Learning Analysis")

ml_df = filtered_df.copy()

features = ml_df[
    ["Followers", "Likes Avg.", "Comments Avg."]
].fillna(0)

target = ml_df["Engagement Rate"].fillna(0)

X_train, X_test, y_train, y_test = train_test_split(
    features,
    target,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

score = r2_score(y_test, predictions)

st.metric(
    "ML Accuracy (R² Score)",
    f"{score:.2f}"
)

feature_importance = pd.DataFrame({
    "Feature": features.columns,
    "Importance": model.feature_importances_
})

fig_ml = px.bar(
    feature_importance,
    x="Feature",
    y="Importance",
    color="Importance",
    title="Feature Importance for Engagement Prediction"
)

st.plotly_chart(fig_ml, use_container_width=True)


st.subheader("📈 AI Insights")

highest_eng = engagement_cat.iloc[0]["Main video category"]
highest_follower = followers_cat.iloc[0]["Main video category"]

st.write(f"✅ Highest Engagement Category: **{highest_eng}**")
st.write(f"✅ Highest Followers Category: **{highest_follower}**")

st.write("Dashboard analysis completed successfully.")