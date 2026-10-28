
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pandas as pd
import streamlit as st
import plotly.express as px


st.subheader("🤖 Machine Learning Analysis")


ml_df = globals().get("filtered_df", pd.DataFrame()).copy()

features = ml_df[
    [
        "Followers",
        "Likes Avg.",
        "Comments Avg."
    ]
].fillna(0)

target = ml_df[
    "Engagement Rate"
].fillna(0)

if len(ml_df) >= 5:
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
        "ML R² Score",
        f"{score:.2f}"
    )

    feature_importance = pd.DataFrame(
        {
            "Feature": features.columns,
            "Importance": model.feature_importances_
        }
    )

    fig_ml = px.bar(
        feature_importance,
        x="Feature",
        y="Importance",
        color="Importance",
        title="Feature Importance for Engagement Prediction"
    )

    st.plotly_chart(
        fig_ml,
        use_container_width=True
    )

else:
    st.warning("Not enough data available for Machine Learning.")
