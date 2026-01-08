"""
Main entry point for the MagicBricks scraping pipeline.

This script:
1. Takes user input (URL and city name)
2. Scrapes raw property data
3. Cleans the scraped data
4. Saves both raw and cleaned CSV files

Run this file to execute the full workflow.
"""

from scraper.scraper import run_scraper
from utils.data_cleaner import clean_data
import os


if __name__ == "__main__":
    # Get target MagicBricks URL from user
    url = input("Enter Magicbricks URL: ").strip()

    # City name used for naming output files
    city_name = input("Enter city name (e.g. mumbai, bhubaneswar): ").strip().lower()

    # Output file names
    raw_file = f"{city_name}_raw_data.csv"
    clean_file = f"{city_name}_cleaned_data.csv"

    # Path to store raw scraped data
    raw_path = os.path.join("data", "raw", raw_file)

    # Start scraping process
    print("\nStarting scraping process...\n")
    run_scraper(url, raw_path)

    # Start data cleaning process
    print("\nStarting cleaning process...\n")
    clean_data(raw_path, clean_file)

    # Final success message
    print("\nPipeline completed successfully ✔")
