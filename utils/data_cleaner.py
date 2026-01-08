
"""
MagicBricks Data Cleaner

This module processes raw scraped MagicBricks data and produces a clean, structured dataset
ready for analysis. It performs the following operations:

- Normalize price (Cr/Lac → numeric INR and lakh)
- Normalize carpet_area → numeric sqft, filling missing values with median
- Extract info from title → bhk, property_type, listing_type, locality, city
- Rename 'society' to 'project_name' for reliability
- Normalize furnishing and status
- Drop unused/problematic columns like title, price, carpet_area, car_parking
- Calculate price_per_sqft
- Reorder columns for a professional final dataset
"""

import pandas as pd
import os
import numpy as np

PROCESSED_DIR = "data/processed"

PROPERTY_WORDS = {"flat", "villa", "house", "apartment", "plot", "studio"}

def clean_data(raw_path: str, output_name="magicbricks_clean.csv"):
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    df = pd.read_csv(raw_path)
    df.columns = df.columns.str.lower()

    # ---------------- PRICE ---------------- #
    def price_to_inr(price_str):
        if pd.isna(price_str):
            return np.nan
        price_str = str(price_str).replace("₹", "").replace(",", "").strip()
        if "Cr" in price_str:
            return float(price_str.replace("Cr", "").strip()) * 10_000_000
        if "Lac" in price_str or "Lakh" in price_str:
            return float(price_str.replace("Lac", "").replace("Lakh", "").strip()) * 100_000
        return float(price_str)

    df["price_inr"] = df["price"].apply(price_to_inr)
    df["price_lakh"] = (df["price_inr"] / 100_000).astype(int)

    # ---------------- CARPET AREA ---------------- #
    df["carpet_area_sqft"] = (
        df["carpet_area"]
        .astype(str)
        .str.replace("sqft", "", regex=False)
        .str.strip()
    )
    df["carpet_area_sqft"] = pd.to_numeric(df["carpet_area_sqft"], errors="coerce")

    median_area = int(df["carpet_area_sqft"].median())
    df["carpet_area_sqft"] = df["carpet_area_sqft"].fillna(median_area).astype(int)

    # ---------------- PRICE PER SQFT ---------------- #
    df["price_per_sqft"] = (
        df["price_inr"] / df["carpet_area_sqft"].replace(0, np.nan)
    ).round(2)
    df["price_per_sqft"] = df["price_per_sqft"].fillna(0)

    # ---------------- BHK ---------------- #
    df["bhk"] = df["title"].str.extract(r"(\d+)\s*BHK")[0]
    df["bhk"] = df["bhk"].fillna(0).astype(int)

    # ---------------- PROPERTY TYPE ---------------- #
    df["property_type"] = df["title"].str.extract(r"BHK\s+(\w+)")[0].str.title()

    # ---------------- LISTING TYPE ---------------- #
    df["listing_type"] = df["title"].str.extract(r"(for Sale|for Rent)")[0]

    # ---------------- PROJECT NAME (ROBUST) ---------------- #
    def extract_project_name(row):
        society = str(row.get("society", "")).strip()
        title = str(row.get("title", "")).lower()

        if society and society.lower() not in PROPERTY_WORDS:
            return society

        if " in " in title:
            after_in = title.split(" in ", 1)[1]
            parts = [p.strip() for p in after_in.split(",")]

            if len(parts) >= 3:
                candidate = parts[0]
            elif len(parts) == 2:
                candidate = parts[0]
            else:
                candidate = ""

            if candidate and candidate.lower() not in PROPERTY_WORDS:
                return candidate.title()

        return "Independent Property"

    df["project_name"] = df.apply(extract_project_name, axis=1)
    df.drop(columns=["society"], inplace=True, errors="ignore")

    # ---------------- LOCALITY & CITY ---------------- #
    def extract_locality_city(title):
        if pd.isna(title) or " in " not in title:
            return pd.Series(["Unknown", "Unknown"])

        location = title.split(" in ", 1)[1].strip()
        parts = [p.strip() for p in location.split(",")]

        # New Delhi handling
        if location.endswith("New Delhi"):
            city = "New Delhi"
            locality = parts[-2] if len(parts) >= 2 else "Unknown"
            return pd.Series([locality, city])

        # Normal comma-separated
        if len(parts) >= 2:
            city = parts[-1]
            locality = parts[-2]
            return pd.Series([locality, city])

        # Space-separated fallback (Chennai cases)
        words = parts[0].split()
        if len(words) >= 2:
            return pd.Series([" ".join(words[:-1]), words[-1]])

        return pd.Series(["Unknown", "Unknown"])

    df[["locality", "city"]] = df["title"].apply(extract_locality_city)

    # ---------------- NORMALIZE ---------------- #
    df["furnishing"] = df["furnishing"].str.title().fillna("Unfurnished")
    df["status"] = df["status"].str.title().fillna("Unknown")

    # ---------------- CLEANUP ---------------- #
    df.drop(columns=["title", "price", "carpet_area", "car_parking"], inplace=True, errors="ignore")

    final_columns = [
        "project_name",
        "property_type",
        "listing_type",
        "city",
        "locality",
        "furnishing",
        "status",
        "bhk",
        "bathrooms",
        "price_lakh",
        "carpet_area_sqft",
        "price_per_sqft",
    ]
    
    df_clean = df[final_columns].copy()  

    # ---------------- FINAL DISPLAY LOGIC FOR PROJECT NAME ---------------- #
    if "project_name" in df_clean.columns:
        non_empty_count = (
            df_clean["project_name"]
            .astype(str)
            .str.strip()
            .replace("Independent Property", "")
            .replace("nan", "")
            .ne("")
            .sum()
        )

        # Case 1: Entire column has no meaningful values → drop it
        if non_empty_count == 0:
            df_clean.drop(columns=["project_name"], inplace=True)

        # Case 2: Column has some valid values → fill missing safely
        else:
            df_clean["project_name"] = (
                df_clean["project_name"]
                .replace("", np.nan)
                .fillna("Project Name Not Available")
            )

    output_path = os.path.join(PROCESSED_DIR, output_name)
    df_clean.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Cleaned data saved to: {output_path}")
