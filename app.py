"""
MagicBricks ETL Pipeline Streamlit App
--------------------------------------
Gracefully handles live scraping failures (403) by switching
to demo mode using sample Mumbai datasets.
"""

from scraper.scraper import run_scraper
from utils.data_cleaner import clean_data
import streamlit as st
import os
import pandas as pd
import requests

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="MagicBricks ETL Pipeline",
    layout="centered"
)

# -------------------------------
# Session state
# -------------------------------
if "scraped" not in st.session_state:
    st.session_state.scraped = False

if "cleaned" not in st.session_state:
    st.session_state.cleaned = False

if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

# -------------------------------
# Styling
# -------------------------------
st.markdown("""
<style>
div.stButton > button {
    background-color: #2ecc71;
    color: white;
    border-radius: 8px;
    padding: 0.5em 1.5em;
    font-weight: 600;
    border: none;
}
div.stButton > button:hover {
    background-color: #27ae60;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Title
# -------------------------------
st.markdown(
    "<h1 style='text-align:center; color:#1f77b4;'>MagicBricks ETL Pipeline</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<div style='text-align:center; font-size:48px;'>🏠</div>",
    unsafe_allow_html=True
)

# -------------------------------
# Inputs
# -------------------------------
url = st.text_input(
    "Enter MagicBricks URL",
    placeholder="https://www.magicbricks.com/property-for-sale/..."
)

city_name = st.text_input(
    "Enter city name (e.g. mumbai)",
    placeholder="mumbai"
).strip().lower()

# -------------------------------
# Default file paths
# -------------------------------
raw_file = f"{city_name}_raw_data.csv"
clean_file = f"{city_name}_cleaned_data.csv"

raw_path = os.path.join("data", "raw", raw_file)
clean_path = os.path.join("data", "processed", clean_file)

# -------------------------------
# Run Scraper (Extract)
# -------------------------------
if st.button("Run Scraper"):
    if not url or not city_name:
        st.error("Please enter both URL and city name")
    else:
        try:
            with st.spinner("Extracting data from MagicBricks..."):
                run_scraper(url, raw_path)

            st.session_state.scraped = True
            st.session_state.demo_mode = False
            st.success("Extraction completed successfully")

        except Exception as e:
            error_message = str(e)

            if "403" in error_message or "Forbidden" in error_message:
                st.session_state.demo_mode = True
                st.session_state.scraped = True

                st.warning("Live scraping blocked by MagicBricks (403 Forbidden)")
                st.info("Demo mode enabled using sample Mumbai data")

            else:
                st.error("An unexpected error occurred")
                st.code(error_message)

# -------------------------------
# Demo mode override paths
# -------------------------------
if st.session_state.demo_mode:
    raw_path = os.path.join("data", "raw", "sample_mumbai_raw_data.csv")
    clean_path = os.path.join("data", "processed", "sample_mumbai_cleaned_data.csv")

    st.markdown(
        """
        <div style="
            background:#fff3cd;
            padding:12px;
            border-radius:8px;
            color:#856404;
            font-weight:600;
            text-align:center;
            margin-bottom:20px;
        ">
        ⚠️ DEMO MODE ENABLED — Live scraping blocked on cloud environment.<br>
        Showing sample Mumbai data to demonstrate ETL pipeline.
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# Preview Raw Data
# -------------------------------
if st.session_state.scraped and os.path.exists(raw_path):
    st.markdown("### 📄 Raw Data Preview")
    df_raw = pd.read_csv(raw_path)
    st.dataframe(df_raw.head(5), width='stretch')
    
    with open(raw_path, "rb") as f:
        st.download_button(
            label="Download Raw Data",
            data=f,
            file_name=os.path.basename(raw_path),
            mime="text/csv"
        )

# -------------------------------
# Clean Data (Transform)
# -------------------------------
if st.session_state.scraped and not st.session_state.demo_mode:
    if st.button("Clean Data"):
        with st.spinner("Transforming raw data..."):
            clean_data(raw_path, clean_file)
            st.session_state.cleaned = True
        st.success("Transformation completed")

# -------------------------------
# Pipeline Visualization
# -------------------------------
st.markdown("<h2 style='text-align:center;'>ETL Pipeline</h2>", unsafe_allow_html=True)

c1, a1, c2, a2, c3 = st.columns([2, 1, 2, 1, 2])

def box(label, color):
    return f"""
    <div style="
        padding:20px;
        border-radius:12px;
        background:{color};
        text-align:center;
        font-weight:600;
        color:white;
    ">
        {label}
    </div>
    """

with c1:
    st.markdown(box("Extract", "#2ecc71"), unsafe_allow_html=True)
with a1:
    st.markdown("➡️", unsafe_allow_html=True)
with c2:
    st.markdown(box("Transform", "#3498db"), unsafe_allow_html=True)
with a2:
    st.markdown("➡️", unsafe_allow_html=True)
with c3:
    st.markdown(box("Load", "#9b59b6"), unsafe_allow_html=True)

# -------------------------------
# Preview Cleaned Data
# -------------------------------
if (st.session_state.cleaned or st.session_state.demo_mode) and os.path.exists(clean_path):
    st.markdown("### 🧹 Cleaned Data Preview")
    df_clean = pd.read_csv(clean_path)
    st.dataframe(df_clean.head(5), width='stretch')

    with open(clean_path, "rb") as f:
        st.download_button(
            label="Download Cleaned Data",
            data=f,
            file_name=os.path.basename(clean_path),
            mime="text/csv"
        )

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Built with Python • BeautifulSoup • Pandas • Streamlit")
