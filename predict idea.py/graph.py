import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Viral Analytics",
    page_icon="📈",
    layout="wide"
)


st.title("📈 Viral Analytics")


followers = 100000
likes = 5000
comments = 300
views = 50000
boost = 65

viral_score = 72.5

st.subheader("🎯 Viral Score")


gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=viral_score,
        title={
            "text": "Viral Score"
        },
        gauge={
            "axis": {
                "range": [0, 100]
            },

            "bar": {
                "color": "red"
            },

            "steps": [

                {
                    "range": [0, 40],
                    "color": "lightgray"
                },

                {
                    "range": [40, 70],
                    "color": "orange"
                },

                {
                    "range": [70, 100],
                    "color": "green"
                }

            ]
        }
    )
)


st.plotly_chart(
    gauge,
    use_container_width=True
)



metrics = pd.DataFrame({

    "Metric": [
        "Followers",
        "Likes",
        "Comments",
        "Views",
        "Boost"
    ],

    "Value": [
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


st.plotly_chart(
    fig,
    use_container_width=True
)



importance = pd.DataFrame({

    "Feature": [
        "Followers",
        "Likes",
        "Comments",
        "Views",
        "Boost_Index"
    ],

    "Importance": [
        0.20,
        0.25,
        0.15,
        0.25,
        0.15
    ]
})


fig2 = px.pie(
    importance,
    values="Importance",
    names="Feature",
    title="Feature Importance"
)


st.plotly_chart(
    fig2,
    use_container_width=True
)
