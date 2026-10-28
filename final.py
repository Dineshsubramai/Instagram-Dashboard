"""Instagram creator analytics dashboard.

Run with: streamlit run final.py
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image, ImageDraw


def make_instagram_icon():
    """Create a small gradient Instagram-style camera icon for the browser tab."""
    image = Image.new("RGB", (128, 128), "#C13584")
    pixels = image.load()

    for y in range(128):
        for x in range(128):
            blend = (x + y) / 256
            pixels[x, y] = (
                int(131 + (245 - 131) * blend),
                int(58 + (96 - 58) * blend),
                int(180 + (64 - 180) * blend),
            )

    drawing = ImageDraw.Draw(image)
    drawing.rounded_rectangle(
        (25, 25, 103, 103),
        radius=22,
        outline="white",
        width=9,
    )
    drawing.ellipse((44, 44, 84, 84), outline="white", width=8)
    drawing.ellipse((80, 36, 93, 49), fill="white")
    return image


st.set_page_config(
    page_title="Instagram Analytics",
    page_icon=make_instagram_icon(),
    layout="wide",
    initial_sidebar_state="expanded",
)


BACKGROUND = "#f4f5f9"
INK = "#28263c"
MUTED = "#77788a"
PURPLE = "#7b4df5"
CHART_COLORS = [
    "#8a55f5",
    "#3989f4",
    "#ff646b",
    "#ff9a55",
    "#32b88a",
    "#4ec5e8",
    "#f5bd45",
]

st.markdown(
f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], .stApp {{
    background: {BACKGROUND};
    color: {INK};
    font-family: 'DM Sans', sans-serif;
}}
[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ max-width: 1600px; padding: 1.4rem 2rem 2.2rem; }}
#MainMenu, footer {{ visibility: hidden; }}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #8a4cf3, #684df3);
    border: 0;
    min-width: 235px;
}}
[data-testid="stSidebar"] * {{ color: white; }}
[data-testid="stSidebar"] input {{ color: #28263c !important; }}

h1, h2, h3, h4 {{ color: {INK} !important; letter-spacing: -0.025em; }}
.topbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0 0 18px;
}}
.brandmark {{
    width: 39px;
    height: 39px;
    border-radius: 12px;
    background: linear-gradient(135deg, #833ab4 0%, #e1306c 52%, #fcb045 100%);
    display: inline-block;
    vertical-align: middle;
    position: relative;
    box-shadow: 0 5px 14px rgba(193, 53, 132, 0.24);
}}
.brandmark:before {{
    content: "";
    position: absolute;
    width: 19px;
    height: 19px;
    border: 2.5px solid white;
    border-radius: 6px;
    left: 8px;
    top: 8px;
}}
.brandmark:after {{
    content: "";
    position: absolute;
    width: 6px;
    height: 6px;
    border: 2px solid white;
    border-radius: 50%;
    left: 14px;
    top: 14px;
    box-shadow: 8px -7px 0 -1px white;
}}
.brandname {{
    font-size: 20px;
    font-weight: 800;
    margin-left: 12px;
    vertical-align: middle;
    color: {INK};
    letter-spacing: -0.035em;
}}
.sidebrand {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 17px;
    line-height: 1.1;
    margin: 4px 0 18px;
}}
.sidebrand .brandmark {{ width: 34px; height: 34px; min-width: 34px; }}
.eyebrow {{
    color: {PURPLE};
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}}
.page-title {{
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -0.045em;
    background: linear-gradient(90deg, #29263b 0%, #7046dc 68%, #d94f91 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    margin: 3px 0;
}}
.caption {{ font-size: 13px; color: {MUTED}; }}
.card {{
    background: white;
    border-radius: 15px;
    padding: 17px 20px;
    box-shadow: 0 8px 24px rgba(40, 42, 70, 0.055);
    height: 100%;
    border: 1px solid rgba(230, 231, 239, 0.65);
}}
.kpi {{
    border-radius: 16px;
    padding: 19px 22px;
    color: white;
    min-height: 112px;
    box-shadow: 0 10px 22px rgba(67, 62, 110, 0.13);
}}
.kpi-label {{ font-size: 13px; opacity: 0.92; }}
.kpi-value {{ font-size: 27px; font-weight: 800; margin-top: 5px; }}
.kpi-note {{ font-size: 11px; opacity: 0.85; }}
.card-title {{ font-size: 15px; font-weight: 800; color: {INK}; margin-bottom: 3px; }}
.card-caption {{ font-size: 11px; color: {MUTED}; margin-bottom: 9px; }}
[data-testid="stPlotlyChart"] {{ background: transparent; }}
[data-testid="stMetric"] {{
    background: #fff;
    border-radius: 13px;
    padding: 12px 15px;
    box-shadow: 0 5px 18px rgba(40, 42, 70, 0.05);
}}
[data-testid="stMetricLabel"] {{ color: {MUTED}; }}
[data-testid="stMetricValue"] {{ color: {INK}; }}
[data-baseweb="tab-list"] {{ gap: 18px; background: transparent; }}
button[data-baseweb="tab"] {{ color: {MUTED}; font-weight: 700; }}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {PURPLE};
    border-bottom-color: {PURPLE};
}}
.stButton > button {{
    background: {PURPLE};
    color: white;
    border: 0;
    border-radius: 9px;
    font-weight: 700;
}}
[data-testid="stDataFrame"] {{ border-radius: 12px; overflow: hidden; }}
hr {{ border-color: #ececf2; }}
</style>
""",
    unsafe_allow_html=True,
)


