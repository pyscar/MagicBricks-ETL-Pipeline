"""
Scraper Configuration

This module stores configuration constants used across the scraping pipeline.
Keeping these values centralized makes the scraper easier to maintain,
update, and extend without touching core scraping logic.

Contents:
- HEADERS: HTTP request headers used to mimic a real browser and reduce blocking
- DEFAULT_CITY: Fallback city value used when no city is explicitly provided
"""

# HTTP headers used for all outgoing requests
# The User-Agent is set to mimic a modern Chrome browser to avoid bot detection
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/143.0.0.0 Safari/537.36"
    )
}

DEFAULT_CITY = "Bhubaneswar"
