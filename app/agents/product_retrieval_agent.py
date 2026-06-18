import json
import re

from dotenv import load_dotenv
load_dotenv()

from agno.agent import Agent
from agno.models.nvidia import Nvidia

from app.tools.web_search_tool import web_search_tool
from app.tools.database_tool import save_products_to_db
from app.tools.product_scraper_tool import scrape_product_page


product_retrieval_agent = Agent(
    name="Product Retrieval Agent",
    model=Nvidia(id="meta/llama-3.3-70b-instruct"),
    instructions=[
        "You are the Product Retrieval Agent.",
        "Use only official/original brand website results when available.",
        "Extract products dynamically from official search results and scraped page details.",
        "Do not invent products.",
        "Return only valid JSON when asked.",
        "If price is not available, use null."
    ],
    markdown=False
)


def extract_json_from_text(text: str):
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return []


def normalize_products(products: list, search_results: list):
    normalized = []

    for product in products:
        if not isinstance(product, dict):
            continue

        name = product.get("name")
        if not name:
            continue

        source_url = product.get("source_url")

        if not source_url and search_results:
            source_url = search_results[0].get("url")

        normalized.append({
            "name": name,
            "category": product.get("category") or "Product",
            "brand": product.get("brand"),
            "price": product.get("price"),
            "rating": None,
            "specs": product.get("specs") or "Extracted from official source",
            "source_url": source_url,
            "availability": product.get("availability") or "Available"
        })

    unique_products = []
    seen = set()

    for product in normalized:
        if product["name"] not in seen:
            unique_products.append(product)
            seen.add(product["name"])

    return unique_products[:5]


def run_product_retrieval_agent(user_message: str, intent: str, db=None):
    try:
        search_results = web_search_tool(user_message)

        scraped_pages = []

        for result in search_results[:3]:
            url = result.get("url", "")
            if url:
                scraped_pages.append(scrape_product_page(str(url)))

        response = product_retrieval_agent.run(f"""
Extract every real product mentioned in these official search results and scraped official pages.

User Query:
{user_message}

Intent:
{intent}

Official Search Results:
{search_results}

Scraped Official Pages:
{scraped_pages}

Return ONLY valid JSON as a list.

Format:
[
  {{
    "name": "",
    "brand": "",
    "category": "",
    "price": null,
    "specs": "",
    "source_url": "",
    "availability": "Available"
  }}
]

Rules:
- Do not invent products.
- Use only products found in official source results or scraped pages.
- Do not include page titles that are not actual product names.
- If price is not found, use null.
""")

        llm_products = extract_json_from_text(response.content)

        extracted_products = normalize_products(
            products=llm_products,
            search_results=search_results
        )

        saved_products = []

        if db and extracted_products:
            saved_products = save_products_to_db(
                db=db,
                products=extracted_products
            )

        return {
            "search_results": search_results,
            "scraped_pages": scraped_pages,
            "extracted_products": extracted_products,
            "saved_product_count": len(saved_products),
            "agent_output": response.content
        }

    except Exception as e:
        return {"error": str(e)}