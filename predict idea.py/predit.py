import streamlit as st
import pandas as pd

from sklearn.ensemble import RandomForestClassifier


st.set_page_config(
    page_title="Viral Prediction",
    page_icon="🚀",
    layout="wide"
)


st.title("🚀 Viral Prediction")


data = pd.DataFrame({

    "Followers": [
        10000,
        50000,
        80000,
        150000,
        300000,
        500000,
        700000,
        1000000
    ],

    "Likes": [
        500,
        4000,
        7000,
        15000,
        25000,
        42000,
        65000,
        100000
    ],

    "Comments": [
        30,
        200,
        350,
        700,
        1200,
        1800,
        2500,
        5000
    ],

    "Views": [
        5000,
        30000,
        60000,
        120000,
        250000,
        450000,
        700000,
        1500000
    ],

    "Boost_Index": [
        45,
        52,
        60,
        70,
        78,
        85,
        90,
        95
    ],

    "Viral": [
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1
    ]
})


X = data.drop(
    "Viral",
    axis=1
)

y = data["Viral"]


model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


model.fit(
    X,
    y
)


followers = st.number_input(
    "Followers",
    min_value=0,
    value=100000
)

likes = st.number_input(
    "Average Likes",
    min_value=0,
    value=5000
)

comments = st.number_input(
    "Average Comments",
    min_value=0,
    value=300
)

views = st.number_input(
    "Average Views",
    min_value=0,
    value=50000
)

boost = st.slider(
    "Boost Index",
    0,
    100,
    65
)
input_data = pd.DataFrame({

    "Followers": [followers],
    "Likes": [likes],
    "Comments": [comments],
    "Views": [views],
    "Boost_Index": [boost]

})




prediction = model.predict(
    input_data
)[0]


probability = model.predict_proba(
    input_data
)[0][1]


viral_score = round(
    probability * 100,
    2
)


st.metric(
    "Viral Score",
    f"{viral_score}%"
)


if prediction == 1:

    st.success(
        "🔥 Will Go Viral"
    )

else:

    st.error(
        "❌ Not Viral"
    )