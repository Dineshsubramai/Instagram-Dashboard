import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score


st.set_page_config(
    page_title="Instagram AI Analytics",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

.main {
    background-color: #f8f9fc;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.dashboard-title {
    font-size: 42px;
    font-weight: 800;
    color: #833AB4;
    text-align: center;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    text-align: center;
    color: #666;
    font-size: 18px;
    margin-bottom: 30px;
}

.kpi-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
    text-align: center;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #333;
    margin-top: 20px;
}

.info-box {
    background: linear-gradient(135deg, #833AB4, #E1306C);
    padding: 20px;
    border-radius: 15px;
    color: white;
}

</style>
""", unsafe_allow_html=True)

FILE_PATH = r"C:\Users\Kaar User\Desktop\New folder\Instagram Analytics\archive (1)\top_200_instagrammers.csv"


@st.cache_data
def load_data():

    df = pd.read_csv(FILE_PATH)

    required_columns = [
        "Main topic",
        "Main video category",
        "Followers",
        "Engagement Rate",
        "Likes Avg.",
        "Comments Avg."
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        st.error(
            f"Missing columns in CSV file: {missing_columns}"
        )
        st.stop()

    df = df[required_columns].copy()

    df["Main topic"] = df["Main topic"].fillna("Unknown")
    df["Main video category"] = df["Main video category"].fillna("Unknown")

    numeric_columns = [
        "Followers",
        "Engagement Rate",
        "Likes Avg.",
        "Comments Avg."
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    df[numeric_columns] = df[numeric_columns].fillna(0)

    return df


df = load_data()

st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png",
    width=80
)

st.sidebar.title("📸 Instagram AI")

st.sidebar.markdown(
    "### Dashboard Controls"
)

st.sidebar.divider()

categories = sorted(
    df["Main video category"].unique().tolist()
)

selected_category = st.sidebar.multiselect(
    "🎬 Select Video Category",
    categories,
    default=categories
)

filtered_df = df[
    df["Main video category"].isin(selected_category)
].copy()


st.markdown(
    '<div class="dashboard-title">📸 Instagram AI Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Analyze influencer performance, categories, engagement and viral potential using Machine Learning'
    '</div>',
    unsafe_allow_html=True
)
if len(filtered_df) > 0:

    total_influencers = len(filtered_df)

    avg_followers = filtered_df["Followers"].mean()

    avg_engagement = filtered_df["Engagement Rate"].mean()

    total_categories = (
        filtered_df["Main video category"]
        .nunique()
    )

else:

    total_influencers = 0
    avg_followers = 0
    avg_engagement = 0
    total_categories = 0


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "👥 Total Influencers",
        f"{total_influencers:,}"
    )


with col2:

    st.metric(
        "👤 Avg Followers",
        f"{avg_followers:,.0f}"
    )


with col3:

    st.metric(
        "🔥 Avg Engagement",
        f"{avg_engagement * 100:.2f}%"
    )


with col4:

    st.metric(
        "🎬 Categories",
        f"{total_categories}"
    )


st.divider()


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Category Analytics",
        "🚀 Viral Predictor",
        "🤖 ML Analysis",
        "📋 Dataset"
    ]
)

with tab1:

    st.markdown(
        '<div class="section-title">📊 Instagram Category Analytics</div>',
        unsafe_allow_html=True
    )

    if len(filtered_df) == 0:

        st.warning(
            "Please select at least one category."
        )

    else:
        st.subheader("🥧 Category Distribution")

        category_count = (
            filtered_df[
                "Main video category"
            ]
            .value_counts()
            .reset_index()
        )

        category_count.columns = [
            "Category",
            "Count"
        ]

        fig_pie = px.pie(
            category_count,
            names="Category",
            values="Count",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Bold
        )

        fig_pie.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

        st.subheader(
            "👥 Average Followers by Category"
        )

        followers_cat = (
            filtered_df
            .groupby("Main video category")["Followers"]
            .mean()
            .reset_index()
            .sort_values(
                by="Followers",
                ascending=False
            )
        )

        fig_followers = px.bar(
            followers_cat,
            x="Main video category",
            y="Followers",
            color="Followers",
            text_auto=".2s",
            color_continuous_scale="Viridis"
        )

        fig_followers.update_layout(
            xaxis_title="Video Category",
            yaxis_title="Average Followers"
        )

        st.plotly_chart(
            fig_followers,
            use_container_width=True
        )

        st.subheader(
            "🔥 Average Engagement Rate by Category"
        )

        engagement_cat = (
            filtered_df
            .groupby("Main video category")[
                "Engagement Rate"
            ]
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

        fig_engage.update_layout(
            xaxis_title="Video Category",
            yaxis_title="Average Engagement (%)"
        )

        st.plotly_chart(
            fig_engage,
            use_container_width=True
        )

        st.subheader("🏆 Category Insights")

        best_engagement_category = (
            engagement_cat.iloc[0][
                "Main video category"
            ]
        )

        best_engagement_value = (
            engagement_cat.iloc[0][
                "Engagement %"
            ]
        )

        top_follower_category = (
            followers_cat.iloc[0][
                "Main video category"
            ]
        )

        top_follower_value = (
            followers_cat.iloc[0]["Followers"]
        )


        insight1, insight2 = st.columns(2)


        with insight1:

            st.success(
                f"""
                ### 🔥 Highest Engagement

                **{best_engagement_category}**

                Average Engagement:

                **{best_engagement_value:.2f}%**
                """
            )


        with insight2:

            st.info(
                f"""
                ### 👥 Highest Average Followers

                **{top_follower_category}**

                Average Followers:

                **{top_follower_value:,.0f}**
                """
            )


with tab2:

    st.markdown(
        '<div class="section-title">🚀 Viral Influencer Predictor</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Enter influencer metrics below to estimate a viral-performance score."
    )

    input_col1, input_col2 = st.columns(2)


    with input_col1:

        followers = st.number_input(
            "👥 Followers",
            min_value=0,
            value=100000,
            step=1000
        )

        likes = st.number_input(
            "❤️ Average Likes",
            min_value=0,
            value=5000,
            step=100
        )

        comments = st.number_input(
            "💬 Average Comments",
            min_value=0,
            value=300,
            step=10
        )


    with input_col2:

        views = st.number_input(
            "👁 Average Views",
            min_value=0,
            value=50000,
            step=1000
        )

        boost = st.slider(
            "🚀 Boost Index",
            min_value=0,
            max_value=100,
            value=65
        )

    training_data = pd.DataFrame({

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


    X = training_data.drop(
        "Viral",
        axis=1
    )

    y = training_data["Viral"]


    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )


    viral_model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    viral_model.fit(
        X_train,
        y_train
    )


    viral_prediction = viral_model.predict(
        pd.DataFrame({
            "Followers": [followers],
            "Likes": [likes],
            "Comments": [comments],
            "Views": [views],
            "Boost_Index": [boost]
        })
    )[0]


    viral_probability = viral_model.predict_proba(
        pd.DataFrame({
            "Followers": [followers],
            "Likes": [likes],
            "Comments": [comments],
            "Views": [views],
            "Boost_Index": [boost]
        })
    )[0][1]


    viral_score = round(
        viral_probability * 100,
        2
    )
    accuracy = accuracy_score(
        y_test,
        viral_model.predict(X_test)
    )

    st.divider()

    p1, p2, p3 = st.columns(3)


    with p1:

        st.metric(
            "🤖 Model Accuracy",
            f"{accuracy * 100:.1f}%"
        )


    with p2:

        st.metric(
            "🚀 Viral Score",
            f"{viral_score:.2f}%"
        )


    with p3:

        if viral_prediction == 1:

            st.success(
                "🔥 High Viral Potential"
            )

        else:

            st.warning(
                "⚠️ Lower Viral Potential"
            )
    st.subheader("🎯 Viral Score Gauge")
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
                    "color": "#E1306C"
                },

                "steps": [
                    {
                        "range": [0, 40],
                        "color": "#eeeeee"
                    },

                    {
                        "range": [40, 70],
                        "color": "#ffd166"
                    },

                    {
                        "range": [70, 100],
                        "color": "#06d6a0"
                    }
                ]
            }
        )
    )


    gauge.update_layout(
        height=400
    )


    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    st.subheader(
        "📊 Influencer Input Analysis"
    )


    col4, col5 = st.columns(2)


    with col4:

        metrics = pd.DataFrame({

            "Metric": [
                "Followers",
                "Likes",
                "Comments",
                "Views",
                "Boost Index"
            ],

            "Value": [
                followers,
                likes,
                comments,
                views,
                boost
            ]
        })


        fig_metrics = px.bar(
            metrics,
            x="Metric",
            y="Value",
            color="Metric",
            title="Input Metrics Overview"
        )


        st.plotly_chart(
            fig_metrics,
            use_container_width=True
        )


    with col5:

        importance = pd.DataFrame({

            "Feature": X.columns,

            "Importance":
                viral_model.feature_importances_
        })


        fig_importance = px.pie(
            importance,
            values="Importance",
            names="Feature",
            title="Viral Prediction Feature Importance"
        )


        st.plotly_chart(
            fig_importance,
            use_container_width=True
        )

    engagement_rate = (
        (likes + comments)
        / max(followers, 1)
    ) * 100
    st.subheader("🤖 AI Insights")


    if viral_score >= 75:

        st.success(
            f"""
            ### 🔥 High Viral Potential

            **Engagement Rate:** {engagement_rate:.2f}%

            The entered metrics produce a high model-estimated
            viral score.

            Focus on maintaining strong audience interaction
            and consistent content performance.
            """
        )
    elif viral_score >= 50:

        st.warning(
            f"""
            ### ⚡ Moderate Viral Potential

            **Engagement Rate:** {engagement_rate:.2f}%

            The model-estimated viral score is in the
            moderate range.

            Improving audience interaction and content
            consistency may improve the input metrics.
            """
        )
    else:

        st.error(
            f"""
            ### 📉 Lower Viral Potential

            **Engagement Rate:** {engagement_rate:.2f}%

            The current input metrics produce a lower
            model-estimated viral score.

            Consider improving likes, comments, views
            and audience interaction.
            """
        )
    st.subheader("💡 AI Recommendations")


    recommendations = []


    if engagement_rate < 5:

        recommendations.append(
            "Increase audience engagement through interactive content."
        )
    if likes < followers * 0.05:

        recommendations.append(
            "Work on increasing average likes relative to follower count."
        )
    if comments < likes * 0.05:

        recommendations.append(
            "Encourage comments using questions, polls and discussions."
        )
    if views < followers * 0.5:

        recommendations.append(
            "Improve content reach and discoverability."
        )
    if boost < 70:

        recommendations.append(
            "Increase the Boost Index through consistent content activity."
        )
    if len(recommendations) == 0:

        recommendations.append(
            "Current input metrics meet all basic recommendation checks."
        )


    for recommendation in recommendations:

        st.write(
            "✅",
            recommendation
        )

with tab3:
    st.markdown(
        '<div class="section-title">🤖 Machine Learning Analysis</div>',
        unsafe_allow_html=True
    )
    if len(filtered_df) < 5:

        st.warning(
            "Not enough filtered records for reliable ML training."
        )
    else:

        ml_df = filtered_df.copy()
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
        X_train, X_test, y_train, y_test = train_test_split(
            features,
            target,
            test_size=0.2,
            random_state=42
        )
        engagement_model = RandomForestRegressor(
            n_estimators=200,
            random_state=42
        )
        engagement_model.fit(
            X_train,
            y_train
        )
        predictions = engagement_model.predict(
            X_test
        )
        score = r2_score(
            y_test,
            predictions
        )

        ml1, ml2, ml3 = st.columns(3)
        with ml1:
            st.metric(
                "R² Score",
                f"{score:.2f}"
            )
        with ml2:

            st.metric(
                "Training Records",
                f"{len(X_train):,}"
            )
        with ml3:

            st.metric(
                "Testing Records",
                f"{len(X_test):,}"
            )
        st.subheader(
            "🧠 Engagement Prediction Feature Importance"
        )
        feature_importance = pd.DataFrame({

            "Feature": features.columns,

            "Importance":
                engagement_model.feature_importances_
        })
        feature_importance = feature_importance.sort_values(
            by="Importance",
            ascending=False
        )
        fig_ml = px.bar(
            feature_importance,
            x="Feature",
            y="Importance",
            color="Importance",
            text_auto=".3f",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(
            fig_ml,
            use_container_width=True
        )

        st.subheader(
            "📈 Actual vs Predicted Engagement"
        )
        comparison = pd.DataFrame({

            "Actual": y_test.values,

            "Predicted": predictions
        })
        fig_prediction = px.scatter(
            comparison,
            x="Actual",
            y="Predicted",
            title="Actual vs Predicted Engagement Rate"
        )
        fig_prediction.add_shape(
            type="line",
            x0=comparison["Actual"].min(),
            y0=comparison["Actual"].min(),
            x1=comparison["Actual"].max(),
            y1=comparison["Actual"].max(),
            line=dict(
                color="red",
                dash="dash"
            )
        )
        st.plotly_chart(
            fig_prediction,
            use_container_width=True
        )
        st.info(
            """
            **R² Score explanation:** R² measures how much of the
            variation in the target variable is explained by the model.
            A value closer to 1 generally indicates a better fit.
            """
        )
with tab4:
    st.markdown(
        '<div class="section-title">📋 Instagram Dataset</div>',
        unsafe_allow_html=True
    )
    st.write(
        f"Showing **{len(filtered_df):,}** filtered records."
    )
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=500
    )
    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Dataset",
        data=csv,
        file_name="instagram_filtered_data.csv",
        mime="text/csv"
    )
st.divider()
st.markdown(
    """
    <div style="text-align:center;color:#777;padding:20px">

    📸 <b>Instagram AI Analytics Dashboard</b><br>
    Category Analytics • Viral Prediction • Machine Learning • AI Insights
  </div>
    """,
    unsafe_allow_html=True
)