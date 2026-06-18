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


def run_recommendation_agent(user_message: str, products, reviews, db=None):
    try:
        selling_strategy = selling_strategy_tool(
            product_name="recommended product",
            category="phone",
            budget=None
        )

        response = recommendation_agent.run(f"""
User query:
{user_message}

Products:
{products}

Review analysis:
{reviews}

Selling strategy:
{selling_strategy}

Return ONLY valid JSON in this exact format:

{{
  "top_recommendation": "",
  "confidence_score": 0,
  "runner_up": "",
  "reasoning": [],
  "review_sentiment": "",
  "upsell": "",
  "cross_sell": "",
  "promotion": "",
  "price_verification_note": ""
}}
""")

        structured_output = extract_json(response.content)

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
            "structured_recommendation": structured_output,
            "saved_to_db": saved_to_db
        }

    except Exception as e:
        return {"error": str(e)}