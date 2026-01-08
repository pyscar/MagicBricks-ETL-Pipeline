"""
Pagination Handler

Extracts the URL of the next results page from MagicBricks HTML.
Used to navigate through paginated property listings.
"""

from bs4 import BeautifulSoup


def get_next_page_url(html: str) -> str | None:
    """
    Returns the next page URL if pagination exists, otherwise None.
    """
    soup = BeautifulSoup(html, "lxml")

    next_btn = soup.find("a", attrs={"title": "Next"})

    if next_btn and next_btn.get("href"):
        return "https://www.magicbricks.com" + next_btn["href"]

    return None
