import re
import requests
from bs4 import BeautifulSoup


INVALID_PRICE_HINTS = [
    "under",
    "below",
    "upto",
    "up to",
    "budget",
    "minimum",
    "maximum"
]


def clean_price(price_text):
    if not price_text:
        return None

    text_lower = price_text.lower()

    if any(word in text_lower for word in INVALID_PRICE_HINTS):
        return None

    matches = re.findall(r"₹\s?[\d,]+", price_text)

    valid_prices = []

    for match in matches:
        number = match.replace("₹", "").replace(",", "").strip()

        try:
            value = float(number)
            if 1000 <= value <= 300000:
                valid_prices.append(value)
        except:
            continue

    if not valid_prices:
        return None

    return min(valid_prices)


def extract_rating(text):
    patterns = [
        r"(\d\.\d)\s*out of\s*5",
        r"(\d\.\d)\s*/\s*5",
        r"rating\s*[:\-]?\s*(\d\.\d)",
        r"rated\s*(\d\.\d)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return float(match.group(1))

    return None


def extract_products(text):
    patterns = [
        r"Galaxy\s+[A-Z]\d+\s*5G",
        r"iPhone\s+\d+\s*(?:Pro|Plus|Pro Max)?",
        r"OnePlus\s+\d+[A-Za-z]*",
        r"Dell\s+[A-Za-z0-9\s-]+",
        r"HP\s+[A-Za-z0-9\s-]+",
        r"ASUS\s+[A-Za-z0-9\s-]+"
    ]

    products = []

    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        products.extend(matches)

    cleaned = []

    for product in products:
        product = " ".join(product.split())

        if len(product) < 5:
            continue

        if product not in cleaned:
            cleaned.append(product)

    return cleaned[:10]


def scrape_product_page(url: str) -> dict:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("title")
        page_title = title.get_text(strip=True) if title else None

        text = soup.get_text(" ", strip=True)

        price = None

        price_selectors = [
            "[class*='price']",
            "[class*='Price']",
            "[class*='amount']",
            "[class*='Amount']",
            "[data-testid*='price']",
            "[aria-label*='price']",
            "span",
            "div"
        ]

        for selector in price_selectors:
            for tag in soup.select(selector):
                tag_text = tag.get_text(" ", strip=True)
                extracted_price = clean_price(tag_text)

                if extracted_price:
                    price = extracted_price
                    break

            if price:
                break

        if not price:
            price = clean_price(text)

        rating = extract_rating(text)

        products_found = extract_products(text)

        specs_keywords = [
            "battery",
            "display",
            "processor",
            "RAM",
            "storage",
            "camera",
            "5G",
            "refresh rate",
            "charging",
            "AMOLED",
            "gaming",
            "octa-core",
            "Snapdragon",
            "Exynos",
            "graphics"
        ]

        specs_found = [
            keyword for keyword in specs_keywords
            if keyword.lower() in text.lower()
        ]

        return {
            "page_title": page_title,
            "price": price,
            "rating": rating,
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