"""
Parses raw HTML from MagicBricks listing pages and extracts
structured property information.

This module is responsible ONLY for:
- Reading HTML content
- Locating property cards
- Extracting visible text fields safely
- Returning clean Python dictionaries

It does NOT handle:
- HTTP requests
- Pagination
- File saving
"""

from bs4 import BeautifulSoup


def parse_properties(html: str) -> list:
    """Extract property details from a MagicBricks HTML page."""
    
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    properties = []

    # Each property listing is wrapped inside this div
    cards = soup.find_all("div", class_="mb-srp__list")

    for prop in cards:
        # Default structure for one property
        record = {
            "title": "",
            "price": "",
            "carpet_area": "",
            "furnishing": "",
            "status": "",
            "society": "",
            "car_parking": "",
            "bathrooms": ""
        }

        # Helper function to safely extract text
        # Prevents errors if a tag is missing
        def safe_text(parent, selector, attr=None, value=None):
            tag = (
                parent.find(selector, attrs={attr: value})
                if attr else parent.find(selector)
            )
            return tag.text.strip() if tag else ""

        # Property title
        record["title"] = safe_text(prop, "h2", "class", "mb-srp__card--title")

        # Price value
        record["price"] = safe_text(prop, "div", "class", "mb-srp__card__price--amount")

        # Carpet area (sqft)
        carpet = prop.find("div", attrs={"data-summary": "carpet-area"})
        if carpet:
            record["carpet_area"] = safe_text(
                carpet, "div", "class", "mb-srp__card__summary--value"
            )

        # Furnishing status
        furnishing = prop.find("div", attrs={"data-summary": "furnishing"})
        if furnishing:
            record["furnishing"] = safe_text(
                furnishing, "div", "class", "mb-srp__card__summary--value"
            )

        # Construction status (Ready / Under Construction)
        status = prop.find("div", attrs={"data-summary": "status"})
        if status:
            record["status"] = safe_text(
                status, "div", "class", "mb-srp__card__summary--label"
            )

        # Society / Project name
        society = prop.find("div", attrs={"data-summary": "society"})
        if society:
            record["society"] = safe_text(
                society, "div", "class", "mb-srp__card__summary--value"
            )

        # Parking information
        parking = prop.find("div", attrs={"data-summary": "parking"})
        if parking:
            record["car_parking"] = safe_text(
                parking, "div", "class", "mb-srp__card__summary--value"
            )

        # Number of bathrooms
        bathroom = prop.find("div", attrs={"data-summary": "bathroom"})
        if bathroom:
            record["bathrooms"] = safe_text(
                bathroom, "div", "class", "mb-srp__card__summary--value"
            )

        # Add extracted property to list
        properties.append(record)

    return properties