REQUIRED_COLUMNS = [
    "Username",
    "Main topic",
    "Main video category",
    "Followers",
    "Engagement Rate",
    "Likes Avg.",
    "Comments Avg.",
    "Views Avg.",
    "Posts",
    "Boost Index",
]
TEXT_COLUMNS = ["Username", "Main topic", "Main video category", "Country", "Channel Name", "Url"]
NUMERIC_COLUMNS = [
    "Followers",
    "Engagement Rate",
    "Likes",
    "Likes Avg.",
    "Comments Avg.",
    "Views Avg.",
    "Posts",
    "Boost Index",
    "Avg. 1 Day",
    "Avg. 3 Day",
    "Avg. 7 Day",
    "Avg. 14 Day",
    "Avg. 30 Day",
    "Engagement Rate (60 Days)",
]
CORE_METRIC_COLUMNS = [
    "Followers",
    "Engagement Rate",
    "Likes Avg.",
    "Comments Avg.",
    "Views Avg.",
    "Posts",
    "Boost Index",
]


def find_csv():
    """Find the bundled creator CSV in the project folders."""
    project_root = Path(__file__).resolve().parent
    possible_paths = [
        project_root / "top_200_instagrammers.csv",
        project_root / "Final OP" / "top_200_instagrammers.csv",
        project_root / "archive (1)" / "top_200_instagrammers.csv",
        project_root / "New folder" / "top_200_instagrammers.csv",
    ]
    return next((path for path in possible_paths if path.exists()), None)


@st.cache_data(show_spinner=False)
def load_csv(source):
    """Read a CSV file and cache the result between Streamlit reruns."""
    return pd.read_csv(source)


with st.sidebar:
    st.markdown(
        '<div class="sidebrand"><span class="brandmark"></span>'
        "<b>Instagram<br>Analytics</b></div>",
        unsafe_allow_html=True,
    )
    st.markdown("### Dashboard filters")
    uploaded_file = st.file_uploader("Upload creator CSV", type=["csv"])
    csv_path = st.text_input("CSV file path", value=str(find_csv() or ""))

    try:
        if uploaded_file is not None:
            raw_data = load_csv(uploaded_file)
        elif csv_path:
            raw_data = load_csv(csv_path)
        else:
            raw_data = None
    except Exception as error:
        raw_data = None
        st.error(f"Unable to open CSV: {error}")

if raw_data is None:
    st.title("Instagram Analytics")
    st.info(
        "Upload a creator CSV or enter its path in the sidebar. "
        "The project CSV is detected automatically when available."
    )
    st.stop()

