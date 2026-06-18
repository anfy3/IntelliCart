import re
import requests
from bs4 import BeautifulSoup


def scrape_product_page(url: str) -> dict:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("title")
        page_title = title.get_text(strip=True) if title else None

        text = soup.get_text(" ", strip=True)

        price_match = re.search(r"₹\s?[\d,]+", text)
        price = price_match.group() if price_match else None

        product_matches = re.findall(
            r"Galaxy\s+[A-Z]\d+\s*5G",
            text,
            flags=re.IGNORECASE
        )

        products_found = list(set(product_matches))

        specs_keywords = [
            "battery", "display", "processor",
            "RAM", "storage", "camera", "5G"
        ]

        specs_found = [
            keyword for keyword in specs_keywords
            if keyword.lower() in text.lower()
        ]

        return {
            "page_title": page_title,
            "price": price,
            "products_found": products_found,
            "specs_found": specs_found,
            "source_url": url,
            "raw_text_preview": text[:700]
        }

    except Exception as e:
        return {
            "error": str(e),
            "source_url": url
        }