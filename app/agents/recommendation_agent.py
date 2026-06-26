import logging
logger = logging.getLogger("IntelliCart")
logger.info("Starting Recommendation Agent")

from dotenv import load_dotenv
load_dotenv()

import json
import re

from agno.agent import Agent
from agno.models.nvidia import Nvidia

from app.tools.selling_strategy_tool import selling_strategy_tool
from app.tools.database_tool import save_recommendation_output

recommendation_agent = Agent(
    name="Recommendation Agent",
    model=Nvidia(id="meta/llama-3.3-70b-instruct"),
    instructions=[
        "Recommend the best product based on user needs.",
        "Return only valid JSON.",
        "Do not fabricate prices or specifications.",
        "If price is not verified, mention that clearly.",
        "Always include confidence_score from 0 to 100."
    ],
    markdown=False
)


def extract_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("Could not parse JSON from recommendation response")


def score_product(product: dict, user_message: str, reviews) -> dict:
    score = 0
    reasons = []

    specs = (product.get("specs") or "").lower()
    name = product.get("name", "")

    user_lower = user_message.lower()

    if "gaming" in user_lower:
        if "gaming" in specs:
            score += 25
            reasons.append("Matches gaming requirement")

        if "processor" in specs or "octa-core" in specs:
            score += 25
            reasons.append("Has processor-related specs useful for gaming")

        if "ram" in specs:
            score += 15
            reasons.append("RAM mentioned, useful for multitasking and gaming")

        if "display" in specs or "amoled" in specs:
            score += 15
            reasons.append("Good display-related specs for gaming")

        if "battery" in specs:
            score += 10
            reasons.append("Battery mentioned, useful for long gaming sessions")

    if "5g" in specs:
        score += 5
        reasons.append("Supports 5G connectivity")

    review_text = str(reviews).lower()

    if "positive" in review_text:
        score += 5
        reasons.append("Review sentiment is positive")

    if score > 100:
        score = 100

    return {
        **product,
        "score": score,
        "score_reasons": reasons
    }


def rank_products(products: list, user_message: str, reviews):
    scored_products = []

    for product in products:
        if isinstance(product, dict):
            scored_products.append(score_product(product, user_message, reviews))

    scored_products.sort(key=lambda x: x.get("score", 0), reverse=True)

    return scored_products


def run_recommendation_agent(user_message: str, products, reviews, db=None):
    try:
        ranked_products = rank_products(products, user_message, reviews)

        top_product = ranked_products[0] if ranked_products else {}
        runner_up = ranked_products[1] if len(ranked_products) > 1 else {}

        selling_strategy = selling_strategy_tool(
            product_name=top_product.get("name", "recommended product"),
            category=top_product.get("category", "phone"),
            budget=None
        )

        response = recommendation_agent.run(f"""
User query:
{user_message}

Ranked products with calculated scores:
{ranked_products}

Review analysis:
{reviews}

Selling strategy:
{selling_strategy}

Return ONLY valid JSON in this exact format:

{{
  "top_recommendation": "{top_product.get("name", "")}",
  "confidence_score": {top_product.get("score", 0)},
  "runner_up": "{runner_up.get("name", "")}",
  "reasoning": {top_product.get("score_reasons", [])},
  "review_sentiment": "",
  "upsell": "",
  "cross_sell": "",
  "promotion": "",
  "price_verification_note": "Price is not verified because official product price was not extracted."
}}

Rules:
- Use the top ranked product as top_recommendation.
- Use the calculated score as confidence_score.
- Do not recommend products outside the extracted product list.
- Do not recommend expensive flagship products as upsell unless they are in the extracted product list.
- Do not invent prices.
""")

        structured_output = extract_json(response.content)

        if top_product:
            structured_output["top_recommendation"] = top_product.get("name")
            structured_output["confidence_score"] = top_product.get("score")
            structured_output["runner_up"] = runner_up.get("name") if runner_up else ""
            structured_output["reasoning"] = top_product.get("score_reasons", [])
            structured_output["ranked_products"] = ranked_products

        saved_to_db = False

        if db:
            save_recommendation_output(
                db=db,
                product_id=1,
                recommendation_text=json.dumps(structured_output),
                confidence_score=structured_output.get("confidence_score", 0)
            )
            saved_to_db = True

        return {
            "selling_strategy": selling_strategy,
            "ranked_products": ranked_products,
            "structured_recommendation": structured_output,
            "saved_to_db": saved_to_db
        }

    except Exception as e:
        return {"error": str(e)}
    
logger.info("Workflow completed successfully")