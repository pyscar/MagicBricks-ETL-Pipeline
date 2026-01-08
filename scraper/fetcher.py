"""
Page Fetcher

This module is responsible for making HTTP requests to MagicBricks pages.
It abstracts away the network layer so that fetching logic is cleanly
separated from parsing and scraping orchestration.

Responsibilities:
- Send HTTP GET requests with proper headers
- Handle request timeouts and HTTP errors
- Return raw HTML content for downstream parsing
"""

import requests
from scraper.config import HEADERS


def fetch_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The page URL to fetch

    Returns:
        str: Raw HTML content of the page

    Raises:
        PermissionError: If access is blocked (HTTP 403)
        requests.HTTPError: For other HTTP errors
    """
    response = requests.get(
        url,
        headers=HEADERS,   # Mimic a real browser to reduce blocking
        timeout=30
    )

    # Explicitly handle forbidden access (common in cloud environments)
    if response.status_code == 403:
        raise PermissionError(
            "403 Forbidden: Access blocked by MagicBricks (cloud environment detected)."
        )

    # Raise exception for other HTTP errors
    response.raise_for_status()

    return response.text
