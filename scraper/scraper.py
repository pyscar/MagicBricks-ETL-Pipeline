"""
MagicBricks Web Scraper

This module handles the raw data scraping process for MagicBricks property listings.
It starts from a user-provided search URL, automatically paginates through all
available result pages, extracts structured property data, and saves it as a raw CSV.

Key responsibilities:
- Fetch HTML pages using a resilient fetcher
- Parse property cards into structured records
- Handle pagination until no next page exists
- Save all collected records into a raw CSV file

This module is intentionally kept clean and focused only on data ingestion.
All data cleaning, normalization, and feature engineering are handled separately
inside utils/data_cleaner.py.
"""

import csv
import os
from scraper.fetcher import fetch_page
from scraper.parser import parse_properties
from scraper.paginator import get_next_page_url


def run_scraper(start_url: str, output_path: str):
    """
    Scrapes MagicBricks property data starting from the given URL
    and saves raw data to the specified output path.

    Parameters:
    - start_url (str): MagicBricks search results URL provided by the user
    - output_path (str): Full file path where raw CSV data will be saved
    """

    # Ensure the raw data directory exists before saving the file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    all_records = []
    current_url = start_url
    page_count = 1

    # Loop through paginated result pages
    while current_url:
        print(f"Scraping page {page_count}")

        # Fetch HTML content of the current page
        html = fetch_page(current_url)

        # Parse property listings from the page
        records = parse_properties(html)

        # Stop if no records are found (safety check)
        if not records:
            print("No records found on this page. Stopping pagination.")
            break

        # Accumulate all property records
        all_records.extend(records)

        # Get the next page URL (if available)
        next_url = get_next_page_url(html)
        if not next_url:
            print("No next page found. Scraping completed.")
            break

        current_url = next_url
        page_count += 1

    # Exit early if scraping returned no data
    if not all_records:
        print("No data scraped.")
        return

    # Write scraped data to raw CSV
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_records[0].keys())
        writer.writeheader()
        writer.writerows(all_records)

    print(f"\nScraped {len(all_records)} properties")
    print(f"Raw data saved to: {output_path}")
