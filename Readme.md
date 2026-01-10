# MagicBricks Property Data Scraper & ETL Pipeline

An end-to-end **ETL (Extract → Transform → Load)** web scraping application that collects real-estate listings from **MagicBricks**, cleans and normalizes the data, and provides downloadable CSV outputs through an interactive **Streamlit** interface.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-bs4-green)](https://www.crummy.com/software/BeautifulSoup/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-yellow)](https://pandas.pydata.org/)[![Streamlit](https://img.shields.io/badge/Streamlit-App-red)](https://streamlit.io/)
[![Web%20Scraping](https://img.shields.io/badge/Web%20Scraping-ETL-purple)](#)[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)](#)


---

## 🚀 Live Demo
🔗 **Streamlit App:**  
👉 https://magicbricks-etl-pipeline-zprhaau8atehq76sgrfpyy.streamlit.app/

---

## 🧠 Project Overview

This project automates the process of collecting and preparing real-estate data for analysis.

### ✔️ What it does
- Scrapes property listings from MagicBricks
- Handles pagination automatically
- Cleans inconsistent location formats (city & locality)
- Normalizes prices, areas, and property attributes
- Provides raw and cleaned CSV downloads
- Visualizes an ETL pipeline inside a Streamlit app

---

## 🔁 ETL Pipeline

🌐 **Extract** → 🧹 **Transform** → 📦 **Load**

- **Extract:** Web scraping using BeautifulSoup  
- **Transform:** Data cleaning, validation, normalization  
- **Load:** Structured CSV files ready for analysis  

---

### Tools & Libraries
- **Python**
- **BeautifulSoup (bs4)**
- **Requests**
- **Pandas**
- **Streamlit**
- **LXML**

---

## 📂 Project Structure

```

magicbricks-etl-pipeline/
│
├── app.py                     # Streamlit application
├── requirements.txt           # Project dependencies
├── README.md
│
├── scraper/
│   ├── __init__.py            # Marks scraper as a Python package
│   ├── scraper.py             # Scraping controller
│   ├── fetcher.py             # HTTP requests
│   ├── parser.py              # HTML parsing
│   ├── paginator.py           # Pagination logic
│   └── config.py              # Headers & constants
│
├── utils/
│   ├── __init__.py            # Utility package
│   └── data_cleaner.py        # Data cleaning & transformation
│
├── data/
│   ├── raw/                   # Raw CSV samples
│   └── processed/             # Cleaned CSV samples
│
└── .streamlit/
    └── config.toml            # Streamlit theme configuration


````

---

### 1️⃣ Clone the repository
```bash
git clone [https://github.com/pyscar/MagicBricks-ETL-Pipeline]
cd magicbricks-etl-pipeline
````

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Streamlit app

```bash
streamlit run app.py
```

---

## 📥 Outputs

### Raw Data

* Original scraped data
* Minimal processing
* Useful for debugging or re-processing

### Cleaned Data

* Standardized prices (INR / Lakh)
* Clean locality & city extraction
* Normalized property attributes
* Analysis-ready format

---

## 🧠 Key Challenges Solved

* Mixed location formats (comma & space separated)
* Missing project names
* City vs locality misclassification (e.g., *New Delhi*)
* Pagination handling
* Safe scraping with headers & timeouts

---

## 📌 Future Enhancements

* Add price & BHK filters
* Interactive charts (price distribution)
* Database storage (PostgreSQL / SQLite)
* Scheduled scraping
* API layer

---
## ⚠️ Note on Web Scraping

MagicBricks actively blocks scraping from cloud environments such as:

- Streamlit Cloud
- GitHub Codespaces
- AWS / GCP / Azure servers

### ✅ Expected behavior
- Scraper works when run **locally** and through the web
- Streamlit cloud app demonstrates:
  - ETL pipeline
  - Data cleaning logic
  - CSV previews
  - UI & workflow
---
### ⚠️ Demo Mode 🧪

* In some cloud environments, live scraping from MagicBricks may be blocked (HTTP 403).
 When this happens, the app automatically switches to demo mode using sample Mumbai data:

  - 📄 sample_mumbai_raw_data.csv
 → Preview raw data

  - 🧹 sample_mumbai_cleaned_data.csv
 → Preview cleaned data

* This ensures you can still explore the ETL pipeline and test all functionality without live data.

## ⚠️ Disclaimer
This project is intended for **educational and portfolio purposes**.
Please respect MagicBricks’ terms of service when scraping data.

---

## 👤 Author

**Oscar Kiamba**
Computer Science (AI & ML) | Data science & Ml Enthusiast

📫 Connect with me on GitHub & LinkedIn
👉 https://github.com/pyscar
👉 https://www.linkedin.com/in/oscar-kiamba/

## Complete video link for the project
* video link -> https://www.youtube.com/watch?v=VzqiQuwK2C0
















