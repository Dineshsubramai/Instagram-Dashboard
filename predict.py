import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ----------------------------------
# Dashboard Config
# ----------------------------------

st.set_page_config(
    page_title="Viral Influencer Predictor",
    page_icon="🚀",
    layout="wide"
)

# ----------------------------------
# Sample Training Data
# ----------------------------------
df = pd.read_csv(r"C:\Users\Kaar User\Desktop\New folder\Instagram Analytics\archive (1)\top_200_instagrammers.csv")
data = pd.DataFrame({
    "Followers":[10000,50000,80000,150000,300000,500000,700000,1000000],
    "Likes":[500,4000,7000,15000,25000,42000,65000,100000],
    "Comments":[30,200,350,700,1200,1800,2500,5000],
    "Views":[5000,30000,60000,120000,250000,450000,700000,1500000],
    "Boost_Index":[45,52,60,70,78,85,90,95],
    "Viral":[0,0,0,1,1,1,1,1]
})

# ----------------------------------
# ML Training
# ----------------------------------

X = data.drop("Viral", axis=1)
y = data["Viral"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

accuracy = accuracy_score(
    y_test,
    model.predict(X_test)
)

# ----------------------------------
# Sidebar Inputs
# ----------------------------------

st.sidebar.header("📊 Influencer Metrics")

followers = st.sidebar.number_input(
    "Followers",
    value=100000
)

likes = st.sidebar.number_input(
    "Average Likes",
    value=5000
)

comments = st.sidebar.number_input(
    "Average Comments",
    value=300
)

views = st.sidebar.number_input(
    "Average Views",
    value=50000
)

boost = st.sidebar.slider(
    "Boost Index",
    0,
    100,
    65
)

# ----------------------------------
# Title
# ----------------------------------

st.title("🚀 Viral Influencer Predictor")

st.markdown(
    """
    Predict influencer virality using Machine Learning
    """
)

# ----------------------------------
# Prediction
# ----------------------------------

input_data = pd.DataFrame({
    "Followers":[followers],
    "Likes":[likes],
    "Comments":[comments],
    "Views":[views],
    "Boost_Index":[boost]
})

prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0][1]

viral_score = round(probability * 100, 2)

# ----------------------------------
# KPI Cards
# ----------------------------------

col1,col2,col3 = st.columns(3)

with col1:
    st.metric(
        "Model Accuracy",
        f"{accuracy*100:.1f}%"
    )

with col2:
    st.metric(
        "Viral Score",
        f"{viral_score}%"
    )

with col3:
    if prediction == 1:
        st.success("🔥 Will Go Viral")
    else:
        st.error("❌ Not Viral")

# ----------------------------------
# Viral Gauge Chart
# ----------------------------------

gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=viral_score,
    title={'text':"Viral Score"},
    gauge={
        'axis': {'range':[0,100]},
        'bar':{'color':'red'},
        'steps':[
            {'range':[0,40],'color':"lightgray"},
            {'range':[40,70],'color':"orange"},
            {'range':[70,100],'color':"green"},
        ]
    }
))

st.plotly_chart(
    gauge,
    use_container_width=True
)

# ----------------------------------
# Input Analysis
# ----------------------------------

col4,col5 = st.columns(2)

with col4:

    metrics = pd.DataFrame({
        "Metric":[
            "Followers",
            "Likes",
            "Comments",
            "Views",
            "Boost"
        ],
        "Value":[
            followers,
            likes,
            comments,
            views,
            boost
        ]
    })

    fig = px.bar(
        metrics,
        x="Metric",
        y="Value",
        color="Metric",
        title="Input Metrics Overview"
    )

    st.plotly_chart(fig, use_container_width=True)


with col5:

    importance = pd.DataFrame({
        "Feature":X.columns,
        "Importance":model.feature_importances_
    })

    fig2 = px.pie(
        importance,
        values="Importance",
        names="Feature",
        title="Feature Importance"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------
# AI Insights
# ----------------------------------

st.subheader("🤖 AI Insights")

engagement_rate = (
    (likes + comments) /
    max(followers,1)
) * 100

if viral_score > 75:
    st.success(
        f"""
        ✅ High Viral Potential

        Engagement Rate: {engagement_rate:.2f}%

        Strong interaction levels.
        Audience responds actively.
        Great chance of content spreading.
        """
    )

elif viral_score > 50:
    st.warning(
        f"""
        ⚡ Moderate Viral Potential

        Engagement Rate: {engagement_rate:.2f}%

        Improve posting timing.
        Increase audience interaction.
        Use trending content.
        """
    )

else:
    st.error(
        f"""
        ❌ Low Viral Potential

        Engagement Rate: {engagement_rate:.2f}%

        Focus on:
        • Better content quality
        • More engagement
        • Trending hashtags
        • Collaborations
        """
    )

# ----------------------------------
# Recommendation Engine
# ----------------------------------

st.subheader("💡 AI Recommendations")

recommendations = []

if engagement_rate < 5:
    recommendations.append(
        "Increase engagement rate above 5%"
    )

if likes < followers * 0.1:
    recommendations.append(
        "Boost average likes through interactive posts"
    )

if comments < likes * 0.1:
    recommendations.append(
        "Encourage comments with polls and questions"
    )

if boost < 70:
    recommendations.append(
        "Improve Boost Index with consistent posting"
    )

if len(recommendations) == 0:
    recommendations.append(
        "Excellent performance. Continue current strategy."
    )

for r in recommendations:
    st.write("✅", r)

# ----------------------------------
# Footer
# ----------------------------------

st.markdown("---")
st.caption("AI-Powered Viral Influencer Prediction Dashboard")
