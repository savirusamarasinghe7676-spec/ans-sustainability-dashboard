
# 5DATA004C - Sustainability Dashboard
# Dataset: Adjusted Net Savings including Particulate Emission Damage (% of GNI)
# Source: World Bank | Indicator: NY.ADJ.SVNG.GN.ZS
# Owner: Saviru Samarasinghe 

# Import the necessary libraries 

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set up the page 

st.set_page_config(
    page_title="Global Sustainability Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS — Makes the dashboard look professional

st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a5276;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #5d6d7e;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f4f8;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border-left: 4px solid #1a5276;
    }
    .insight-box {
    background-color: #1a3a5c;
    border-left: 4px solid #2980b9;
    padding: 0.8rem 1rem;
    border-radius: 4px;
    margin: 0.5rem 0;
    color: #ffffff
}
    .warning-box {
    background-color: #3d2e00;
    border-left: 4px solid #f39c12;
    padding: 0.8rem 1rem;
    border-radius: 4px;
    color: #ffffff !important;
}
    </style>
""", unsafe_allow_html=True)

# Data Loading and Preparation

@st.cache_data
def load_data():
    """Load and prepare the World Bank ANS dataset."""
    try:
        df = pd.read_excel(
            "data/ans_data.xls",
            engine="xlrd",
            header=3
        )
    except FileNotFoundError:
        st.error("Dataset file not found. Please ensure 'data/ans_data.xls' exists.")
        st.stop()

    # Keep only useful columns
    year_cols = [c for c in df.columns if str(c).isdigit() and int(c) >= 1990]
    keep_cols = ["Country Name", "Country Code"] + year_cols
    df = df[keep_cols].copy()

    # Remove rows with no country name
    df = df.dropna(subset=["Country Name"])

    # Convert to long format: one row per (country, year)
    df_long = df.melt(
        id_vars=["Country Name", "Country Code"],
        value_vars=year_cols,
        var_name="Year",
        value_name="ANS"
    )
    df_long["Year"] = df_long["Year"].astype(int)

    # Remove rows where ANS value is missing
    df_long = df_long.dropna(subset=["ANS"])

    # Round ANS to 2 decimal places
    df_long["ANS"] = df_long["ANS"].round(2)

    # Add a colour category for styling
    df_long["Status"] = df_long["ANS"].apply(
        lambda x: "Positive (Wealth Building)" if x >= 0 else "Negative (Wealth Depleting)"
    )

    return df_long

# Load the data
df = load_data()

# Sidebar controls 

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Color_icon_green.svg/120px-Color_icon_green.svg.png", width=60)
    st.title("Dashboard Controls")
    st.markdown("---")

    # Year selector
    st.subheader("📅 Select Year")
    available_years = sorted(df["Year"].unique())
    selected_year = st.slider(
        "Year",
        min_value=int(min(available_years)),
        max_value=int(max(available_years)),
        value=2020,
        step=1,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Country selector for time series
    st.subheader("🌍 Countries for Time Series")
    all_countries = sorted(df["Country Name"].unique())
    default_countries = ["United Kingdom", "United States", "China", "India", "Germany", "Singapore"]
    
    valid_defaults = [c for c in default_countries if c in all_countries]
    selected_countries = st.multiselect(
        "Select Countries",
        options=all_countries,
        default=valid_defaults,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # N selector for bar charts
    st.subheader("🔢 Top/Bottom N Countries")
    top_n = st.slider("N countries to show", 5, 20, 10, label_visibility="collapsed")

    st.markdown("---")
    st.caption("📊 Data: World Bank Open Data")
    st.caption("📌 Indicator: NY.ADJ.SVNG.GN.ZS")
    st.caption("🗓️ Coverage: 266 economies, 1990–2021")

# Main Header 

st.markdown('<p class="main-header">🌍 Global Sustainability Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Adjusted Net Savings Including Particulate Emission Damage (% of GNI) — '
    'World Bank | Is the world building or depleting its genuine wealth?</p>',
    unsafe_allow_html=True
)
st.markdown("---")

# Section 1 — KPI Cards

year_data = df[df["Year"] == selected_year].copy()
global_avg = year_data["ANS"].mean()
negative_count = (year_data["ANS"] < 0).sum()
positive_count = (year_data["ANS"] >= 0).sum()
country_count = len(year_data)
negative_pct = (negative_count / country_count * 100) if country_count > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="📅 Selected Year",
        value=str(selected_year)
    )
with col2:
    st.metric(
        label="🌐 Global Average ANS",
        value=f"{global_avg:.2f}%",
        delta=f"vs 0% threshold"
    )
with col3:
    st.metric(
        label="✅ Wealth-Building Nations",
        value=str(positive_count),
        delta=f"{100 - negative_pct:.1f}% of total"
    )
with col4:
    st.metric(
        label="⚠️ Wealth-Depleting Nations",
        value=str(negative_count),
        delta=f"-{negative_pct:.1f}% of total",
        delta_color="inverse"
    )
with col5:
    st.metric(
        label="🗺️ Countries with Data",
        value=str(country_count)
    )

st.markdown("---")

# Section 2 — Choropeth Map (Global ANS Distribution)

st.subheader(f"🗺️ Visualisation 1: Global ANS Distribution — {selected_year}")

fig_map = px.choropleth(
    year_data,
    locations="Country Code",
    color="ANS",
    hover_name="Country Name",
    hover_data={"ANS": ":.2f", "Country Code": False},
    color_continuous_scale="RdYlGn",
    color_continuous_midpoint=0,
    range_color=[-35, 40],
    title=f"Adjusted Net Savings (% of GNI) — {selected_year}",
    labels={"ANS": "ANS (% of GNI)"}
)
fig_map.update_layout(
    height=520,
    margin=dict(l=0, r=0, t=40, b=0),
    coloraxis_colorbar=dict(
        title="ANS % of GNI",
        tickvals=[-30, -20, -10, 0, 10, 20, 30, 40],
        ticktext=["-30%", "-20%", "-10%", "0%", "+10%", "+20%", "+30%", "+40%"]
    ),
    geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth")
)
st.plotly_chart(fig_map, width='stretch')

st.markdown(
    '<div class="insight-box">🔍 <b>Key Insight:</b> Red/orange countries are consuming more '
    'wealth than they are creating — depleting natural resources faster than building human capital. '
    'Green countries are investing in education and clean infrastructure. '
    'Use the year slider to observe how the global picture has changed since 1990.</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# Section 3 — Line Chart (Time Series)

st.subheader("📈 Visualisation 2: ANS Trends Over Time (1990–2021)")

if not selected_countries:
    st.markdown(
        '<div class="warning-box">⚠️ Please select at least one country from the sidebar to display the time series chart.</div>',
        unsafe_allow_html=True
    )
else:
    ts_data = df[
        (df["Country Name"].isin(selected_countries)) &
        (df["Year"] >= 1990) &
        (df["Year"] <= 2021)
    ].copy()

    if ts_data.empty:
        st.warning("No data available for the selected countries in this time range.")
    else:
        fig_line = px.line(
            ts_data,
            x="Year",
            y="ANS",
            color="Country Name",
            title="Adjusted Net Savings Trends by Country (1990–2021)",
            labels={"ANS": "ANS (% of GNI)", "Country Name": "Country"},
            markers=True
        )
        fig_line.add_hline(
            y=0,
            line_dash="dash",
            line_color="red",
            line_width=2,
            annotation_text="Break-Even Threshold (0%)",
            annotation_position="bottom right"
        )
        fig_line.update_layout(
            height=480,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        fig_line.update_traces(line=dict(width=2.5))
        st.plotly_chart(fig_line, width='stretch')

        st.markdown(
            '<div class="insight-box">🔍 <b>Key Insight:</b> Countries that fall below the red dashed line are '
            'depleting their national wealth. The UK dipped close to zero after 2008. China and India show '
            'strong positive trends — consistent investment in human capital drives high ANS scores.</div>',
            unsafe_allow_html=True
        )

st.markdown("---")
