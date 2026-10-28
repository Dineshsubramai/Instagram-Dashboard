
import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Training Data",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Viral Influencer Training Data")



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


st.subheader("Training Dataset")

st.dataframe(
    data,
    use_container_width=True
)


st.write(
    "Number of records:",
    len(data)
)

st.write(
    "Number of columns:",
    len(data.columns)
)
