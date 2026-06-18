from ddgs import DDGS

OFFICIAL_SITES = {
    "samsung": "samsung.com/in",
    "apple": "apple.com/in",
    "oneplus": "oneplus.in",
    "vivo": "vivo.com/in",
    "oppo": "oppo.com/in",
    "realme": "realme.com/in",
    "dell": "dell.com/en-in",
    "hp": "hp.com/in-en",
    "lenovo": "lenovo.com/in",
    "asus": "asus.com/in"
}


def detect_brand(query: str) -> str | None:
    query_lower = query.lower()

    for brand in OFFICIAL_SITES:
        if brand in query_lower:
            return brand

    return None


def web_search_tool(query: str) -> list:
    results = []

    try:
        brand = detect_brand(query)

        if brand:
            official_site = OFFICIAL_SITES[brand]
            search_query = f"{query} site:{official_site}"
        else:
            search_query = f"{query} official site price specifications"

        with DDGS() as ddgs:
            for item in ddgs.text(search_query, max_results=10):

                url = item.get("href", "")

                # Keep only official results
                if brand and OFFICIAL_SITES[brand] not in url:
                    continue

                results.append({
                    "title": item.get("title"),
                    "url": url,
                    "snippet": item.get("body"),
                    "source_type": "official" if brand else "web"
                })

        if not results:
            return [{
                "title": "No official product results found",
                "url": None,
                "snippet": "Try using a more specific brand or product name.",
                "source_type": "not_found"
            }]

        return results

    except Exception as e:
        return [{
            "title": "Search error",
            "url": None,
            "snippet": str(e),
            "source_type": "error"
        }]