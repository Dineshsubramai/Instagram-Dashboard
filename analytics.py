from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

st.set_page_config(
    page_title="Instagram Analytics",
    page_icon="📊",
    layout="wide",
)

# Editorial dark theme with a bright mint accent.
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --bg: #080d18;
    --panel: #101827;
    --panel2: #131f30;
    --line: #243247;
    --muted: #91a1b7;
    --text: #f2f6fc;
    --mint: #55e6c1;
}

html,
body,
[data-testid="stAppViewContainer"] {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(8, 13, 24, 0.86);
}

[data-testid="stSidebar"] {
    background: #0b1220;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] * {
    color: var(--text);
}

.block-container {
    max-width: 1440px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}

h1,
h2,
h3 {
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: -0.035em;
    color: var(--text) !important;
}

.hero {
    padding: 1.7rem 1.9rem;
    margin-bottom: 1.45rem;
    border: 1px solid #26374d;
    border-radius: 22px;
    background:
        radial-gradient(
            ellipse at 88% 0%,
            rgba(85, 230, 193, 0.15),
            transparent 40%
        ),
        linear-gradient(120deg, #111c2d, #0d1524 70%);
}

.eyebrow {
    color: var(--mint);
    text-transform: uppercase;
    letter-spacing: 0.16em;
    font-weight: 700;
    font-size: 0.72rem;
}

.hero h1 {
    margin: 0.4rem 0 0.35rem;
    font-size: 2rem;
}

.hero p {
    color: #a8b6c9;
    margin: 0;
    font-size: 1rem;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #121e2f, #0f1827);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1.15rem 1.2rem;
    min-height: 122px;
}

[data-testid="stMetricLabel"] {
    color: #a7b5c8 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-family: 'Manrope', sans-serif;
}

[data-testid="stMetricDelta"] {
    color: var(--mint) !important;
}

[data-testid="stPlotlyChart"] {
    background: #101827;
    border: 1px solid var(--line);
    border-radius: 17px;
    padding: 0.7rem;
}

[data-testid="stPlotlyChart"] > div {
    border-radius: 12px;
}

[data-testid="stAlert"] {
    background: #111e2d;
    border: 1px solid #26374d;
    border-radius: 14px;
    color: var(--text);
}

[data-testid="stMarkdownContainer"] p {
    color: #b2bfd0;
}

hr {
    border-color: var(--line);
}

.section-note {
    color: var(--muted);
    font-size: 0.88rem;
    margin-top: -0.5rem;
    margin-bottom: 0.8rem;
}

footer {
    visibility: hidden;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

DATA_PATH = (
    Path(__file__).resolve().parent
    / "archive (1)"
    / "top_200_instagrammers.csv"
)
DATA_COLUMNS = [
    "Main topic",
    "Main video category",
    "Followers",
    "Engagement Rate",
    "Likes Avg.",
    "Comments Avg.",
]
FEATURE_COLUMNS = ["Followers", "Likes Avg.", "Comments Avg."]

if not DATA_PATH.is_file():
    st.error(f"Could not find the creator data file: {DATA_PATH}")
    st.stop()

creators_df = pd.read_csv(DATA_PATH)
creators_df = creators_df[DATA_COLUMNS].copy()
creators_df["Main topic"] = creators_df["Main topic"].fillna("Unknown")
creators_df["Main video category"] = creators_df["Main video category"].fillna(
    "Unknown"
)

st.markdown("""
<div class="hero">
  <div class="eyebrow">Creator intelligence · Instagram</div>
  <h1>Category performance</h1>
  <p>Explore audience scale, engagement quality, and the signals behind
     high-performing creator niches.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### Dashboard controls")
st.sidebar.caption("Choose categories to update every view")
available_categories = sorted(creators_df["Main video category"].unique())
selected_categories = st.sidebar.multiselect(
    "Video categories",
    available_categories,
    default=available_categories,
)
filtered_creators = creators_df[
    creators_df["Main video category"].isin(selected_categories)
]

if filtered_creators.empty:
    st.info("Select at least one category to see the dashboard.")
    st.stop()

creator_count, followers_average, engagement_average, category_count = st.columns(4)
creator_count.metric("Creators analyzed", f"{len(filtered_creators):,}")
followers_average.metric(
    "Average followers",
    f"{filtered_creators['Followers'].mean():,.0f}",
)
engagement_average.metric(
    "Average engagement",
    f"{filtered_creators['Engagement Rate'].mean() * 100:.2f}%",
)
category_count.metric(
    "Categories selected",
    f"{filtered_creators['Main video category'].nunique():,}",
)
st.write("")


# Shared chart styling keeps visualizations consistent with the dashboard theme.
CHART_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "DM Sans, sans-serif", "color": "#dce6f3"},
    "margin": {"l": 20, "r": 20, "t": 48, "b": 20},
    "legend": {"bgcolor": "rgba(0,0,0,0)"},
    "hoverlabel": {"bgcolor": "#182538", "font_color": "#f2f6fc"},
}

# Category landscape
st.subheader("Category landscape")
st.markdown(
    '<div class="section-note">Compare the mix of creators with audience size '
    "and engagement by niche.</div>",
    unsafe_allow_html=True,
)
left_column, right_column = st.columns([0.9, 1.1], gap="large")

category_counts = (
    filtered_creators["Main video category"]
    .value_counts()
    .rename_axis("Category")
    .reset_index(name="Creators")
)
category_pie = px.pie(
    category_counts,
    names="Category",
    values="Creators",
    hole=0.68,
    color_discrete_sequence=px.colors.qualitative.Safe,
)
category_pie.update_traces(
    textposition="inside",
    textinfo="percent",
    marker={"line": {"color": "#101827", "width": 3}},
)
category_pie.update_layout(
    **CHART_LAYOUT,
    height=390,
    annotations=[
        {
            "text": (
                f"{len(filtered_creators)}<br>"
                "<span style='font-size:12px;color:#91a1b7'>creators</span>"
            ),
            "x": 0.5,
            "y": 0.5,
            "showarrow": False,
            "font": {"size": 22, "color": "#f2f6fc", "family": "Manrope"},
        }
    ],
)
with left_column:
    st.markdown("#### Creator mix")
    st.plotly_chart(category_pie, width="stretch")

followers_by_category = (
    filtered_creators.groupby("Main video category", as_index=False)["Followers"]
    .mean()
    .sort_values("Followers", ascending=True)
)
followers_chart = px.bar(
    followers_by_category,
    x="Followers",
    y="Main video category",
    orientation="h",
    color="Followers",
    text="Followers",
    color_continuous_scale=[[0, "#287d84"], [1, "#55e6c1"]],
)
followers_chart.update_traces(
    texttemplate="%{text:.2s}",
    textposition="outside",
    cliponaxis=False,
    marker_line_width=0,
)
followers_chart_layout = {
    **CHART_LAYOUT,
    "margin": {"l": 15, "r": 65, "t": 24, "b": 35},
}
followers_chart.update_layout(
    **followers_chart_layout,
    coloraxis_showscale=False,
    yaxis_title="",
    xaxis_title="Average followers",
    height=390,
)
with right_column:
    st.markdown("#### Audience scale by category")
    st.plotly_chart(followers_chart, width="stretch")

# Engagement and growth signals
st.subheader("Engagement & growth signals")
st.markdown(
    '<div class="section-note">Spot high-engagement niches and understand '
    "which creator metrics matter most.</div>",
    unsafe_allow_html=True,
)
engagement_by_category = (
    filtered_creators.groupby("Main video category", as_index=False)[
        "Engagement Rate"
    ]
    .mean()
)
engagement_by_category["Engagement %"] = (
    engagement_by_category["Engagement Rate"] * 100
)
engagement_by_category = engagement_by_category.sort_values(
    "Engagement %",
    ascending=True,
)

model_creators = filtered_creators.dropna(subset=["Engagement Rate"])
model_creators = model_creators[
    model_creators[FEATURE_COLUMNS].notna().any(axis=1)
]
if len(model_creators) >= 5:
    features = model_creators[FEATURE_COLUMNS].fillna(0)
    target = model_creators["Engagement Rate"]
    features_train, features_test, target_train, target_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
    )
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
    )
    model.fit(features_train, target_train)
    model_score = r2_score(target_test, model.predict(features_test))
    feature_importance = pd.DataFrame(
        {
            "Signal": FEATURE_COLUMNS,
            "Importance": model.feature_importances_,
        }
    ).sort_values("Importance", ascending=True)
else:
    model_score = None
    feature_importance = pd.DataFrame(
        {"Signal": FEATURE_COLUMNS, "Importance": [0, 0, 0]}
    )

engagement_chart = px.bar(
    engagement_by_category,
    x="Engagement %",
    y="Main video category",
    orientation="h",
    color="Engagement %",
    text="Engagement %",
    color_continuous_scale=[[0, "#7b5ce1"], [1, "#c5a6ff"]],
)
engagement_chart.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside",
    cliponaxis=False,
    marker_line_width=0,
)
engagement_chart_layout = {
    **CHART_LAYOUT,
    "margin": {"l": 15, "r": 65, "t": 24, "b": 35},
}
engagement_chart.update_layout(
    **engagement_chart_layout,
    coloraxis_showscale=False,
    yaxis_title="",
    xaxis_title="Average engagement",
    height=390,
)

importance_chart = px.bar(
    feature_importance,
    x="Importance",
    y="Signal",
    orientation="h",
    color="Importance",
    text="Importance",
    color_continuous_scale=[[0, "#287d84"], [1, "#55e6c1"]],
)
importance_chart.update_traces(
    texttemplate="%{text:.0%}",
    textposition="outside",
    cliponaxis=False,
    marker_line_width=0,
)
importance_chart_layout = {
    **CHART_LAYOUT,
    "margin": {"l": 15, "r": 50, "t": 24, "b": 35},
}
importance_chart.update_layout(
    **importance_chart_layout,
    coloraxis_showscale=False,
    yaxis_title="",
    xaxis_title="Relative model importance",
    height=390,
)

left_column, right_column = st.columns(2, gap="large")
with left_column:
    st.markdown("#### Engagement by category")
    st.plotly_chart(engagement_chart, width="stretch")
with right_column:
    st.markdown("#### Signals linked to engagement")
    st.plotly_chart(importance_chart, width="stretch")

top_engagement_category = engagement_by_category.iloc[-1]
top_follower_category = followers_by_category.iloc[-1]
engagement_insight, followers_insight, model_insight = st.columns(
    [1, 1, 1.2],
    gap="medium",
)
with engagement_insight:
    st.metric(
        "Top engagement niche",
        str(top_engagement_category["Main video category"]),
        f"{top_engagement_category['Engagement %']:.2f}% avg engagement",
    )
with followers_insight:
    st.metric(
        "Largest audience niche",
        str(top_follower_category["Main video category"]),
        f"{top_follower_category['Followers']:,.0f} avg followers",
    )
with model_insight:
    if model_score is not None:
        st.metric(
            "Model fit (R²)",
            f"{model_score:.2f}",
            help=(
                "Holdout score from the random forest engagement model; "
                "scores can vary with the selected categories."
            ),
        )
    else:
        st.info("Select at least five creators to calculate the model fit.")