missing_columns = [
    column for column in REQUIRED_COLUMNS if column not in raw_data.columns
]
if missing_columns:
    st.error("Required CSV columns are missing: " + ", ".join(missing_columns))
    st.stop()

data = raw_data.copy()

for column in TEXT_COLUMNS:
    if column in data.columns:
        data[column] = data[column].fillna("Unknown").astype(str)

for column in NUMERIC_COLUMNS:
    if column in data.columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

for column in CORE_METRIC_COLUMNS:
    data[column] = data[column].fillna(0)

data["Engagement %"] = data["Engagement Rate"] * 100


with st.sidebar:
    category_options = sorted(data["Main video category"].unique().tolist())
    selected_categories = st.multiselect(
        "Creator categories",
        category_options,
        default=category_options,
    )

    if "Country" in data.columns:
        country_options = sorted(
            country
            for country in data["Country"].dropna().unique()
            if country != "Unknown"
        )
        selected_countries = st.multiselect(
            "Countries",
            country_options,
            default=country_options,
        )
    else:
        selected_countries = None

    topic_options = sorted(
        topic for topic in data["Main topic"].dropna().unique() if topic != "Unknown"
    )
    selected_topics = st.multiselect(
        "Main topics",
        topic_options,
        default=topic_options,
    )
    username_search = st.text_input("Search username", placeholder="e.g. cristiano")

filtered_data = data[data["Main video category"].isin(selected_categories)].copy()

if selected_countries is not None:
    included_countries = selected_countries.copy()
    if "Unknown" in data["Country"].values:
        included_countries.append("Unknown")
    filtered_data = filtered_data[filtered_data["Country"].isin(included_countries)]

included_topics = selected_topics.copy()
if "Unknown" in data["Main topic"].values:
    included_topics.append("Unknown")
filtered_data = filtered_data[filtered_data["Main topic"].isin(included_topics)]

if username_search.strip():
    filtered_data = filtered_data[
        filtered_data["Username"].str.contains(
            username_search.strip(),
            case=False,
            na=False,
        )
    ]

if filtered_data.empty:
    st.warning("No creators match the selected filters.")
    st.stop()

with st.sidebar:
    st.markdown("---")
    st.markdown("### At a glance")

    sidebar_category_stats = (
        filtered_data.groupby("Main video category")["Engagement %"]
        .mean()
        .sort_values(ascending=False)
    )
    if not sidebar_category_stats.empty:
        leading_category = sidebar_category_stats.index[0]
        leading_engagement = sidebar_category_stats.iloc[0]
    else:
        leading_category = "No category"
        leading_engagement = 0

    st.markdown(
        f'''<div style="background:rgba(255,255,255,.14);border-radius:12px;padding:12px 14px;margin:8px 0">
        <div style="font-size:11px;opacity:.82">CREATORS IN VIEW</div>
        <div style="font-size:25px;font-weight:800">{len(filtered_data):,}</div>
        <div style="font-size:11px;opacity:.86">{filtered_data["Main video category"].nunique()} categories selected</div>
        </div>''',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"**Top engagement category:** {leading_category} · "
        f"{leading_engagement:.2f}%"
    )
    if "Country" in filtered_data.columns:
        country_count = filtered_data.loc[
            filtered_data["Country"] != "Unknown", "Country"
        ].nunique()
        st.caption(f"Creators from {country_count} countries")
    st.caption("This summary updates when you change the filters above.")

    with st.expander("About these metrics"):
        st.write(
            "Engagement rate is displayed as a percentage. Average likes, comments, "
            "and views are per creator, based on the values in the loaded CSV. "
            "Country, topic, and time-window charts use optional columns when present."
        )


CHART_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {
        "family": "DM Sans, sans-serif",
        "color": "#5d5e70",
        "size": 11,
    },
    "margin": {"l": 8, "r": 8, "t": 20, "b": 8},
    "hoverlabel": {"bgcolor": "white", "font_color": INK},
}


