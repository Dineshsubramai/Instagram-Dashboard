import streamlit as st


st.set_page_config(
    page_title="AI Recommendations",
    page_icon="💡",
    layout="wide"
)


st.title("💡 AI Recommendations")

followers = 100000
likes = 5000
comments = 300
boost = 65

engagement_rate = (
    (likes + comments)
    / max(followers, 1)
) * 100

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
        "Excellent performance. "
        "Continue current strategy."
    )
for recommendation in recommendations:

    st.write(
        "✅",
        recommendation
    )
