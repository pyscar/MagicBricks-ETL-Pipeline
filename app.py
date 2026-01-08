import streamlit as st
import os
import pandas as pd

from scraper.scraper import run_scraper
from utils.data_cleaner import clean_data


# -------------------------------
# Page config 
# -------------------------------
st.set_page_config(
    page_title="MagicBricks ETL Pipeline",
    layout="centered"
)


# -------------------------------
# Button styling
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
    color: white;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------
# Title + Icon
# -------------------------------
st.markdown(
    "<h1 style='text-align:center; color:#1f77b4;'>MagicBricks ETL Pipeline</h1>",
    unsafe_allow_html=True
)


st.markdown(
    "<div style='text-align: center; transform: translateX(-28px); font-size: 48px;'>🏠</div>",
    unsafe_allow_html=True
)


# -------------------------------
# Session state
# -------------------------------
if "scraped" not in st.session_state:
    st.session_state.scraped = False

if "cleaned" not in st.session_state:
    st.session_state.cleaned = False


# -------------------------------
# User inputs
# -------------------------------
url = st.text_input("Enter MagicBricks URL",placeholder="https://www.magicbricks.com/...")

city_name = st.text_input("Enter city name (e.g. mumbai, chennai)",placeholder="mumbai").strip().lower()


# -------------------------------
# File paths
# -------------------------------
raw_file = f"{city_name}_raw_data.csv"
clean_file = f"{city_name}_cleaned_data.csv"

raw_path = os.path.join("data", "raw", raw_file)
clean_path = os.path.join("data", "processed", clean_file)


# -------------------------------
# Run scraper (Extract)
# -------------------------------
if st.button("Run Scraper"):
    if not url or not city_name:
        st.error("Please enter both URL and city name")
    else:
        with st.spinner("Extracting data from MagicBricks..."):
            run_scraper(url, raw_path)
            st.session_state.scraped = True
        st.success("Extraction completed")


# -------------------------------
# Preview + download raw data
# -------------------------------
if st.session_state.scraped and os.path.exists(raw_path):

    st.markdown("### Preview Raw Data")
    df_raw = pd.read_csv(raw_path)
    st.dataframe(df_raw.head(5), use_container_width=True)

    with open(raw_path, "rb") as f:
        st.download_button(
            label="Download Raw Data",
            data=f,
            file_name=raw_file,
            mime="text/csv"
        )


# -------------------------------
# Clean data (Transform)
# -------------------------------
if st.session_state.scraped:
    if st.button("Clean Data"):
        with st.spinner("Transforming raw data..."):
            clean_data(raw_path, clean_file)
            st.session_state.cleaned = True
        st.success("Transformation completed")


# -------------------------------
# ETL Pipeline Visualization
# -------------------------------
st.markdown("<h2 style='text-align:center; color:#1f77b4;'>Data Pipeline</h2>",unsafe_allow_html=True)

c1, a1, c2, a2, c3 = st.columns([2, 1, 2, 1, 2])

def pipeline_box(label, color):
    text_color = "white" if color != "#ffffff" else "black"
    return f"""
    <div style="
        padding:20px;
        border-radius:12px;
        background:{color};
        text-align:center;
        font-weight:600;
        color:{text_color};
        box-shadow:0 4px 10px rgba(0,0,0,0.15);
    ">
        {label}
    </div>
    """

with c1:
    st.markdown(
        pipeline_box("Extract", "#2ecc71"),  # green
        unsafe_allow_html=True
    )

with a1:
    st.markdown(
        "<div style='text-align:center; font-size:30px; margin-top:15px;'>➡️</div>",
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        pipeline_box("Transform", "#3498db"),  # blue
        unsafe_allow_html=True
    )

with a2:
    st.markdown(
        "<div style='text-align:center; font-size:30px; margin-top:15px;'>➡️</div>",
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        pipeline_box("Load", "#ffffff"),  # white
        unsafe_allow_html=True
    )

# -------------------------------
# Preview + download cleaned data
# -------------------------------
if st.session_state.cleaned and os.path.exists(clean_path):

    st.markdown("### Preview Cleaned Data")
    df_clean = pd.read_csv(clean_path)
    st.dataframe(df_clean.head(5), use_container_width=True)

    with open(clean_path, "rb") as f:
        st.download_button(
            label="Download Cleaned Data",
            data=f,
            file_name=clean_file,
            mime="text/csv"
        )


# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Built with Python • BeautifulSoup • Pandas • Streamlit")