def polish_chart(figure, height=285):
    """Apply shared colors and grid styling to a Plotly chart."""
    figure.update_layout(**CHART_LAYOUT, height=height)
    figure.update_xaxes(
        showgrid=True,
        gridcolor="#ececf2",
        zeroline=False,
        tickfont=dict(color=MUTED),
    )
    figure.update_yaxes(
        showgrid=True,
        gridcolor="#ececf2",
        zeroline=False,
        tickfont=dict(color=MUTED),
    )
    return figure


st.markdown(
    '<div class="topbar"><div><span class="brandmark"></span>'
    '<span class="brandname">Instagram Analytics</span></div>'
    '<div class="caption">CREATOR PERFORMANCE OVERVIEW</div></div>',
    unsafe_allow_html=True,
)

title_column, count_column = st.columns([3, 1])
with title_column:
    st.markdown(
        '<div class="eyebrow">Creator insights</div>'
        '<div class="page-title">Instagram Analytics</div>'
        '<div class="caption">Dashboard overview of creator audience and content performance</div>',
        unsafe_allow_html=True,
    )
with count_column:
    st.markdown(
        f'<div style="text-align:right;padding-top:16px" class="caption">'
        f'{len(filtered_data):,} creators · '
        f'{filtered_data["Main video category"].nunique()} categories</div>',
        unsafe_allow_html=True,
    )
st.write("")

summary_cards = [
    (
        "◉",
        f"{len(filtered_data):,}",
        "Creators analyzed",
        CHART_COLORS[0],
        "Accounts in current view",
    ),
    (
        "◎",
        f"{filtered_data['Followers'].mean():,.0f}",
        "Average followers",
        CHART_COLORS[1],
        "Audience size per account",
    ),
    (
        "♡",
        f"{filtered_data['Engagement %'].mean():.2f}%",
        "Average engagement",
        CHART_COLORS[2],
        "Likes and comments rate",
    ),
    (
        "▣",
        f"{filtered_data['Posts'].mean():,.0f}",
        "Average posts",
        CHART_COLORS[3],
        "Published posts per creator",
    ),
]

summary_columns = st.columns(4, gap="medium")
for column, (symbol, value, label, color, note) in zip(
    summary_columns,
    summary_cards,
):
    with column:
        st.markdown(
            f'<div class="kpi" style="background:linear-gradient(120deg,{color},{color}bb)">'
            f'<div class="kpi-label">{symbol} &nbsp; {label}</div>'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-note">{note}</div></div>',
            unsafe_allow_html=True,
        )
st.write("")


performance_column, category_column = st.columns([1.8, 1], gap="medium")

with performance_column:
    st.markdown(
        '<div class="card"><div class="card-title">Creator performance</div>'
        '<div class="card-caption">Category trends · audience and engagement compared with the filtered average</div>',
        unsafe_allow_html=True,
    )

    category_stats = filtered_data.groupby(
        "Main video category",
        as_index=False,
    ).agg(
        Followers=("Followers", "mean"),
        Engagement=("Engagement %", "mean"),
        Creators=("Username", "count"),
    )
    average_followers = max(filtered_data["Followers"].mean(), 1)
    average_engagement = max(filtered_data["Engagement %"].mean(), 0.0001)
    category_stats["Audience index"] = (
        category_stats["Followers"] / average_followers * 100
    )
    category_stats["Engagement index"] = (
        category_stats["Engagement"] / average_engagement * 100
    )
    category_stats = category_stats.nlargest(8, "Creators")

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=category_stats["Main video category"],
            y=category_stats["Audience index"],
            mode="lines+markers",
            name="Audience index",
            line=dict(color="#ff8c52", width=3, shape="spline"),
            marker=dict(size=8),
        )
    )
    figure.add_trace(
        go.Scatter(
            x=category_stats["Main video category"],
            y=category_stats["Engagement index"],
            mode="lines+markers",
            name="Engagement index",
            line=dict(color="#9052ec", width=3, shape="spline"),
            marker=dict(size=8),
        )
    )
    polish_chart(figure, 285)
    figure.update_layout(
        legend=dict(orientation="h", y=1.15, x=0.3, font=dict(size=10)),
        yaxis_title="Index (average = 100)",
        xaxis_title="",
        margin=dict(l=15, r=12, t=28, b=30),
    )
    st.plotly_chart(figure, use_container_width=True)

    metric_columns = st.columns(4)
    metric_columns[0].metric(
        "Avg. likes",
        f"{filtered_data['Likes Avg.'].mean():,.0f}",
    )
    metric_columns[1].metric(
        "Avg. comments",
        f"{filtered_data['Comments Avg.'].mean():,.0f}",
    )
    metric_columns[2].metric(
        "Avg. views",
        f"{filtered_data['Views Avg.'].mean():,.0f}",
    )
    metric_columns[3].metric(
        "Avg. boost index",
        f"{filtered_data['Boost Index'].mean():.1f}",
    )
    st.markdown('</div>', unsafe_allow_html=True)

