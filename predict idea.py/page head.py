
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


st.set_page_config(
    page_title="Viral Influencer Predictor",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Viral Influencer Predictor")

st.write(
    "Welcome to the AI-Powered Viral Influencer Prediction Dashboard."
)

st.success("Streamlit is working successfully!")
