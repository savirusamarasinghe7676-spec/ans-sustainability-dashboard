
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