with category_column:
    st.markdown(
        '<div class="card"><div class="card-title">Analytics</div>'
        '<div class="card-caption">Creator category mix in the current view</div>',
        unsafe_allow_html=True,
    )

    category_mix = (
        filtered_data["Main video category"]
        .value_counts()
        .head(7)
        .rename_axis("Category")
        .reset_index(name="Creators")
    )
    figure = go.Figure(
        go.Pie(
            labels=category_mix["Category"],
            values=category_mix["Creators"],
            hole=0.65,
            sort=False,
            marker=dict(colors=CHART_COLORS, line=dict(color="white", width=4)),
            textinfo="none",
            hovertemplate="%{label}<br>%{value} creators (%{percent})<extra></extra>",
        )
    )
    figure.update_layout(
        **CHART_LAYOUT,
        height=300,
        showlegend=False,
        annotations=[
            dict(
                text=(
                    f"{len(filtered_data):,}<br>"
                    '<span style="font-size:11px;color:#77788a">creators</span>'
                ),
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=24, color=INK),
            )
        ],
    )
    st.plotly_chart(figure, use_container_width=True)

    legend_rows = category_mix.head(5)
    for start in range(0, len(legend_rows), 2):
        legend_columns = st.columns(2)
        for offset, (_, row) in enumerate(legend_rows.iloc[start : start + 2].iterrows()):
            color = CHART_COLORS[(start + offset) % len(CHART_COLORS)]
            legend_columns[offset].markdown(
                f'<span style="color:{color};font-size:18px">■</span> '
                f'<span style="color:#5d5e70">{row["Category"]}</span> '
                f'<b style="color:{INK}">{int(row["Creators"])}</b>',
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")
activity_column, leaderboard_column = st.columns([0.82, 1.8], gap="medium")

with activity_column:
    st.markdown(
        '<div class="card"><div class="card-title">Top creators</div>'
        '<div class="card-caption">Largest audiences in this selection</div>',
        unsafe_allow_html=True,
    )
    top_creators = filtered_data.nlargest(5, "Followers")

    for _, creator in top_creators.iterrows():
        st.markdown(
            '<div style="display:flex;justify-content:space-between;align-items:center;'
            'border-bottom:1px solid #f0f0f4;padding:10px 0">'
            f'<div><b style="color:{INK}">@{creator["Username"]}</b>'
            f'<div style="color:{MUTED};font-size:11px">'
            f'{creator["Main video category"]} · {creator["Engagement %"]:.2f}% engagement</div></div>'
            f'<b style="color:{PURPLE}">{creator["Followers"] / 1e6:.1f}M</b></div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

with leaderboard_column:
    st.markdown(
        '<div class="card"><div class="card-title">Creator leaderboard</div>'
        '<div class="card-caption">Top accounts by audience size</div>',
        unsafe_allow_html=True,
    )
    leaderboard = filtered_data.nlargest(8, "Followers")[
        [
            "Username",
            "Main video category",
            "Followers",
            "Engagement %",
            "Likes Avg.",
        ]
    ].copy()
    leaderboard["Followers"] = leaderboard["Followers"].map(lambda value: f"{value:,.0f}")
    leaderboard["Engagement %"] = leaderboard["Engagement %"].map(
        lambda value: f"{value:.2f}%"
    )
    leaderboard["Likes Avg."] = leaderboard["Likes Avg."].map(
        lambda value: f"{value:,.0f}"
    )
    leaderboard.columns = [
        "Username",
        "Category",
        "Followers",
        "Engagement",
        "Avg. likes",
    ]
    st.dataframe(leaderboard, use_container_width=True, hide_index=True, height=285)
    st.markdown('</div>', unsafe_allow_html=True)



st.write("")
st.markdown("## Audience, geography & growth")
st.caption(
    "Explore country, topic, total likes, and recent-performance fields from the CSV."
)

growth_column, topic_column = st.columns([1.25, 1], gap="medium")

with growth_column:
    st.markdown(
        '<div class="card"><div class="card-title">Recent average performance</div>'
        '<div class="card-caption">Mean daily views across available rolling windows</div>',
        unsafe_allow_html=True,
    )
    rolling_windows = [
        ("1 day", "Avg. 1 Day"),
        ("3 days", "Avg. 3 Day"),
        ("7 days", "Avg. 7 Day"),
        ("14 days", "Avg. 14 Day"),
        ("30 days", "Avg. 30 Day"),
    ]
    available_windows = [
        (label, column)
        for label, column in rolling_windows
        if column in filtered_data.columns and filtered_data[column].notna().any()
    ]

    if available_windows:
        window_summary = pd.DataFrame(
            {
                "Period": [label for label, _ in available_windows],
                "Average views": [
                    filtered_data[column].mean() for _, column in available_windows
                ],
            }
        )
        figure = px.line(
            window_summary,
            x="Period",
            y="Average views",
            markers=True,
        )
        figure.update_traces(
            line=dict(color="#8a55f5", width=3),
            marker=dict(size=9, color="#ff9a55"),
            fill="tozeroy",
            fillcolor="rgba(138,85,245,.10)",
        )
        polish_chart(figure, 300)
        figure.update_layout(xaxis_title="", yaxis_title="Average views", showlegend=False)
        st.plotly_chart(figure, use_container_width=True)
    else:
        st.info("This CSV does not contain usable rolling-average columns.")
    st.markdown('</div>', unsafe_allow_html=True)

with topic_column:
    st.markdown(
        '<div class="card"><div class="card-title">Topics with strongest engagement</div>'
        '<div class="card-caption">Average current engagement by main topic</div>',
        unsafe_allow_html=True,
    )
    topic_stats = (
        filtered_data[filtered_data["Main topic"] != "Unknown"]
        .groupby("Main topic", as_index=False)
        .agg(
            Engagement=("Engagement %", "mean"),
            Creators=("Username", "count"),
        )
        .nlargest(8, "Engagement")
        .sort_values("Engagement")
    )

    if not topic_stats.empty:
        figure = px.bar(
            topic_stats,
            x="Engagement",
            y="Main topic",
            orientation="h",
            color="Engagement",
            text="Engagement",
            color_continuous_scale=[[0, "#ff9a55"], [1, "#8a55f5"]],
        )
        figure.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            cliponaxis=False,
        )
        polish_chart(figure, 300)
        figure.update_layout(
            coloraxis_showscale=False,
            yaxis_title="",
            xaxis_title="Average engagement (%)",
            margin=dict(l=8, r=50, t=15, b=25),
        )
        st.plotly_chart(figure, use_container_width=True)
    else:
        st.info("Topic labels are not populated for the current creators.")
    st.markdown('</div>', unsafe_allow_html=True)

country_column, comparison_column = st.columns([1, 1.25], gap="medium")

with country_column:
    st.markdown(
        '<div class="card"><div class="card-title">Audience by country</div>'
        '<div class="card-caption">Countries represented in the selected creators</div>',
        unsafe_allow_html=True,
    )

    if "Country" in filtered_data.columns:
        country_stats = (
            filtered_data[filtered_data["Country"] != "Unknown"]
            .groupby("Country", as_index=False)
            .agg(
                Creators=("Username", "count"),
                Followers=("Followers", "mean"),
            )
            .nlargest(10, "Creators")
            .sort_values("Creators")
        )
    else:
        country_stats = pd.DataFrame()

    if not country_stats.empty:
        figure = px.bar(
            country_stats,
            x="Creators",
            y="Country",
            orientation="h",
            color="Followers",
            text="Creators",
            color_continuous_scale=[[0, "#4ec5e8"], [1, "#7b4df5"]],
            hover_data={"Followers": ":,.0f"},
        )
        polish_chart(figure, 320)
        figure.update_layout(
            coloraxis_showscale=False,
            yaxis_title="",
            xaxis_title="Creators",
            margin=dict(l=8, r=15, t=15, b=25),
        )
        st.plotly_chart(figure, use_container_width=True)
    else:
        st.info("No country values are available for this selection.")
    st.markdown('</div>', unsafe_allow_html=True)

with comparison_column:
    st.markdown(
        '<div class="card"><div class="card-title">Engagement: current vs. last 60 days</div>'
        '<div class="card-caption">Creators with both engagement measurements</div>',
        unsafe_allow_html=True,
    )
    sixty_day_column = "Engagement Rate (60 Days)"

    if (
        sixty_day_column in filtered_data.columns
        and filtered_data[sixty_day_column].notna().any()
    ):
        comparison_data = filtered_data.dropna(subset=[sixty_day_column]).copy()
        comparison_data["Engagement 60d %"] = (
            comparison_data[sixty_day_column] * 100
        )
        comparison_data = comparison_data.nlargest(250, "Followers")

        figure = px.scatter(
            comparison_data,
            x="Engagement 60d %",
            y="Engagement %",
            color="Main video category",
            size="Followers",
            hover_name="Username",
            size_max=17,
            color_discrete_sequence=CHART_COLORS,
        )
        polish_chart(figure, 320)
        figure.update_layout(
            xaxis_title="60-day engagement (%)",
            yaxis_title="Current engagement (%)",
            legend=dict(orientation="h", y=1.14, font=dict(size=9)),
        )
        st.plotly_chart(figure, use_container_width=True)
    else:
        st.info("The 60-day engagement field is unavailable for this selection.")
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown("## Creator profile")
profile_options = filtered_data["Username"].sort_values().tolist()
selected_profile_name = st.selectbox(
    "Choose a creator to inspect",
    profile_options,
    key="profile_creator",
)
profile = filtered_data.loc[
    filtered_data["Username"] == selected_profile_name
].iloc[0]
profile_columns = st.columns([1.3, 1, 1, 1, 1])
profile_columns[0].markdown(
    f"**@{selected_profile_name}**  \n\n"
    f"{profile.get('Channel Name', selected_profile_name)}"
)
profile_columns[1].metric("Followers", f"{profile['Followers']:,.0f}")
profile_columns[2].metric("Likes per post", f"{profile['Likes Avg.']:,.0f}")
profile_columns[3].metric("Comments per post", f"{profile['Comments Avg.']:,.0f}")
profile_columns[4].metric("Engagement", f"{profile['Engagement %']:.2f}%")

profile_url = str(profile.get("Url", "Unknown"))
if "Url" in filtered_data.columns and profile_url.startswith("http"):
    st.markdown(
        f"[Open Instagram profile for @{selected_profile_name}]({profile_url})"
    )

with st.expander("Browse and download the full filtered dataset"):
    export_data = filtered_data.drop(columns=["Engagement %"])
    st.dataframe(export_data, use_container_width=True, hide_index=True, height=400)
    st.download_button(
        "Download filtered CSV",
        export_data.to_csv(index=False).encode("utf-8"),
        "instagram_creators_filtered.csv",
        "text/csv",
    )

st.markdown(
    '<div class="caption" style="text-align:center;padding:18px 0 4px">'
    "Instagram Analytics · Values are calculated from the loaded dataset and active filters"
    "</div>",
    unsafe_allow_html=True,
)
