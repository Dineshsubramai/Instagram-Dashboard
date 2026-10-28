import streamlit as st


st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Insights")


with st.form("insights_form"):
    likes = st.number_input("Likes", min_value=0, value=0)
    comments = st.number_input("Comments", min_value=0, value=0)
    followers = st.number_input("Followers", min_value=1, value=1)
    viral_score = st.slider("Viral Score", min_value=0, max_value=100, value=0)
    submitted = st.form_submit_button("Analyze")


if submitted:
    engagement_rate = (
        (likes + comments)
        / max(followers, 1)
    ) * 100

    st.write(
        f"Engagement Rate: "
        f"**{engagement_rate:.2f}%**"
    )

    if viral_score > 75:
        st.success(
            f"""
            ✅ High Viral Potential

            Engagement Rate:
            {engagement_rate:.2f}%

            Strong interaction levels.

            Audience responds actively.

            Great chance of content spreading.
            """
        )

    elif viral_score > 50:
        st.warning(
            f"""
            ⚡ Moderate Viral Potential

            Engagement Rate:
            {engagement_rate:.2f}%

            Improve posting timing.

            Increase audience interaction.

            Use trending content.
            """
        )

    else:
        st.error(
            f"""
            ❌ Low Viral Potential

            Engagement Rate:
            {engagement_rate:.2f}%

            Focus on:

            • Better content quality

            • More engagement

            • Trending hashtags

            • Collaborations
            """
        )
else:
    st.info("Enter your Instagram stats to analyze engagement and viral potential.")
