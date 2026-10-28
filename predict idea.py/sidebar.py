
import streamlit as st


st.set_page_config(
    page_title="Influencer Inputs",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Influencer Metrics")




st.sidebar.header(
    "📊 Influencer Metrics"
)


followers = st.sidebar.number_input(
    "Followers",
    min_value=0,
    value=100000
)


likes = st.sidebar.number_input(
    "Average Likes",
    min_value=0,
    value=5000
)


comments = st.sidebar.number_input(
    "Average Comments",
    min_value=0,
    value=300
)


views = st.sidebar.number_input(
    "Average Views",
    min_value=0,
    value=50000
)


boost = st.sidebar.slider(
    "Boost Index",
    min_value=0,
    max_value=100,
    value=65
)



st.write("### Selected Influencer Metrics")

st.write(
    "Followers:",
    followers
)

st.write(
    "Average Likes:",
    likes
)

st.write(
    "Average Comments:",
    comments
)

st.write(
    "Average Views:",
    views
)

st.write(
    "Boost Index:",
    boost
)
