from ddgs import DDGS


def review_scraper_tool(product_name: str):
    reviews = []

    try:
        query = f"{product_name} reviews user experience"

        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=10)

            for item in results:
                reviews.append({
                    "title": item.get("title"),
                    "snippet": item.get("body"),
                    "url": item.get("href")
                })

        return reviews

    except Exception as e:
        return [{"error": str(e)}]