
import streamlit as st
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


st.set_page_config(
    page_title="ML Training",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 Random Forest Model Training")


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




X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)



model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


model.fit(
    X_train,
    y_train
)




predictions = model.predict(X_test)


accuracy = accuracy_score(
    y_test,
    predictions
)


st.metric(
    "Model Accuracy",
    f"{accuracy * 100:.1f}%"
)


st.success(
    "Random Forest model trained successfully!"
)
